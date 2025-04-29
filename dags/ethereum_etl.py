from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv('/secrets/tiingo.env')
TOKEN = os.getenv('TOKEN')

with DAG(
    dag_id='ethereum_price_etl',
    start_date=days_ago(2),
    schedule_interval='@weekly',
    catchup=False
) as dag:

    ## 1. Initialize / create table if it doesn't exist
    @task
    def create_table():
        ## Initialize the PostgresHook
        postgres_hook = PostgresHook(postgres_conn_id='postgres_connection')

        query = '''
            CREATE TABLE IF NOT EXISTS eth_price (
                id SERIAL PRIMARY KEY,
                date DATE,
                open_price REAL,
                high_price REAL,
                low_price REAL,
                close_price REAL,
                volume REAL,
                trades INT
            )
        '''

        postgres_hook.run(query)


    extract_price = SimpleHttpOperator(
        task_id='extract_eth_price',
        http_conn_id='tiingo_api',  # point to https://api.tiingo.com
        endpoint='tiingo/crypto/prices',  # Only the path
        method='GET',
        data={
            "tickers": "ethusd",
            "startDate": "{{ prev_ds }}",
            "resampleFreq": "1day"
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": "Token {{ conn.tiingo_api.extra_dejson.token }}"
        },
        response_filter=lambda response: response.json(),
        log_response=True,
    )

    @task
    def transform_eth_price_data(response):
        temp = response['priceData']
        eth_price_data = {
            "date": temp['date'],
            'open_price': temp['open'],
            'high_price': temp['high'],
            'low_price': temp['low'],
            'close_price': temp['close'],
            'volume': temp['volume'],
            'trades': temp['tradesDone']
        }

        return eth_price_data

    @task
    def load_data(eth_price_data):
        postgres_hook = PostgresHook(postgres_conn_id='postgres_connection')

        query = '''
            INSERT INTO eth_price (date, open_price, high_price, low_price, close_price, volume, trades)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''

        postgres_hook.run(query, parameters={
            eth_price_data['date'],
            eth_price_data['open_price'],
            eth_price_data['high_price'],
            eth_price_data['low_price'],
            eth_price_data['close_price'],
            eth_price_data['volume'],
            eth_price_data['trades']
        })

    ## Dependencies
    create_table() >> extract_price
    response = extract_price.output
    transformed_data = transform_eth_price_data(response)
    load_data(transformed_data)