import sys
import airflow
from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

sys.path.insert(1, '/home/shvardhan/airflow/dags/scripts/')

from process_logs import process_logs_func


default_args = {
    "owner": "Airflow",
    "start_date": airflow.utils.dates.days_ago(1),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "youremail@host.com",
    "retries": 1
}

with DAG(dag_id="template_dag", schedule_interval="@daily", default_args=default_args) as dag:
    t0 = BashOperator(
        task_id="t0",
        # bash_command="echo {{ ds }}")
        ## Output : 2022-05-02
        # bash_command="echo {{ var.value.my_login }}")
        ## Output : my_login_value  ## only if you set variable my_login its value as my_login_value
        bash_command="echo {{ ts_nodash }} :: {{ macros.ds_format(ts_nodash, '%Y%m%dT%H%M%S', '%Y-%m-%d-%H-%M') }}")
        ## Output : INFO - 20220503T152853 :: 2022-05-03-15-28
    t3 = BashOperator(
        task_id="t3",
        bash_command="pwd")
    # t1 = BashOperator(
    #         task_id="generate_new_logs",
    #         bash_command="scripts/generate_new_logs.sh",
    #         params={'filename': 'log.csv'})

    t4 = PythonOperator(
           task_id="process_logs",
           python_callable=process_logs_func,
           provide_context=True,
           templates_dict={"log_dir" : "dags/scripts/"},
           params={'filename': 'log.csv'}
           )

    t3 >> t0 >> t4