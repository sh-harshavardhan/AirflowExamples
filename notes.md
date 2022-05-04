https://www.hackerxone.com/2021/10/15/steps-to-install-and-setup-apache-airflow-on-ubuntu-20-04-lts/

sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository universe

sudo apt-get install python-setuptools
sudo apt install python3-pip

sudo apt-get install libmysqlclient-dev
sudo apt-get install libssl-dev
sudo apt-get install libkrb5-dev

sudo apt install python3-virtualenv
virtualenv airflow_example

cd airflow_example/bin/
source activate

export AIRFLOW_HOME=~/airflow
pip3 install apache-airflow
pip3 install typing_extensions

airflow db init

airflow users create --username admin --firstname admin --lastname testing --role Admin --email admin@domain.com

kill -9 `cat /home/shvardhan/airflow/airflow-webserver.pid`
kill -9 `cat /home/shvardhan/airflow/airflow-scheduler.pid`
rm -f /home/shvardhan/airflow/*.pid
airflow webserver -p 8080 -D
airflow scheduler -D