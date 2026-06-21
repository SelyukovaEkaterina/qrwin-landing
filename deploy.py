import os
import mimetypes
import boto3
from botocore.config import Config

# Реквизиты Beget S3
ENDPOINT_URL = 'https://s3.ru1.storage.beget.cloud'
BUCKET_NAME = '1919a3d97e3e-website'
ACCESS_KEY = '0000FO8HD1CW20L0NQG2'
SECRET_KEY = 'xeEkCSZrEJVh5VFL7jI2k1cltBCCqCgpO0bdzDXz'

def deploy():
    print("Инициализация S3 клиента...")
    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(
            signature_version='s3',
            s3={'addressing_style': 'path'}
        ),
    )

    dist_dir = 'dist'
    if not os.path.exists(dist_dir):
        print(f"Ошибка: директория {dist_dir} не найдена. Сначала запустите сборку.")
        return

    print(f"Начало деплоя из директории '{dist_dir}' в бакет '{BUCKET_NAME}'...")

    # Получаем список всех файлов в бакете, чтобы иметь возможность удалить лишние (аналог --delete)
    existing_keys = set()
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=BUCKET_NAME):
            if 'Contents' in page:
                for obj in page['Contents']:
                    existing_keys.add(obj['Key'])
    except Exception as e:
        print(f"Предупреждение при получении списка файлов: {e}")

    uploaded_keys = set()

    for root, dirs, files in os.walk(dist_dir):
        for file in files:
            # Игнорируем системные файлы типа .DS_Store
            if file == '.DS_Store':
                continue

            local_path = os.path.join(root, file)
            # Относительный путь для S3
            s3_key = os.path.relpath(local_path, dist_dir)
            
            # На Windows пути могут быть с обратным слэшем, заменяем на прямой
            s3_key = s3_key.replace('\\', '/')

            # Определяем MIME-тип
            content_type, _ = mimetypes.guess_type(local_path)
            if not content_type:
                if file.endswith('.html'):
                    content_type = 'text/html; charset=utf-8'
                elif file.endswith('.css'):
                    content_type = 'text/css'
                elif file.endswith('.js'):
                    content_type = 'application/javascript'
                else:
                    content_type = 'application/octet-stream'
            
            # Для HTML файлов принудительно ставим кодировку utf-8
            if content_type == 'text/html':
                content_type = 'text/html; charset=utf-8'

            print(f"Загрузка {local_path} -> {s3_key} ({content_type})...")
            
            try:
                s3_client.upload_file(
                    local_path,
                    BUCKET_NAME,
                    s3_key,
                    ExtraArgs={
                        'ContentType': content_type,
                        'ACL': 'public-read' # По умолчанию делаем публичными для раздачи сайта
                    }
                )
                uploaded_keys.add(s3_key)
            except Exception as e:
                print(f"Ошибка при загрузке {s3_key}: {e}")

    if not uploaded_keys:
        print("Ошибка: ни один файл не загружен. Удаление пропущено.")
        return

    # Удаляем файлы, которых больше нет в dist (аналог --delete)
    keys_to_delete = existing_keys - uploaded_keys
    if keys_to_delete:
        print(f"Удаление устаревших файлов ({len(keys_to_delete)} шт.)...")
        for key in keys_to_delete:
            print(f"Удаление {key}...")
            try:
                s3_client.delete_object(Bucket=BUCKET_NAME, Key=key)
            except Exception as e:
                print(f"Ошибка при удалении {key}: {e}")

    print("\nДеплой успешно завершен!")

if __name__ == '__main__':
    deploy()
