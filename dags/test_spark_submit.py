import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta
from airflow.models import Connection
from airflow import settings

import csv
import requests
import json

default_args = {
    "owner": "Airflow",
    "start_date": airflow.utils.dates.days_ago(1),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}


def create_spark_new_conn(conn_name):
    conn = Connection(conn_id=f'{conn_name}',
                          conn_type="spark",
                          host="local",
                          extra='{"deploy-mode":"client"}')
    session = settings.Session()
    conn_name = session.query(Connection).filter(Connection.conn_id == conn.conn_id).first()
    if str(conn_name) == str(conn.conn_id):
        print(f"Connection {conn.conn_id} already exists")
        return None

    session.add(conn)
    session.commit()
    print(f'Connection {conn_name} is created')
    return conn


with DAG(dag_id="test_spark_submit", schedule_interval="@once", default_args=default_args, catchup=False) as dag:
    create_spark_new_conn = PythonOperator(
        task_id="create_spark_new_conn",
        python_callable=create_spark_new_conn,
        op_kwargs={"conn_name": 'my_sample_spark_conn1'}

    )

    # Running Spark Job to process the data
    spark_submit_task = SparkSubmitOperator(
        task_id="spark_submit_task",
        conn_id="my_spark_conn",
        application="/home/shvardhan/airflow/dags/scripts/mysparkcode.py",
        verbose=False
    )

create_spark_new_conn >> spark_submit_task
