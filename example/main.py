import requests 

from utils import VK_API_TOKEN
from utils import VK_API_VERSION


def _check_posts_count(n_posts: int) -> None:
    if n_posts < 1:
        raise ValueError("Количество постов должно быть > 1")
    

def _is_not_club_url_type(url: str) -> bool:
    return 'public' not in url and 'club' not in url


def _get_not_public_url_type_params(search_url: str, n_posts: int, offset: int) -> dict:
    return {
        "access_token": VK_API_TOKEN,
        "domain": search_url,
        "v": VK_API_VERSION,
        "count": n_posts,
        "offset": offset
    }


def _get_public_url_type_params(public_id: int, n_posts: int, offset: int) -> dict:
    return {
        "access_token": VK_API_TOKEN,
        "owner_id": public_id,
        "v": VK_API_VERSION,
        "count": n_posts,
        "offset": offset
    }


def _get_group_id_from_public_type_url(search_url: str) -> str:
    if 'public' in search_url[-1]:
        return search_url[-1][6:]
    return search_url[-1][4:]


def _get_posts_list(all_posts: list[dict], search_url: str) -> list[str]:
    sorted_posts = []
    for post in all_posts:
        # В идеале вынести получение кол-ва лайков и генерацию юрла в отдельные функции
        sorted_posts.append(
            [post['likes']['count'], f'https://vk.com/{search_url}?w=wall{post["from_id"]}_{post["id"]}']
        )
    return sorted_posts


def _get_sorted_posts_list(post_list: list[str]) -> None:
    post_list.sort(key=lambda x: x[0], reverse=True)


def get_posts_from_vk(n_posts: int, search_url: str) -> list[dict]:
    offset = 0
    all_posts = []
    while offset < n_posts:
        if _is_not_club_url_type(search_url):
            response = requests.get(
                f'https://api.vk.com/method/wall.get',
                params=_get_not_public_url_type_params(
                    search_url,
                    n_posts,
                    offset
                )
            )
            data = response.json()['response']['items']
        else:
            public_id = _get_group_id_from_public_type_url(search_url)
            response = requests.get(
                f'https://api.vk.com/method/wall.get',
                params=_get_public_url_type_params(
                    public_id,
                    n_posts,
                    offset
                )
            )
            data = response.json()['response']['items']
        offset += 100
        all_posts.extend(data)
    return all_posts


def find_most_liked_vk_posts(search_url: str, n_posts: int) -> list[str]:
    _check_posts_count(n_posts)
    search_url = search_url.split(sep='/')
    all_posts = get_posts_from_vk(n_posts, search_url[-1])
    not_sorted_posts = _get_posts_list(all_posts, search_url[-1])
    _get_sorted_posts_list(not_sorted_posts)
    for post in not_sorted_posts:
        print(f"Likes: {post[0]}, URL: {post[1]}")

def plus(a,b):
    print(a + b)
    return a + b



def main():
    find_most_liked_vk_posts(
        input("VK Group URL: "),
        int(input("N Posts: "))
    )
    plus(3,2)

if __name__ == "__main__":
    main()