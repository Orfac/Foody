import datetime as dt
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from foody_scraper.src.main import main

default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2020, 11, 22),
    'max_active_runs': 1
}

def parse():
    main()

def analyze():
    print("analyze")

with DAG('foody_parser',
         default_args=default_args, 
         schedule_interval='0 * * * *',
         ) as dag:

    t1 = PythonOperator(
        task_id='parse',
        python_callable=parse,
        dag=dag)

    t2 = PythonOperator(
        task_id='analyze',
        python_callable=analyze,
        dag=dag)

    t2.set_upstream(t1)