[![Python CI](https://github.com/Temalllytera/python-project-52/actions/workflows/main.yml/badge.svg)](https://github.com/Temalllytera/python-project-52/actions/workflows/main.yml)

##Деплой

Приложение доступно по адресу: https://python-project-52-9w5j.onrender.com

## Отслеживание ошибок

В проекте подключён коллектор ошибок [Bugsink](https://www.bugsink.com/)
через `sentry-sdk`. Необработанные исключения в продакшене автоматически
отправляются в сервис вместе со стектрейсом и контекстом запроса.

Сбор ошибок включается только при заданной переменной `SENTRY_DSN`.
В локальной разработке она не задаётся, поэтому события никуда не уходят.

## Переменные окружения

| Переменная | Обязательна | Назначение |
|---|---|---|
| `SECRET_KEY` | да | ключ Django для криптоподписи |
| `DEBUG` | нет | режим отладки, в продакшене `False` |
| `ALLOWED_HOSTS` | нет | разрешённые хосты через запятую |
| `DATABASE_URL` | нет | подключение к БД, по умолчанию SQLite |
| `SENTRY_DSN` | нет | DSN коллектора ошибок |

## Запуск локально

```bash
git clone https://github.com/Temalllytera/python-project-52.git
cd python-project-52
make install
make migrate
make start
```