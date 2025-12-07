import requests


class YandexDiskClient:
    BASE_URL = "https://cloud-api.yandex.net/v1/disk"

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"OAuth {self.token}"
        }

    def create_folder(self, folder_path: str) -> None:
        """Создает папку на Яндекс.Диске по указанному пути."""
        url = f"{self.BASE_URL}/resources"
        params = {"path": folder_path}
        response = requests.put(url, headers=self.headers, params=params)
        if response.status_code not in (201, 409):
            # 201 — создано, 409 — уже существует
            raise RuntimeError(
                f"Не удалось создать папку '{folder_path}': "
                f"status={response.status_code}, text={response.text}"
            )

    def upload_file_by_url(self, disk_path: str, file_url: str) -> dict:
        """
        Загружает файл на Я.Диск по ссылке (по воздуху).
        disk_path — путь и имя файла на диске.
        file_url — прямой URL файла (картинка с котом).
        Возвращает словарь с информацией об операции.
        """
        url = f"{self.BASE_URL}/resources/upload"
        params = {
            "path": disk_path,
            "url": file_url,
            "overwrite": "true",
        }
        response = requests.post(url, headers=self.headers, params=params)
        if response.status_code not in (202, 201):
            raise RuntimeError(
                f"Не удалось отправить задачу на загрузку файла '{disk_path}': "
                f"status={response.status_code}, text={response.text}"
            )
        return response.json()

    def get_resource_info(self, path: str) -> dict:
        """
        Возвращает информацию о файле или папке на диске.
        Например, размер файла, тип, пути и т.п.
        """
        url = f"{self.BASE_URL}/resources"
        params = {"path": path}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise RuntimeError(
                f"Не удалось получить информацию о ресурсе '{path}': "
                f"status={response.status_code}, text={response.text}"
            )
        return response.json()
