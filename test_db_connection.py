import yaml
import sqlalchemy
from sqlalchemy import text
import random

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


# Create a new database connector instance
new_connector = AWSDBConnector()

# Verify the connection by fetching a single random row from the database
def verify_db_connection():
    random_row = random.randint(0, 11000)
    engine = new_connector.create_db_connector()

    with engine.connect() as connection:
        pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
        pin_selected_row = connection.execute(pin_string)
        
        for row in pin_selected_row:
            pin_result = dict(row._mapping)

        print("Connection successful! Here's a sample row from pinterest_data:")
        print(pin_result)


if __name__ == "__main__":
    verify_db_connection()