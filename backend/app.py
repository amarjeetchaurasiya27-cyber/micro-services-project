from flask import Flask, jsonify
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app) 

@app.route('/')
def home():
    return jsonify(message="Hello Amarjeet! 3-Tier Project ka Backend sahi chal raha hai. 🚀")

@app.route('/db-status')
def status():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'db'),
            database=os.getenv('DB_NAME', 'devops_db'),
            user=os.getenv('DB_USER', 'amarjeet'),
            password=os.getenv('DB_PASS', 'password123')
        )
        return jsonify(db_status="Database Connected! ✅")
    except Exception as e:
        return jsonify(db_status="Database Connection Failed ❌", error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)