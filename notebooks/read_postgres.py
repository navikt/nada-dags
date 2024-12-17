import os

from google.cloud.sql.connector import Connector
import pg8000
import pandas as pd
import sqlalchemy

instance_connection_name = "nada-dev-db2e:europe-north1:nada-backend"
db_iam_user = os.environ["CLOUDSQL_DB_IAM_USER"]
db_name = "nada"

connector = Connector()

def getconn() -> pg8000.dbapi.Connection:
    conn: pg8000.dbapi.Connection = connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_iam_user,
        db=db_name,
        enable_iam_auth=True,
    )
    return conn

engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn)

query = "SELECT * FROM dashboards"
df = pd.read_sql_query(query, engine)

print(df)
