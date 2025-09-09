import os
import pandas as pd
import connectorx as cx

conn_string = f"""oracle://{os.environ["ORACLE_DB_USER"]}:{os.environ["ORACLE_DB_PASSWORD"]}@{os.environ["ORACLE_DB_HOST"]}:{os.environ["ORACLE_DB_PORT"]}/?service_name={os.environ["ORACLE_DB_SERVICE_NAME"]}"""
res = cx.read_sql(conn_string, f"SELECT * FROM {os.environ['ORACLE_DB_TABLE_NAME']}")

print("Fetched data using connectorx:")
print(res)
