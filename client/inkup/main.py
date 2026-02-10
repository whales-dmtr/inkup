import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FRONTEND_SECRET")

csrf = CSRFProtect(app)

BASE_API_URL = os.getenv("API_TRUSTED_ORIGINS", '').split(' ')[0]

@app.route("/", methods=["GET"])
def index():
    posts = requests.get(f"{BASE_API_URL}/posts/",)

    return render_template("index.html", data=posts.json())


@app.route("/login", methods=["GET", "POST"])
def login(username=None, password=None):
    return render_template("login.html", data={"base_url": "http://localhost:8000"})

