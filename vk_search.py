import requests


def search_vk(search_url, posts_count):
    if posts_count < 1:
        print('Количество постов должно быть > 0')
        return

    offset = 0
    token = 'f39fef3ff39fef3ff39fef3f02f08a6163ff39ff39fef3f97666a030d299ec0db735fc0'
    version = 5.131
    search_url = search_url.split(sep='/')
    all_posts = []

    while offset < posts_count:
        try:
            if 'public' not in search_url[-1] and 'club' not in search_url[-1]:
                response = requests.get(
                    f'https://api.vk.com/method/wall.get?access_token={token}&domain={search_url[-1]}&v={version}&count={posts_count}&offset={offset}')
                data = response.json()['response']['items']
            else:

                if 'public' in search_url[-1]:
                    url = search_url[-1][6:]
                else:
                    url = search_url[-1][4:]
                response = requests.get(
                    f'https://api.vk.com/method/wall.get?access_token={token}&owner_id={url}&v={version}&count={posts_count}&offset={offset}')
                data = response.json()['response']['items']
        except:
            print('Неверная ссылка, группа закрыта и/или в ней нет ни одного поста')
            return

        offset += 100
        all_posts.extend(data)

    posts_lst = []

    for post in all_posts:
        posts_lst.append(
            [post['likes']['count'], f'https://vk.com/{search_url[-1]}?w=wall{post["from_id"]}_{post["id"]}'])
    posts_lst.sort(key=lambda x: x[0], reverse=True)

    if posts_count < 5:
        count = posts_count
    else:
        count = 5
    try:
        for i in range(count):
            print(posts_lst[i][1])
    except:
        pass


search_vk(input(), int(input()))
