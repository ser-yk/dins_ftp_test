

@pytest.mark.parametrize('file_name', [
    '1000GB.zip',
    '100GB.zip',
    '50GB.zip',
    '10GB.zip',
    '1GB.zip',
    '500MB.zip',
    '200MB.zip',
    '100MB.zip',
    '50MB.zip',
    '20MB.zip',
    '10MB.zip',
    '5MB.zip',
    '3MB.zip',
    '2MB.zip',
    '1MB.zip',
    '512KB.zip',
    '100KB.zip',
    '1KB.zip',
])
def load_file_from_ftp(self, ftp):
    pass

def test_ftp():
    pass


def connect_to_ftp(ftp_connect):
    try:
        file_name = download_file_from_ftp(ftp_connect, file_name)
        return file_name
    except Exception as err:
        assert False, err


def download_file(ftp_connect, file_name):
    pass


def file_should_exists(download_file):
    assert check_exist_file(download_file), f'The downloaded file was not found in the directory: {download_file}'


def file_size_should_right(download_file, size):
    file_size = get_file_size(download_file)
    assert file_size in size, f'The file size is not equal to the declared size in the file name.' \
                              f'Expected: {size}, actual: {file_size}'

