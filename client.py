import requests
import json
from time import sleep
from random import randint

class SQLiteClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def execute_query(self, query):
        url = f"{self.base_url}/execute"
        payload = json.dumps({"query": query})
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=payload)
        return response.json()

    def query_database(self, query):
        url = f"{self.base_url}/query"
        payload = json.dumps({"query": query})
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=payload)
        return response.json()

    def list_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        return self.query_database(query)

    def create_table(self, table_name, columns):
        columns_def = ", ".join(f"{col} {dtype}" for col, dtype in columns.items())
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def});"
        return self.execute_query(query)

    def list_records(self, table_name):
        query = f"SELECT * FROM {table_name};"
        return self.query_database(query)

    def filter_records(self, table_name, filter_condition):
        query = f"SELECT * FROM {table_name} WHERE {filter_condition};"
        return self.query_database(query)

def random_sleep():
    sleep(randint(1, 5))

# Example usage
if __name__ == "__main__":
    client = SQLiteClient("http://localhost:5000")
    print("Client connected to server")
    for _ in range(randint(1, 10 )):
        random_sleep()
        # Create table
        client.create_table("test", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
        random_sleep()
        # Insert data
        client.execute_query("INSERT INTO test (name) VALUES ('John Doe');")
        random_sleep()
        client.execute_query("INSERT INTO test (name) VALUES ('Jane Smith');")
        random_sleep()
        # List tables
        tables = client.list_tables()
        print("Tables:", tables)
        random_sleep()
        # List all records in a table
        records = client.list_records("test")
        print("Records:", records)
        random_sleep()
        # Filter records
        filtered_records = client.filter_records("test", "name = 'John Doe'")
        print("Filtered Records:", filtered_records)
        random_sleep()