from flask import Flask, request, jsonify
import sqlite3
from queue import Queue
from threading import Thread, Lock

app = Flask(__name__)
db_lock = Lock()
request_queue = Queue()

def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

def worker():
    while True:
        func, args = request_queue.get()
        try:
            func(*args)
        finally:
            request_queue.task_done()

Thread(target=worker, daemon=True).start()

@app.route('/execute', methods=['POST'])
def execute_query():
    query = request.json['query']
    request_queue.put((handle_execute_query, (query,)))
    request_queue.join()
    return jsonify({"status": "success"}), 201

def handle_execute_query(query):
    with db_lock:
        conn = get_db_connection()
        conn.execute(query)
        conn.commit()
        conn.close()

@app.route('/query', methods=['POST'])
def query_database():
    query = request.json['query']
    request_queue.put((handle_query_database, (query,)))
    request_queue.join()
    result = request_queue.result
    return jsonify(result)

def handle_query_database(query):
    with db_lock:
        conn = get_db_connection()
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        conn.close()
    request_queue.result = [dict(row) for row in rows]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
