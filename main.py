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
    rand_num = random.randint(0, get_max_num_xkcd())
    url = f'https://xkcd.com/{rand_num}/info.0.json'
    file_path = download_image_tmp(get_comics_info(url)['img'])
    return file_path


def upload_random_xkcd_comics_to_vk(my_token, vk_community_id):
    comics_name = download_random_comics()
    print(f"comics download with file path : {comics_name}")
    vk_api.add_image_to_community(my_token, vk_community_id, comics_name)
    os.remove(comics_name)


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    vk_community_id = os.getenv('VK_COMMUNITY_ID')

    upload_random_xkcd_comics_to_vk(vk_token, vk_community_id)
