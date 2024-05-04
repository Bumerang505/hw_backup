import requests
from datetime import datetime

vk_user_id = input('Введите id пользователя VK: ')
vk_token = input('Введите токен VK: ')  # 27147356
image_count = input('Введите количество скачиваемых фото: ')
yandex_token = input('Введите Яндекс токен: ')  # y0_AgAAAABWwuc2AADLWwAAAAECe4dYAACZsRUTcNVB3YLb3DRuzY8QW3JeoQ


dict_photos = {}


def vk_get_big_size_photos(vk_id, vk_access_token):
    url = f"https://api.vk.com/method/photos.get?owner_id={vk_id}&album_id=profile&extended=1&v=5.199&count={image_count}"

    headers = {
        'Authorization': f"Bearer {vk_access_token}"}

    response = requests.request("GET", url, headers=headers)

    items = response.json()['response']['items']

    for image in items:
        name = image['likes']['count']
        name_date = str(image['likes']['count']) + ' ' + str(datetime.fromtimestamp(image['date']).date())

        if image['likes']['count'] in dict_photos:
            dict_photos[name_date] = image['sizes'][-1]['url']
            with open(f"{name_date}.json", 'w') as f_json:
                f_json.write(f'[{{\n"file_name": "{name_date}.jpg",\n"size": "{image["sizes"][-1]["type"]}"\n}}]')
        else:
            dict_photos[image['likes']['count']] = image['sizes'][-1]['url']
            with open(f"{name}.json", 'w') as f_json:
                f_json.write(f'[{{\n"file_name": "{name}.jpg",\n"size": "{image["sizes"][-1]["type"]}"\n}}]')


vk_get_big_size_photos(vk_user_id, vk_token)


def download_image(url, file_name):
    response = requests.get(url)
    with open(file_name, 'wb') as file:
        file.write(response.content)


def create_folder_yandex(ya_token):
    url = f"https://cloud-api.yandex.net/v1/disk/resources?path=%2Fvk_user_id_{vk_user_id}"

    payload = {}
    headers = {
        'Authorization': f'OAuth {ya_token}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)


def get_url_for_write_ya_disk(ya_token, file_name):
    url = f"https://cloud-api.yandex.net/v1/disk/resources/upload?path=%2Fvk_user_id_{vk_user_id}%2F{file_name}.jpg"

    payload = {}
    headers = {
        'Authorization': f'OAuth {ya_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()['href']


create_folder_yandex(yandex_token)

for f_name, f_url in dict_photos.items():
    download_image(f_url, f'{f_name}.jpg')
    get_url_for_write_ya_disk(yandex_token, f_name)

    with open(f'{f_name}.jpg', 'rb') as f:
        requests.put(get_url_for_write_ya_disk(yandex_token, f_name), files={'file': f})
