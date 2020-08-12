from ftplib import FTP
from pathlib import Path
from random import randint


def download_file(ftp: FTP, path: str, name: str) -> None:
    """
    Function to download files from FTP server
    @:param ftp: File Transfer Protocol Object
    @:param path: The path for save
    @:param name: The name of the file to download
    """
    out = Path(path) / name
    with open(str(out), 'wb') as f:
        ftp.retrbinary('RETR ' + name, f.write)


def upload_file(ftp: FTP, path: str, ftype: str = None):
    """
    Function for uploading files to FTP server
    @:param ftp: File Transfer Protocol Object
    @:param path: File path for download
    """
    try:
        file_name = path.split('\\')[-1]
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


def get_file_size(path: str, name: str) -> int:
    """
    The function determines the file size in bytes
    :param path: File path
    :param name: File name
    :return: File size in bytes
    """
    file_path = Path(path) / name
    size = int(file_path.stat().st_size)
    return size


def create_dir(dir_name: str, name='') -> str:
    """
    The function creates the specified directory.
    And returns it as a string if a filename is specified,
    then it will be included in the string.
    :param dir_name: Directory to create
    :param name: File name
    :return: Full path in string
    """
    out = Path.cwd() / dir_name
    out.mkdir(parents=True, exist_ok=True)
    if name:
        out = out / name
    return str(out)


def get_random_file_name(files: list) -> str:
    """
    The function randomly selects a file by name from the list
    :param files: Files list
    :return: Selected file name
    """
    while True:
        i = randint(0, len(files) - 1)
        f = files[i]
        if '.' in f:
            break
    return f


def create_file(name: str, size_kb: int, dir_='upload') -> str:
    """
    The function creates a file of the specified size in the specified directory
    :param name: File name
    :param size_kb: File size in KB
    :param dir: File path for file
    :return:
    """
    out = create_dir(dir_, name)
    with open(out, "wb") as f:
        f.truncate(1024 * size_kb)
    return out
