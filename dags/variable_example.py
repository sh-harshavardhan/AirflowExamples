import datetime
import json
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable


def print_hello():
    print("print_hello")


def read_json():
    global json_config
    with open('/home/shvardhan/airflow/conf/config1.json') as json_fp:
        json_config = json.load(json_fp)
        for k, v in json_config.items():
            Variable.set(k, v)


read_json()

with DAG(
        dag_id='variable_example',
        schedule_interval='@once',
        start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
        catchup=False,
        dagrun_timeout=datetime.timedelta(minutes=60),
) as dag:
    print_hello = PythonOperator(
        task_id='print_hello',
        python_callable=print_hello,
    )

    get_variables = BashOperator(
        task_id='get_variables',
        # bash_command='echo Username : {} , Email : {}'.format(json_config.get("username"),
        #                                                       json_config.get("email")),
        bash_command='echo Username : {} , Email : {}'.format(Variable.get("username"),
                                                              Variable.get("email")),
    )

    print_hello >> get_variables
