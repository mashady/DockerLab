from flask import Flask, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('DB_NAME', 'mydb')
DB_USER = os.environ.get('DB_USER', 'user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')

def get_db_connection():
    """Create a database connection to PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Could not connect to database: {e}")
        return None

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Flask PostgreSQL Demo</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    line-height: 1.6;
                }
                h1 {
                    color: #4285f4;
                }
                .status {
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }
                .success {
                    background-color: #d4edda;
                    color: #155724;
                }
                .error {
                    background-color: #f8d7da;
                    color: #721c24;
                }
            </style>
        </head>
        <body>
            <h1>Flask with PostgreSQL Docker Demo</h1>
            <div class="status success">
                <p>Web server is running successfully!</p>
            </div>
            <p>Check the database connection status: <a href="/db-status">Database Status</a></p>
        </body>
    </html>
    """

@app.route('/db-status')
def db_status():
    """Check database connection and return status"""
    conn = get_db_connection()
    
    if conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        
        cur.execute("INSERT INTO test_table (name) VALUES (%s)", ('Test entry',))
        conn.commit()
        
        cur.execute("SELECT * FROM test_table ORDER BY created_at DESC LIMIT 5")
        records = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return """
        <html>
            <head>
                <title>Database Status</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        line-height: 1.6;
                    }
                    h1 {
                        color: #4285f4;
                    }
                    .status {
                        padding: 10px;
                        border-radius: 5px;
                        margin-bottom: 20px;
                    }
                    .success {
                        background-color: #d4edda;
                        color: #155724;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }
                    th, td {
                        padding: 8px;
                        text-align: left;
                        border-bottom: 1px solid #ddd;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h1>Database Connection Status</h1>
                <div class="status success">
                    <p>Successfully connected to PostgreSQL database!</p>
                </div>
                <p>A test table was created and data was inserted successfully.</p>
                <p><a href="/">Return to home</a></p>
            </body>
        </html>
        """
    else:
        return """
        <html>
            <head>
                <title>Database Status</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        line-height: 1.6;
                    }
                    h1 {
                        color: #4285f4;
                    }
                    .status {
                        padding: 10px;
                        border-radius: 5px;
                        margin-bottom: 20px;
                    }
                    .error {
                        background-color: #f8d7da;
                        color: #721c24;
                    }
                </style>
            </head>
            <body>
                <h1>Database Connection Status</h1>
                <div class="status error">
                    <p>Failed to connect to PostgreSQL database!</p>
                </div>
                <p>Please check your database configuration and ensure the PostgreSQL service is running.</p>
                <p><a href="/">Return to home</a></p>
            </body>
        </html>
        """

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)