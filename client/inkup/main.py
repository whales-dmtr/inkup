import os

from flask import Flask, render_template
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

BASE_API_URL = f"http://{os.getenv("API_DOMAIN")}:8000"


@app.route("/", methods=["GET"])
def index():
    posts = requests.get(f"{BASE_API_URL}/posts/",)
    print(posts.json())

    return render_template("index.html", data=posts.json())

