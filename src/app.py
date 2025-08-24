from flask import Flask, Response, send_file
from flask_sqlalchemy import SQLAlchemy
import os
import time
import requests

start_time = time.time()
start_period = 10

app = Flask(__name__)

# Access the environment variable
app_env = os.environ.get("APP_ENV", "Development")
connection_string = os.environ.get("DB_CONNECTION", "")

# Configure the MySQL database connection
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db = SQLAlchemy(app)


# Define a Counter model
class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)


# Initialize the databased
with app.app_context():
    db.create_all()
    counter = Counter.query.first()
    if counter is None:
        counter = Counter(value=0)
        db.session.add(counter)
        db.session.commit()


@app.route("/")
def hello():
    counter = Counter.query.first()
    counter.value += 1
    db.session.commit()
    return f'''
    Docker is Awesome! My ENV var is: {app_env}<br>
    Page reload count: {counter.value}<br>
<pre>                   ##        .</pre>
<pre>             ## ## ##       ==</pre>
<pre>          ## ## ## ##      ===</pre>
<pre>      /""""""""""""""""\\___/ ===</pre>
<pre> ~~~ (~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===-- ~~~</pre>
<pre>      \\______ o          __/</pre>
<pre>        \    \        __/</pre>
<pre>         \\____\\______/</pre>
    '''


@app.route("/logo")
def docker_logo():
    return send_file("docker-logo.png", mimetype="image/png")


@app.route("/health")
def health_check():
    return Response("Healthy", status=200)


@app.route("/ready")
def readiness_check():
    if time.time() < start_time + start_period:
        return Response("Not Ready", status=503)
    else:
        return Response("Ready", status=200)


@app.route("/external-call")
def external_call():
    external_url = os.getenv("EXTERNAL_ENDPOINT")
    if not external_url:
        Response("EXTERNAL_ENDPOINT not defined", status=500)
    try:
        response = requests.get(external_url)
        return Response(
            f"External call response: {response.text}", status=response.status_code
        )
    except Exception as e:
        return Response(f"Error calling external endpoint: {str(e)}", status=500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
