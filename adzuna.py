import dlt
import os
import requests

@dlt.resource(
        table_name="adzuna", 
        write_disposition="merge", 
        primary_key='id', 
        columns={"location": {"data_type": "complex"}}
        )
def get_jobs(APP_ID, APP_KEY):
    page_number = 1
    while True:
        params = {
            'app_id': APP_ID, 
            'app_key': APP_KEY, 
            'results_per_page': 1000, 
            'what': 'data engineer', 
            'max_days_old': 7
            }
        url = f"https://api.adzuna.com/v1/api/jobs/au/search/{page_number}"
        response = requests.get(url, params)
        response.raise_for_status()
        if response.json()['results']:
            yield response.json()['results']
            page_number += 1
            continue
        break

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="adzuna",
        destination="bigquery",
        dataset_name="jobs"
    )
    APP_ID = os.environ['APP_ID']
    APP_KEY = os.environ['APP_KEY']
    print("APP_ID:", APP_ID)
    print("APP_KEY:", APP_KEY)
    print("Starting pipeline")
    load_info = pipeline.run(get_jobs(APP_ID, APP_KEY))
    print(load_info)