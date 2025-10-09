from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/payment', methods=['POST'])
def payment():
    return jsonify({"status": "Payment successful"}), 200

if __name__ == '__main__':
    app.run(port=5003)
