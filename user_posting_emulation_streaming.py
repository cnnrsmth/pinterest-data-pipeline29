import requests
from time import sleep
import random
from multiprocessing import Process
import yaml
import boto3
import json
import sqlalchemy
from sqlalchemy import text


random.seed(100)


class AWSDBConnector:
    def __init__(self):
        # Read credentials from db_creds.yaml
        with open('db_creds.yaml', 'r') as file:
            creds = yaml.safe_load(file)
        self.HOST = creds['HOST']
        self.USER = creds['USER']
        self.PASSWORD = creds['PASSWORD']
        self.DATABASE = creds['DATABASE']
        self.PORT = creds['PORT']

    def create_db_connector(self):
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()

def send_data_to_kinesis():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            # Fetch data from Pinterest data table
            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            pin_result = None
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            # Fetch data from Geolocation data table
            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            geo_result = None
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            # Fetch data from User data table
            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            user_result = None
            for row in user_selected_row:
                user_result = dict(row._mapping)
            
            print(pin_result)
            print(geo_result)
            print(user_result)

            # Define the API invoke URLs for each stream
            invoke_url_pin = "https://9ni8b5q78h.execute-api.us-east-1.amazonaws.com/test/streams/streaming-0afffcc5e36f-pin/record"
            invoke_url_geo = "https://9ni8b5q78h.execute-api.us-east-1.amazonaws.com/test/streams/streaming-0afffcc5e36f-geo/record"
            invoke_url_user = "https://9ni8b5q78h.execute-api.us-east-1.amazonaws.com/test/streams/streaming-0afffcc5e36f-user/record"

            # Create the payloads for each stream with the updated structure
            pin_data = json.dumps({
                "StreamName": "streaming-0afffcc5e36f-pin",
                "Data": {
                    "index": pin_result["index"],
                    "unique_id": pin_result["unique_id"],
                    "title": pin_result["title"],
                    "description": pin_result["description"],
                    "poster_name": pin_result["poster_name"],
                    "follower_count": pin_result["follower_count"],
                    "tag_list": pin_result["tag_list"],
                    "is_image_or_video": pin_result["is_image_or_video"],
                    "image_src": pin_result["image_src"],
                    "downloaded": pin_result["downloaded"],
                    "save_location": pin_result["save_location"],
                    "category": pin_result["category"]
                },
                "PartitionKey": "test"
            })

            geo_data = json.dumps({
                "StreamName": "streaming-0afffcc5e36f-geo",
                "Data": {
                    "ind": geo_result["ind"],
                    "timestamp": str(geo_result["timestamp"]),
                    "latitude": geo_result["latitude"],
                    "longitude": geo_result["longitude"],
                    "country": geo_result["country"]
                },
                "PartitionKey": "test"
            })

            user_data = json.dumps({
                "StreamName": "streaming-0afffcc5e36f-user",
                "Data": {
                    "ind": user_result["ind"],
                    "first_name": user_result["first_name"],
                    "last_name": user_result["last_name"],
                    "age": user_result["age"],
                    "date_joined": str(user_result["date_joined"])
                },
                "PartitionKey": "test"
            })

            # Headers for the API request
            headers = {'Content-Type': 'application/json'}

            # Send the data to the API
            pin_response = requests.request("PUT", invoke_url_pin, headers=headers, data=pin_data)
            geo_response = requests.request("PUT", invoke_url_geo, headers=headers, data=geo_data)
            user_response = requests.request("PUT", invoke_url_user, headers=headers, data=user_data)

            # Print response status codes
            print(f"Pin response status code: {pin_response.status_code}")
            print(f"Geo response status code: {geo_response.status_code}")
            print(f"User response status code: {user_response.status_code}")

if __name__ == "__main__":
    send_data_to_kinesis()
    print('Working')