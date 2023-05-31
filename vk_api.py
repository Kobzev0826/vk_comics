import requests, os, sys


def raise_vk_response(response):
    try:
        error = response['error']
        sys.stderr.write(f"ERROR: {error['error_msg']}")
        sys.exit()
    except KeyError:
        return


def get_upload_url(vk_community_id, access_token):
    upload_url = f'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'group_id': vk_community_id,
        'access_token': access_token,
        'v': 5.131
    }
    upload_response = requests.get(upload_url, params=params)
    upload_response.raise_for_status()
    upload_dict = upload_response.json()
    raise_vk_response(upload_dict)

    return upload_dict['response']


def upload_photo(photo_path, access_token, vk_community_id):
    with open(photo_path, 'rb') as file:
        files = {'photo': file}
        upload_url = get_upload_url(vk_community_id, access_token)['upload_url']
        upload_response = requests.post(upload_url, files=files)
    upload_response.raise_for_status()
    uploaded_photo = upload_response.json()
    raise_vk_response(uploaded_photo)
    return uploaded_photo


def post_wall_photo(access_token, vk_community_id, photo, server, photo_hash, caption=""):
    save_url = f'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': access_token,
        'v': 5.131,
        'group_id': vk_community_id,
        'photo': photo,
        'server': server,
        'hash': photo_hash,
        'caption': caption
    }

    save_response = requests.post(save_url, data=params)

    save_response.raise_for_status()

    uploaded_photo = save_response.json()
    raise_vk_response(uploaded_photo)
    saved_photo = uploaded_photo['response'][0]

    post_url = f'https://api.vk.com/method/wall.post'
    post_data = {
        'access_token': access_token,
        'v': 5.131,
        'owner_id': f"-{vk_community_id}",
        'attachments': f'photo{saved_photo["owner_id"]}_{saved_photo["id"]}'
    }
    response = requests.post(post_url, data=post_data)
    response.raise_for_status()
    raise_vk_response(response.json())


def add_image_to_community(access_token, vk_community_id, photo_path, caption=''):
    uploaded_photo = upload_photo(photo_path, access_token, vk_community_id)
    post_wall_photo(access_token, vk_community_id, uploaded_photo['photo'], uploaded_photo['server'],
                    uploaded_photo['hash'], caption)
