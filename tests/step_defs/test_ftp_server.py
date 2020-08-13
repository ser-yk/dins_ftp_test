from time import time
from pathlib import Path

from pytest_bdd import scenario, given, when, then, parsers
import pytest

from methods.ftp_methods import download_file, upload_file, get_file_size, create_dir, get_random_file_name
from methods.ftp_methods import get_file_size_as_string, create_file

# Constants
file_list_global = list()
status_global = ''
download_file_global = 0


@given("I have connect to ftp server")
def connect(connect_to_ftp):
    return connect_to_ftp


# Test 1
@scenario('TS0001_Test_FTP.feature', 'Check that the file are present on the FTP server')
def test_file_are_present_on_ftp():
    pass


@given("the actual size of <file_name> on ftp server")
def get_actual_file_size_on_ftp(connect, file_name):
    ftp_file_size = connect.size(file_name)
    return ftp_file_size


@when("I get the files list from ftp server")
def get_files_list_ftp(connect):
    global file_list_global
    file_list_global = connect.nlst()


@then("<file_name> exists on the ftp server")
def file_should_be_on_ftp(file_name):
    global file_list_global
    assert file_name in file_list_global, 'File does not exist on ftp server'


@then("<file_name> and actual size are the same")
def compare_actual_file_size_and_file_name(file_name, get_actual_file_size_on_ftp):
    string_size_file = get_file_size_as_string(get_actual_file_size_on_ftp, file_name)
    assert string_size_file in file_name, f'File name and actual size are not the same, actual - {string_size_file}'


# Test 2
@scenario('TS0001_Test_FTP.feature', 'Test download files')
def test_download_download():
    pass


@given(parsers.parse("I have the directory - {download}"))
def create_download_dir(download):
    full_dir = create_dir(dir_name=download)
    return full_dir


@when("I download <file_name> from ftp server")
def download_file_from_ftp(connect, create_download_dir, file_name):
    download_file(connect, create_download_dir, file_name)


@then("<file_name> exists in the download directory")
def file_should_be_in_download_dir(file_name, create_download_dir):
    file_path = create_dir('download', file_name)
    assert Path(file_path).stat().st_size, 'File does not exist in download directory'


@then("the size of <file_name> in the download dir is equal to the size of file on the server")
def file_size_should_be_equal(connect, file_name, create_download_dir):
    ftp_file_size = connect.size(file_name)
    download_file_size = get_file_size(create_download_dir, file_name)
    assert ftp_file_size == download_file_size, f'File sizes are different. ' \
                                                f'Downloaded {download_file_size} bytes, but on server {ftp_file_size}'


# Test 3
@scenario('TS0001_Test_FTP.feature', 'Delete file on ftp server')
def test_ftp_file_delete():
    pass


@given("I have the files list from ftp")
def get_files_list_ftp_server(connect):
    return connect.nlst()


@when("I try delete file on ftp server")
def delete_file_on_ftp(connect, get_files_list_ftp_server):
    try:
        file_name = get_random_file_name(get_files_list_ftp_server)
        global status_global
        status_global = connect.delete(file_name)
    except Exception as err:
        status_global = str(err)


@then(parsers.parse("I get a {status} - permission denied"))
def step_impl(status):
    global status_global
    assert status in status_global, f'Server returned an unexpected status: {status_global}. ' \
                                    f'Expected: {status} - permission denied'


# Test 4
@scenario('TS0001_Test_FTP.feature', 'Upload file to ftp server')
def test_upload_file_on_ftp():
    pass


@given("I have <file_name> <size> KB for upload")
def create_file_for_upload(file_name, size):
    path_file = create_file(file_name, int(size))
    return path_file


@given("directory - upload on ftp")
def open_upload_dir_on_ftp(connect):
    connect.cwd('upload')
    return connect


@when("I upload file on ftp")
def step_impl(open_upload_dir_on_ftp, create_file_for_upload):
    global status_global
    status_global = upload_file(open_upload_dir_on_ftp, create_file_for_upload)


@then(parsers.parse("I have successful status - {ftp_answer} from ftp server"))
def status_should_be_success(ftp_answer):
    global status_global
    assert ftp_answer in status_global, f'Expected successful status {ftp_answer} Transfer complete. Actual: {status_global}'


@then("file not exists on ftp directory after loading")
def file_should_not_be_on_ftp(open_upload_dir_on_ftp, create_file_for_upload):
    global file_list_global
    file_list_global = open_upload_dir_on_ftp.nlst()
    file_name = create_file_for_upload.split('\\')[-1]
    assert file_name not in file_list_global, f'The file - {file_name} is present on the ftp server, Expected that not be'


# Test 5
@scenario('TS0001_Test_FTP.feature', 'Test download time')
def test_download_time():
    pass


@when("I download <file_name>")
def get_download_time(connect, create_download_dir, file_name):
    start = time()
    download_file_from_ftp(connect, create_download_dir, file_name)
    global download_file_global
    download_file_global = int(time() - start)


@then("download time not smaller than <expected_time> sec")
def download_time_should_be_more(expected_time):
    assert int(expected_time) > download_file_global, f'Loading time is too long: {download_file_global}. ' \
                                               f'Expected not more {expected_time}'
