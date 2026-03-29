from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# This stores data coming from Raspberry Pi
data_store = {
    "cpu": 0,
    "ram": 0,
    "temp": "N/A",
    "signal": "N/A",
    "devices": [],
    "blocked": []
}

# -------------------------------
# Receive data from Raspberry Pi
# -------------------------------
@app.route("/update", methods=["POST"])
def update():
    global data_store
    data_store = request.json
    return {"status": "updated"}

# -------------------------------
# Dashboard page
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------------
# API for frontend
# -------------------------------
@app.route("/stats")
def stats():
    return jsonify(data_store)

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    app.run()