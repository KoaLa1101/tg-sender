# tg-sender
_tg-sender_ - это сервис для отправки каких либо данных из clickhouse в чат telegram.

## Установка

Вы можете установить tg-sender с помощью Docker. Для этого выполните следующие команды:

```docker build -t tg-sender .
docker run -p 9438:9438 -v /path/to/config:/app/config tg-sender
```
## Использование
После установки tg-sender будет доступен по адресу http://localhost:9438/send.

## Изменение данных для отправки
Для изменения данных для отправки - необходимо в файле queries.sql прописать "<заголовок>;<YOUR_SQL>"

## Изменение хоста
Чтобы изменить хост, на котором работает ClickHouse, необходимо изменить файл config.ini. В этом файле указывается URL и порт ClickHouse.

## Лицензия
Нема

## Контакты
Если у вас есть какие-либо вопросы, вы можете связаться со мной @koala1101
но лучше никогда не писать. Сломал? чини сам!