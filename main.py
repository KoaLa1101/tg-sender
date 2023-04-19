import configparser
import requests
from flask import Flask
from telegram import Bot
import tabulate

app = Flask(__name__)

json_format_sql = " FORMAT JSON "

# Чтение конфигурационного файла
config = configparser.ConfigParser()
config.read('app_config/config.ini')

# Инициализация телеграм бота
bot = Bot(token=config['telegram']['token'])
chat_id = config['telegram']['chat_id']

# Инициализация клиента ClickHouse
clickhouse_host = config['clickhouse']['host']
clickhouse_port = config['clickhouse']['port']
clickhouse_user = config['clickhouse']['user']
clickhouse_password = config['clickhouse']['password']
clickhouse_database = config['clickhouse']['database']
clickhouse_url = f'http://{clickhouse_user}:{clickhouse_password}@{clickhouse_host}:{clickhouse_port}/?database={clickhouse_database}'


def result_to_table(result, header):
    table_data = [list(item.values()) for item in result]
    return tabulate.tabulate(table_data, headers=header, tablefmt='pipe')


def execute_queries():
    with open('app_config/queries.sql', 'r') as f:
        queries = f.read().split('\n')
        results = []
        for query in queries:
            if query.strip():
                response = requests.post(clickhouse_url, data=query.split(';')[1].strip() + json_format_sql)
                response.raise_for_status()
                result_json = response.json()
                header = result_json['meta']
                header = [x['name'] for x in header]
                table = result_to_table(result_json['data'], header)
                result ='🕘 * Статистика за 24 часа * 🕘' + '\n🔉 *' + query.split(';')[0].strip().strip("'") + '* 🔉' + '\n' + '`' + table + '`'
                print(result)
                results.append(result)
    return results


@app.route('/send', methods=['GET'])
def send_to_telegram():
    results = execute_queries()
    for result in results:
        bot.send_message(chat_id=chat_id, text=str(result), parse_mode='MarkdownV2')
    return "Messages sent."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9438)
