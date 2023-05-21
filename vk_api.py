import requests, os


def get_upload_url(vk_community_id, access_token):
    upload_url = f'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'group_id': vk_community_id,
        'access_token': access_token,
        'v': 5.131
    }
    upload_response = requests.get(upload_url, params=params)
    upload_response.raise_for_status()
    return upload_response.json()['response']


def upload_photo(photo_path, access_token, vk_community_id):
    with open(photo_path, 'rb') as file:
        files = {'photo': file}
        upload_url = get_upload_url(vk_community_id, access_token)['upload_url']
        upload_response = requests.post(upload_url, files=files)
    upload_response.raise_for_status()
    uploaded_photo = upload_response.json()
    return uploaded_photo


def save_wall_photo(access_token, vk_community_id, photo, server,hash ):
    save_url = f'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': access_token,
        'v': 5.131,
        'group_id': vk_community_id,
        'photo': photo,
        'server': server,
        'hash': hash
    }
    save_response = requests.get(save_url, params=params)
    saved_photo = save_response.json()['response'][0]

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
    photo, server,hash = upload_photo(photo_path, access_token, vk_community_id)
    save_wall_photo(access_token, vk_community_id, photo, server,hash)
