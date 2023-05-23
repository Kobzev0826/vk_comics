import requests, random
import tempfile, os
import vk_api
from dotenv import load_dotenv


def download_image_tmp(url, params={}):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file.write(response.content)
        temp_file.flush()
        return temp_file.name


def get_comics_info(url, params={}):
    response = requests.get(url, params=params)
    response.raise_for_status()
    comics_info = response.json()
    return {
        "alt": comics_info['alt'],
        "img": comics_info['img'],
        "num": comics_info['num']
    }


def get_max_num_xkcd():
    return get_comics_info('https://xkcd.com/info.0.json')['num']


def download_random_comics():
    max_num_xkcd_comics = get_max_num_xkcd()
    rand_num = random.randint(0, max_num_xkcd_comics)
    url = f'https://xkcd.com/{rand_num}/info.0.json'
    comics_info = get_comics_info(url)
    comics_path = download_image_tmp(comics_info['img'])
    return comics_path, comics_info['alt']


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    vk_community_id = os.environ['VK_COMMUNITY_ID']
    try:
        comics_path, alt = download_random_comics()
        vk_api.add_image_to_community(vk_token, vk_community_id, comics_path, alt)
    finally:
        os.remove(comics_path)
