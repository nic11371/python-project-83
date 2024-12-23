<div align="center">
  <h1>Анализатор страниц</h1>
</div>

WEB-приложение проверяет страницы сайтов по ссылке URL на SEO пригодность. Каждая страница сайта добавляется в таблицу проверок на SEO при удачном запросе с нашего сервиса.
Если страницы не существует, ошибка запроса или неправильная валидация страница проверку не пройдет.


#### Прохождение валидации

1. Длина URL ссылки не должна превышать 255 символов
2. URL адрес должен быть формата https://domen2.domen1
3. Нельзя добавить ссылки две одинааковые ссылки для проверки

***Можно указывать параметры в URL адресе - ссылки нормализуются до формата в пункте 2.***


## Иструкция по установке

1. Для начала необходимо [установить окружение.](https://ru.hexlet.io/courses/python-setup-environment/lessons/venv/theory_unit)
2. Далее [установить poetry.](https://python-poetry.org/docs/#installing-with-pipx)
3. Перейти в директорию `python-project-83` и ввести `poetry install`. Данная команда создаст виртуальное окружение в текущей директории.
4. Далее нужно собрать пакет командой `make biuld`. ***!Неоходимо находиться в директории python-project, т.к. в ней есть Makefile. Все make команды будут работать только там.***
6. Установить gunicorn.
7. Для установки приложения из пакетов ввести `make package-install`. Приложение установлено и готово к использованию.


## Запуск приложения

1. Для запуска приложения на локальной машине введите команду make dev.
2. Для запуска приложения на продакшн перейдите по ссылке https://python-project-83-2q23.onrender.com .


### Hexlet tests and linter status:
[![Actions Status](https://github.com/nic11371/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/nic11371/python-project-83/actions)
[![main](https://github.com/nic11371/python-project-83/actions/workflows/main.yml/badge.svg)](https://github.com/nic11371/python-project-83/actions/workflows/main.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/561f99c96f7cea662dd4/maintainability)](https://codeclimate.com/github/nic11371/python-project-83/maintainability)
