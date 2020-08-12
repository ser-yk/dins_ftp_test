from ftplib import FTP
from pathlib import Path
from random import randint
import os


def download_file(ftp: FTP, path: str, name: str) -> None:
    """
    Функция для загрузки файлов с FTP-сервера
    @param ftp: Объект протокола передачи файлов
    @param name: Имя файла, который нужно скачать
    """
    out = Path(path) / name
    with open(str(out), 'wb') as f:
        ftp.retrbinary('RETR ' + name, f.write)


def upload_file(ftp: FTP, path: str, ftype: str = None):
    """
    Функция для загрузки файлов на FTP-сервер
    @param ftp_obj: Объект протокола передачи файлов
    @param path: Путь к файлу для загрузки
    """
    try:
        file_name = get_file_name_from_path(path)
        if ftype == 'TXT':
            with open(path) as f:
                status = ftp.storlines('STOR ' + file_name, f)
        else:
            with open(path, 'rb') as f:
                status = ftp.storbinary('STOR ' + file_name, f, 1024)
    except Exception as err:
        status = str(err)
    finally:
        return status


def get_file_size_as_string(path: str) -> str:
    q = Path(path)
    kb_size = int(q.stat().st_size / 1024)
    measure = path[-6:-4]
    if measure == 'KB':
        return str(kb_size) + 'KB'
    elif measure == 'MB':
        mb_size = int(kb_size / 1024)
        return str(mb_size) + 'MB'
    elif measure == 'GB':
        gb_size = int(kb_size / 1024 / 1024)
        return str(gb_size) + 'GB'


def get_file_size(path: str, name: str) -> int:
    file_path = Path(path) / name
    size = os.path.getsize(str(file_path))
    return size


def check_exist_file(path: str) -> bool:
    q = Path(path)
    return q.exists()


def get_file_name_from_path(path: str) -> str:
    file_name = path.split('\\')[-1]
    return file_name


def get_download_dir(dir_name: str, name='') -> str:
    out = Path.cwd() / dir_name
    out.mkdir(parents=True, exist_ok=True)
    if name:
        out = out / name
    return str(out)


def get_random_file_name(files: list) -> str:
    while True:
        i = randint(0, len(files) - 1)
        f = files[i]
        if '.' in f:
            break
    return f


def create_file(name: str, size_kb: int) -> str:
    out = get_download_dir('upload', name)
    with open(out, "wb") as f:
        f.truncate(1024 * size_kb)
    return out
