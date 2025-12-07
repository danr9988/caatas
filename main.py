import json
import time
import urllib.parse

import requests

from yandex_disk_client import YandexDiskClient


CATAAS_BASE_URL = "https://cataas.com"


def build_cataas_url(text: str) -> str:
    encoded_text = urllib.parse.quote(text)
    return f"{CATAAS_BASE_URL}/cat/says/{encoded_text}"


def main() -> None:
    group_name = input("Введите название вашей группы в Нетологии: ").strip()
    text_for_image = input("Введите текст для картинки: ").strip()
    yadisk_token = input("Введите токен Яндекс.Диска: ").strip()

    if not group_name or not text_for_image or not yadisk_token:
        print("Все поля обязательны для заполнения.")
        return

    image_url = build_cataas_url(text_for_image)
    yadisk_client = YandexDiskClient(token=yadisk_token)

    folder_path = group_name
    print("Создаем папку на Я.Диске...")
    yadisk_client.create_folder(folder_path)

    file_name = f"{text_for_image}.jpg"
    disk_path = f"{folder_path}/{file_name}"

    print("Запускаем загрузку файла на Я.Диск...")
    upload_info = yadisk_client.upload_file_by_url(
        disk_path=disk_path,
        file_url=image_url,
    )
    print("Задача на загрузку отправлена, ожидаем появления файла...")

    resource_info = None
    for attempt in range(5):
        try:
            resource_info = yadisk_client.get_resource_info(disk_path)
            break
        except RuntimeError:
            time.sleep(1)

    if resource_info is None:
        result_data = {
            "group_name": group_name,
            "text": text_for_image,
            "disk_path": disk_path,
            "upload_info": upload_info,
        }
    else:
        result_data = {
            "group_name": group_name,
            "text": text_for_image,
            "disk_path": disk_path,
            "size": resource_info.get("size"),
            "type": resource_info.get("type"),
            "name": resource_info.get("name"),
            "upload_info": upload_info,
        }

    with open("result.json", "w", encoding="utf-8") as json_file:
        json.dump(result_data, json_file, ensure_ascii=False, indent=4)

    print("Готово! Информация о файле сохранена в result.json.")


if __name__ == "__main__":
    main()
