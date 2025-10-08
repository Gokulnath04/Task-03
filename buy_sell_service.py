from flask import Flask, request, jsonify, send_file
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="trading_db",
        user="postgres",
        password="12345", 
        host="localhost",
        port="5432"
    )

INVOICE_DIR = "invoices"
os.makedirs(INVOICE_DIR, exist_ok=True)

@app.route('/buy', methods=['POST'])
def buy():
    try:
        data = request.json
        product = data.get("product")
        quantity = data.get("quantity")
        price = data.get("price")

        if not (product and quantity and price):
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transactions (type, product, quantity, price, date)
            VALUES (%s, %s, %s, %s, %s)
        """, ("buy", product, quantity, price, datetime.now()))
        conn.commit()
        cur.close()
        conn.close()

        filename = os.path.join(INVOICE_DIR, f"buy_invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
        with open(filename, "w") as f:
            f.write(f"=== BUY INVOICE ===\nProduct: {product}\nQuantity: {quantity}\nPrice: {price}\nDate: {datetime.now()}")

        return send_file(filename, as_attachment=True)
    except Exception as e:
        print("Error in /buy:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/sell', methods=['POST'])
def sell():
    try:
        data = request.json
        product = data.get("product")
        quantity = data.get("quantity")
        price = data.get("price")

        if not (product and quantity and price):
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transactions (type, product, quantity, price, date)
            VALUES (%s, %s, %s, %s, %s)
        """, ("sell", product, quantity, price, datetime.now()))
        conn.commit()
        cur.close()
        conn.close()

        filename = os.path.join(INVOICE_DIR, f"sell_invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
        with open(filename, "w") as f:
            f.write(f"=== SELL INVOICE ===\nProduct: {product}\nQuantity: {quantity}\nPrice: {price}\nDate: {datetime.now()}")

        return send_file(filename, as_attachment=True)
    except Exception as e:
        print("Error in /sell:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
