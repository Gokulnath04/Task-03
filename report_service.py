from flask import Flask, send_file
import psycopg2
import pandas as pd

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="trading_db",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432"
    )

@app.route('/report', methods=['GET'])
def report():
    conn = get_db_connection()
    query = "SELECT * FROM transactions ORDER BY date DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()

    filename = "transaction_report.csv"
    df.to_csv(filename, index=False)

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5002)
