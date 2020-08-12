import pytest
from ftplib import FTP
from pathlib import Path
import shutil


@pytest.yield_fixture()
def connect_to_ftp():
    ftp = FTP('speedtest.tele2.net')
    ftp.login()
    yield ftp
    ftp.close()
    path_download = Path.cwd() / 'download'
    if path_download.exists():
        shutil.rmtree(str(path_download))
    path_upload = Path.cwd() / 'upload'
    if path_upload.exists():
        shutil.rmtree(str(path_upload))
