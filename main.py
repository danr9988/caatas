import json
import urllib.parse

import requests

from yandex_disk_client import YandexDiskClient


CATAAS_BASE_URL = "https://cataas.com"


def build_cataas_url(text: str) -> str:
    """Собирает URL для получения картинки кота с текстом."""
    encoded_text = urllib.parse.quote(text)
    return f"{CATAAS_BASE_URL}/cat/says/{encoded_text}"


def main() -> None:
    group_name = input("Введите название вашей группы в Нетологии: ").strip()
    text_for_image = input("Введите текст для картинки: ").strip()
    yadisk_token = input("Введите токен Яндекс.Диска: ").strip()

    if not group_name or not text_for_image or not yadisk_token:
        print("Все поля обязательны для заполнения.")
        return

    # 1. Собираем URL для котика с текстом
    image_url = build_cataas_url(text_for_image)

    # 2. Создаем клиента Я.Диска
    yadisk_client = YandexDiskClient(token=yadisk_token)

    # 3. Создаем папку с именем группы
    folder_path = group_name
    yadisk_client.create_folder(folder_path)

    # 4. Задаем путь и имя файла на диске
    file_name = f"{text_for_image}.jpg"
    disk_path = f"{folder_path}/{file_name}"

    # 5. Отправляем задачу на загрузку файла по URL
    upload_info = yadisk_client.upload_file_by_url(
        disk_path=disk_path,
        file_url=image_url,
    )

    # 6. Сохраняем информацию о файле в JSON (без запроса размера)
    result_data = {
        "group_name": group_name,
        "text": text_for_image,
        "disk_path": disk_path,
    }

    with open("result.json", "w", encoding="utf-8") as json_file:
        json.dump(result_data, json_file, ensure_ascii=False, indent=4)

    print("Готово! Информация о файле сохранена в result.json.")


if __name__ == "__main__":
    main()
