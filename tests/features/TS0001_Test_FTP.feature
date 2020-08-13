# Created by Sergey Yakshin at 11.08.2020
Feature: T0001_Test_load_file
  FTP contains files for testing download speed, their set and sizes are fixed.
  You can upload files to the /upload folder to test the upload speed,
  files from this folder are deleted immediately after the upload is complete

  Background:
    Given I have connect to ftp server

  Scenario Outline: Check that the file are present on the FTP server
    Given the actual size of <file_name> on ftp server
    When I get the files list from ftp server
    Then <file_name> exists on the ftp server
    And <file_name> and actual size are the same
    Examples:
      | file_name  |
      | 1000GB.zip |
      | 100GB.zip  |
      | 50GB.zip   |
      | 10GB.zip   |
      | 1GB.zip    |
      | 500MB.zip  |
      | 200MB.zip  |
      | 100MB.zip  |
      | 50MB.zip   |
      | 20MB.zip   |
      | 10MB.zip   |
      | 5MB.zip    |
      | 3MB.zip    |
      | 2MB.zip    |
      | 1MB.zip    |
      | 512KB.zip  |
      | 100KB.zip  |
      | 1KB.zip    |

  Scenario Outline: Test download files
    Given I have the directory - download
    When I download <file_name> from ftp server
    And I get the files list from ftp server
    Then <file_name> exists in the download directory
    And <file_name> exists on the ftp server
    And the size of <file_name> in the download dir is equal to the size of file on the server
    Examples:
      | file_name |
      | 50MB.zip  |
      | 20MB.zip  |
      | 1MB.zip   |
      | 512KB.zip |
      | 100KB.zip |
      | 1KB.zip   |

  Scenario: Delete file on ftp server
    Given I have the files list from ftp
    When I try delete file on ftp server
    Then I get a 550 - permission denied

  Scenario Outline: Upload file to ftp server
    Given I have <file_name> <size> KB for upload
    And directory - upload on ftp
    When I upload file on ftp
    And I get the files list from ftp server
    Then I have successful status - 226 from ftp server
    And file not exists on ftp directory after loading
    Examples:
      | size   | file_name     |
      | 1024   | test_1MB.zip  |
      | 102400 | test_10MB.zip |

#    Just in case
  Scenario Outline: Test download time
    Given I have the directory - download
    When I download <file_name>
    Then download time not smaller than <expected_time> sec
    Examples:
      | file_name | expected_time |
      | 50MB.zip  | 20            |
      | 20MB.zip  | 10            |
      | 10MB.zip  | 5             |
