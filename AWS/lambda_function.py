import os
import logging
import requests
import pandas as pd
from datetime import datetime
from elasticsearch import Elasticsearch, helpers

def lambda_handler(event, context):
    logging.basicConfig(level=logging.INFO)
    logging.info('Lambda function execution started.')

    index_name = "python-aws"
    es = connect_to_elastic()
    last_update_date = updated_last(es, index_name)
    response = connect_to_nasa(last_update_date)
    df = create_df(response)

    try:
        update_new_data(df, es, last_update_date, index_name)
        last_update_date = updated_last(es, index_name)
        logging.info(f'Updated last date: {last_update_date}')
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def connect_to_elastic():
    elastic_cloud_id = os.getenv("ELASTIC_CLOUD_ID")
    elastic_api_key = os.getenv("ELASTIC_API_KEY")
    return Elasticsearch(cloud_id=elastic_cloud_id, api_key=elastic_api_key)

def connect_to_nasa(last_update_date):
    url = "https://api.nasa.gov/neo/rest/v1/feed"
    nasa_api_key = os.getenv("NASA_API_KEY")
    params = {
        "api_key": nasa_api_key,
        "start_date": last_update_date,
        "end_date": datetime.now(),
    }
    response = requests.get(url, params)
    logging.info(f"NASA API Response: {response.status_code}, {response.text}")
    return response.json()

def create_df(response):
    all_objects = []
    for date, objects in response["near_earth_objects"].items():
        for obj in objects:
            obj["close_approach_date"] = date
            all_objects.append(obj)
    df = pd.json_normalize(all_objects)
    df.drop(["close_approach_data", "links.self"], axis=1)
    if df.isnull().values.any() == True:
        df.fillna(0, inplace=True)
    return df

def doc_generator(df, index_name):
    for index, document in df.iterrows():
        yield {
            "_index": index_name,
            "_id": f"{document['id']}",
            "_source": document.to_dict(),
        }

def updated_last(es, index_name):
    query = {
        "size": 0,
        "aggs": {"last_date": {"max": {"field": "close_approach_date"}}},
    }
    response = es.search(index=index_name, body=query)
    last_updated_date_string = response["aggregations"]["last_date"]["value_as_string"]
    datetime_obj = datetime.strptime(last_updated_date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return datetime_obj.strftime("%Y-%m-%d")

def update_new_data(df, es, last_update_date, index_name):
    if isinstance(last_update_date, str):
        last_update_date = datetime.strptime(last_update_date, "%Y-%m-%d")

    last_update_date = pd.Timestamp(last_update_date).normalize()
    today = pd.Timestamp(datetime.now().date()).normalize()

    if not df.empty:
        df["close_approach_date"] = pd.to_datetime(df["close_approach_date"])
        update_range = df.loc[(df["close_approach_date"] > last_update_date) & (df["close_approach_date"] < today)]
        if not update_range.empty:
            helpers.bulk(es, doc_generator(update_range, index_name))
            logging.info("Data updated.")
        else:
            logging.info("No new data to update.")
    else:
        logging.info("The DataFrame is empty or None.")
