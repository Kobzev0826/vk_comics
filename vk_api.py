import requests, os
from dotenv import load_dotenv


def get_upload_url(vk_community_id, access_token):
    upload_url = f'https://api.vk.com/method/photos.getWallUploadServer?group_id={vk_community_id}&access_token={access_token}&v=5.131'
    upload_response = requests.get(upload_url)
    upload_response.raise_for_status()
    return upload_response.json()['response']


def upload_photo(photo_path, access_token, vk_community_id):
    with open(photo_path, 'rb') as file:
        files = {'photo': file}
        upload_server = get_upload_url(vk_community_id, access_token)['upload_url']
        upload_response = requests.post(upload_server, files=files)
        upload_response.raise_for_status()
        uploaded_photo = upload_response.json()
    return uploaded_photo


def saveWallPhoto(access_token, vk_community_id, uploaded_photo):
    # Save uploaded photo to VK
    save_url = f'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': access_token,
        'v': 5.131,
        'group_id': vk_community_id,
        'photo': uploaded_photo["photo"],
        'server': uploaded_photo["server"],
        'hash': uploaded_photo["hash"]
    }
    save_response = requests.get(save_url, params=params)
    saved_photo = save_response.json()['response'][0]

    # Post the image to your community
    post_url = f'https://api.vk.com/method/wall.post'
    post_data = {
        'access_token': access_token,
        'v': 5.131,
        'owner_id': f"-{vk_community_id}",
        'attachments': f'photo{saved_photo["owner_id"]}_{saved_photo["id"]}'
    }
    response = requests.post(post_url, data=post_data)
    response.raise_for_status()


def add_image_to_community(access_token, vk_community_id, photo_path):
    uploaded_photo = upload_photo(photo_path, access_token, vk_community_id)
    saveWallPhoto(access_token, vk_community_id, uploaded_photo)
