from google.cloud.sql.connector import Connector
import sqlalchemy, pymysql
import os

connector = Connector()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./key.json"

def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "idyllic-now-333714:europe-west3:mysql-projects",
        "pymysql",
        user="root",
        password="NieInterere123",
        db="twitter"
    )
    return conn

pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)
print(pool.connect())