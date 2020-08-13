# test_ftp_server

## Задание
1.	Разработать тестовые сценарии.
2.	Написать автотесты на python (или другом языке, если python не знаком) 
для тестирования FTP сервера ftp://speedtest.tele2.net в соответствии с разработанными сценариями.
3.	Провести тестирование и написать отчет.

Описание функционала FTP сервера: - На FTP лежат файлы для тестирования скорости скачивания, 
их набор и размеры - фиксированы. - В папку /upload можно загружать файлы для тестирования скорости загрузки, 
файлы из этой папки удаляются сразу по завершении загрузки.


## Решение

#####Тесты написаны в стиле BDD с использованием pytest-6.0.1, pytest-bdd-3.4.0 и pytest-html-2.1.1

В тестовом наборе TS0001_Test_FTP.feature разработаны следующие сценарии:
* **Check that the file are present on the FTP server** - имея список файлов, 
в названии, которых указан размер, проверяем, что эти файлы есть на сервере, 
и что название соответствует фактическому размеру.
* **Test download files** - выборочно скачиваем файлы с сервера, проверяем, 
что их размер совпадает с файлом на сервере, проверяем, что после
скачивания файл всё также присутствует на сервере (не удалился).
* **Delete file on ftp server** - пробуем удалить случайный файл с сервера. 
Ожидаем, что сервер не даст нам этого сделать и выдаст ошибку.
* **Upload file to ftp server** - пробуем загрузить фал на сервер.
Ожидаем, что будет получен успешный статус о загрузке файла.
Файл после загрузки будет отсутствовать на сервере, т.к. то его удаляет.
* **Test download time** - тест проверяет, что файл заданного размера скачивается
за определённое время. Актуально если есть требования и мы знаем скорость
своего соединения.


**Отчет о тестировании** - сохраняется в папке 'reports' в .html формате

**Для запуска тестирования** - Необходимо установить все указанные выше пакеты,
в командной строке перейти в директорию \tests и выполнить команду pytest


#####Работа тестового скрипта проверена только на Windows

