from time import time

from pytest_bdd import scenario, given, when, then, parsers
import pytest

from methods.ftp_methods import *

# Constants
FILES_LIST = list()
STATUS = ''
DOWNLOAD_TIME = 0


@pytest.mark.parametrize('file_name', [
    # '1000GB.zip', '100GB.zip', '50GB.zip',
    # '10GB.zip', '1GB.zip', '500MB.zip',
    # '200MB.zip', '100MB.zip', '50MB.zip',
    '20MB.zip', '10MB.zip', '5MB.zip',
    # '3MB.zip', '2MB.zip', '1MB.zip',
    # '512KB.zip', '100KB.zip', '1KB.zip',
])
@scenario('TS0001_Test_FTP.feature', 'Test download files')
def test_ftp_download(file_name):
    pass


@given("I have connect to ftp server")
def connect(connect_to_ftp):
    return connect_to_ftp


@given(parsers.parse("I have the directory - {download}"))
def create_download_dir(download):
    full_dir = get_download_dir(dir_name=download)
    return full_dir


@when("I download <file_name> from ftp server")
def download_file_from_ftp(connect, create_download_dir, file_name):
    download_file(connect, create_download_dir, file_name)


@when("I get the files list from ftp server")
def get_files_list_ftp(connect):
    global FILES_LIST
    FILES_LIST = connect.nlst()


@then("<file_name> exists in the download directory")
def file_should_be_in_download_dir(file_name, create_download_dir):
    file_path = get_download_dir('download', file_name)
    assert check_exist_file(file_path), 'File does not exist in download directory'


@then("<file_name> still exists on the ftp server")
def file_should_be_on_ftp(file_name):
    assert file_name in FILES_LIST, 'File does not exist on ftp server after download'


@then("the size of <file_name> in the download dir is equal to the size of file on the server")
def file_size_should_be_equal(connect, file_name, create_download_dir):
    ftp_file_size = connect.size(file_name)
    download_file_size = get_file_size(create_download_dir, file_name)
    assert ftp_file_size == download_file_size, f'File sizes are different. ' \
                                                f'Downloaded {download_file_size} bytes, but on server {ftp_file_size}'


# Test 2
@scenario('TS0001_Test_FTP.feature', 'Delete file on ftp')
def test_ftp_file_delete():
    pass


@given("I have the files list from ftp")
def get_files_list_ftp_server(connect):
    return connect.nlst()


@when("I try delete file on ftp server")
def delete_file_on_ftp(connect, get_files_list_ftp_server):
    try:
        file_name = get_random_file_name(get_files_list_ftp_server)
        global STATUS
        STATUS = connect.delete(file_name)
    except Exception as err:
        STATUS = str(err)


@then(parsers.parse("I get a {status} - permission denied"))
def step_impl(status):
    global STATUS
    assert status in STATUS, f'Server returned an unexpected status: {STATUS}. Expected: {status} - permission denied'


# Test 3
@pytest.mark.parametrize('size,file_name', [(1024, 'test_1MB.zip'),
                                            # (102400, 'test_10MB.zip')
                                            ])
@scenario('TS0001_Test_FTP.feature', 'Upload file to ftp')
def test_upload_file_on_ftp(size, file_name):
    pass


@given("I have file for upload")
def create_file_for_upload(size, file_name):
    path_file = create_file(file_name, size)
    return path_file


@given("directory - upload on ftp")
def open_upload_dir_on_ftp(connect):
    connect.cwd('upload')
    return connect


@when("I upload file on ftp")
def step_impl(open_upload_dir_on_ftp, create_file_for_upload):
    global STATUS
    STATUS = upload_file(open_upload_dir_on_ftp, create_file_for_upload)


@then(parsers.parse("I have successful status - {answer}"))
def status_should_be_success(answer):
    global STATUS
    assert answer in STATUS, f'Expected successful status {answer} from ftp server. Actual: {STATUS}'


@then("file not exists on ftp directory")
def file_should_not_be_on_ftp(open_upload_dir_on_ftp, create_file_for_upload):
    global FILES_LIST
    FILES_LIST = open_upload_dir_on_ftp.nlst()
    file_name = get_file_name_from_path(create_file_for_upload)
    assert file_name not in FILES_LIST, f'The file - {file_name} is present on the ftp server, Expected that not be'


# Test 4
@pytest.mark.parametrize('file_name', [
    # '1000GB.zip', '100GB.zip', '50GB.zip',
    # '10GB.zip', '1GB.zip', '500MB.zip',
    # '200MB.zip', '100MB.zip', '50MB.zip',
    '20MB.zip', '10MB.zip', '5MB.zip',
    # '3MB.zip', '2MB.zip', '1MB.zip',
    # '512KB.zip', '100KB.zip', '1KB.zip',
])
@scenario('TS0001_Test_FTP.feature', 'Test download speed')
def test_download_speed(file_name):
    pass


@when("I download file")
def get_download_time(connect, create_download_dir, file_name):
    start = time()
    download_file_from_ftp(connect, create_download_dir, file_name)
    global DOWNLOAD_TIME
    DOWNLOAD_TIME = int(time() - start)


@then(parsers.parse("download speed not smaller than {time_} sec"))
def download_time_should_be_more(time_):
    assert int(time_) > DOWNLOAD_TIME, f'Loading time is too long: {DOWNLOAD_TIME}. Expected not more {time}'
