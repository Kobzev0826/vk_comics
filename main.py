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


def upload_random_xkcd_comics_to_vk(my_token, vk_community_id):
    try:
        right_limit_random = get_max_num_xkcd()
        rand_num = random.randint(0, right_limit_random)
        url = f'https://xkcd.com/{rand_num}/info.0.json'
        image_url = get_comics_info(url)['img']
        comics_name = download_image_tmp(image_url)
        vk_api.add_image_to_community(my_token, vk_community_id, comics_name)
    finally:
        os.remove(comics_name)


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    vk_community_id = os.getenv('VK_COMMUNITY_ID')
    upload_random_xkcd_comics_to_vk(vk_token, vk_community_id)
