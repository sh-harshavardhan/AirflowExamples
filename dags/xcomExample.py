import datetime
import json
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator


def read_json_anothertime(**kwargs):
    ti = kwargs['ti']
    json_data = ti.xcom_pull(task_ids='get_remote_json')
    json_config = json.loads(json_data)
    print(json_config)
    print("id :: {} ".format(json_config["id"]))
    print(json_config["name"])


def read_json(**kwargs):
    ti = kwargs['ti']
    json_data = ti.xcom_pull(task_ids='get_remote_json')
    json_config = json.loads(json_data)
    print(json_config)


with DAG(
        dag_id='xcomExample',
        schedule_interval='@once',
        start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
        catchup=False,
        dagrun_timeout=datetime.timedelta(minutes=60),
) as dag:
    get_remote_json = BashOperator(
        task_id='get_remote_json',
        bash_command="cat /home/shvardhan/myconfig.json",
        do_xcom_push=True,
        dag=dag)

    load_json_to_dict = PythonOperator(
        task_id='load_json',
        python_callable=read_json,
    )

    read_json_anothertime = PythonOperator(
        task_id='read_json_anothertime',
        python_callable=read_json_anothertime,
    )

    get_remote_json >> load_json_to_dict >> read_json_anothertime
