## Описание проекта

Вторая версия реализации проекта по автоматизации тестирования API ресурса restful-booker.

Restful-booker - открытое API для тренировки работы с запросами.

[Ссылка на документацию API restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html) 

____

## Установка проекта

- Скачать репозиторий на свою машину:

```
git clone https://github.com/LesyaLesya/python_testing_api_restful_booker_v2.git
```

- Перейти в директорию скачанного репозитория

- Установить и активировать виртуальное окружение (для запуска тестов через консоль/ide)

```
python3 -m venv venv
source venv/bin/activate
```
- Обновить PIP и установить зависимости (для запуска тестов через консоль/ide)

```
pip install -U pip
pip install -r requirements.txt
```

- Выбрать интерпретатор для проекта (для запуска тестов через консоль/ide)
____

## Запуск тестов

### __В IDE PyCharm__

#### Запустить тесты в PyCharm 

В Terminal выполнить команду:

```
pytest -n 2 -m marker tests/
```
где:

- -n - во сколько потоков запускать тесты, если не указывать параметр при запуске - тесты будут запущены в 1 поток.
- -m - маркер, какую группу тестов запускать.
Дополнительные параметры (см. config.yml):
- --schema=http|https - по-умолчанию https
- --host - по-умолчанию default (restful-booker.herokuapp.com)
- --user - - по-умолчанию admin


#### Получить отчет Allure 

- В Terminal выполнить команду, в качестве параметра указав путь до исполняемого файла allure на вашей машине:

```
./run_allure_report.sh /path/to/allure/bin
Пример: ./run_allure_report.sh /Applications/allure/bin/allure
```
