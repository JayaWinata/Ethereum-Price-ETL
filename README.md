# Ethereum Price ETL Project

##   Overview

This project is an Ethereum Price ETL pipeline built using Apache Airflow and Astronomer. It automatically extracts Ethereum (ETH) price data from an API, transforms the data into a structured format, and loads it into a PostgreSQL database for future analysis. The project demonstrates a real-world ETL workflow designed for cryptocurrency data collection and management.

## Key Features

- Automated ETL Pipeline: Fully automated using Airflow DAGs and tasks.
- Scheduled Data Fetching: Periodic extraction of Ethereum prices.
- Data Transformation: Cleans and formats raw API responses.
- Data Loading: Inserts the transformed data into a PostgreSQL database.
- Extensible Architecture: Easily extendable for more cryptocurrencies or other datasets.

## Tech Stack

- **Apache Airflow**: For orchestrating the ETL process.
- **Astronomer**: For deploying and managing Airflow environments.
- **Python**: Core language for DAGs and task development.
- **PostgreSQL**: Database to store the extracted and transformed Ethereum price data.
- **Docker**: (via Astronomer) to containerize the Airflow environment.
- **API Source**: Public endpoint providing Ethereum price data (Tiingo API).

## Key Steps

1. **Extraction**
    - Use an HttpOperator to fetch Ethereum price data from the API.

2. **Transformation**
    - Parse and clean the API response.
    - Extract fields such as open, high, low, close, volume, and trades.
    - Structure data into a format suitable for database insertion.

3. Loading
    - Insert the transformed data into a PostgreSQL database using Airflow's PostgresHook.

4. Orchestration
    - A single Airflow DAG defines the full workflow.
    - Tasks are organized sequentially: Extract -> Transform -> Load.

## Project Limitations

- Single Ticker: Only Ethereum (ETH/USD) is processed.
- Simple Transformation: No complex data cleaning or validation.
- Small Scale: Designed for educational or small project purposes, not yet production-ready.

## Conclusion

This project provides a solid foundation for understanding how to use Apache Airflow and Astronomer to build an ETL pipeline for financial or cryptocurrency data. It showcases end-to-end workflow automation, from data extraction to loading into a database. Although limited in scope, it can be easily scaled and enhanced with more sophisticated features like multi-asset support, retry mechanisms, and data validation checks, making it a great starting point for more complex ETL projects.
