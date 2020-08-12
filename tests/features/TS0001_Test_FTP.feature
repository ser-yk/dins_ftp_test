# Created by Sergey Yakshin at 11.08.2020
Feature: T0001_Test_load_file
  # Enter feature description here

  Background:
    Given I have connect to ftp server

  Scenario: Test download files
    Given I have directory - download
    When I download <file_name> from ftp server
    And I get the files list from ftp server
    Then <file_name> exists in download directory
    And <file_name> still exists on ftp server
#    check size

  Scenario: Delete file on ftp
    Given I have the files list from ftp
    When I try delete file on ftp server
    Then I get a 550 - permission denied

  Scenario: Upload file to ftp
    Given I have file for upload
    And directory - upload on ftp
    When I upload file on ftp
    And I get the files list from ftp server
    Then I have status success status - 250
    And file not exists on ftp directory

  Scenario: Test download speed
    Given I have directory - download
    When I download file
    Then download speed not smaller than 20 sec