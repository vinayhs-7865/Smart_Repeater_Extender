from flask import Flask, render_template, jsonify, request, redirect, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "smart_repeater_secret"

USERNAME = "admin"
PASSWORD = "admin123"

# Data from Raspberry Pi
data_store = {
    "cpu": 0,
    "ram": 0,
    "temp": "N/A",
    "signal": "N/A",
    "devices": [],
    "blocked": [],
    "logs": []
}

# -------------------------------
# AUTH
# -------------------------------
def login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect("/login")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# -------------------------------
# RECEIVE DATA FROM PI
# -------------------------------
@app.route("/update", methods=["POST"])
def update():
    global data_store
    data_store.update(request.json)
    return {"status": "ok"}

# -------------------------------
# LOGIN
# -------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect("/")
        return render_template("login.html", error="Invalid Credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -------------------------------
# PAGES
# -------------------------------
@app.route("/")
@login_required
def home():
    return render_template("index.html")

@app.route("/devices")
@login_required
def devices():
    return render_template("devices.html")

@app.route("/blocked")
@login_required
def blocked():
    return render_template("blocked.html")

@app.route("/logs")
@login_required
def logs():
    return render_template("logs.html")

# -------------------------------
# API
# -------------------------------
@app.route("/stats")
@login_required
def stats():
    return jsonify(data_store)

@app.route("/logs_data")
@login_required
def logs_data():
    return jsonify({"logs": data_store.get("logs", [])})

# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run()