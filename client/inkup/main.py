from datetime import datetime, timedelta
import os

from functools import wraps
from flask.helpers import make_response
import requests
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FRONTEND_SECRET")

csrf = CSRFProtect(app)

BASE_API_URL = os.getenv("API_TRUSTED_ORIGINS", "").split(" ")[0]


def auth_required(f):
    """
    Decorator for endpoints which requires authentication.
    Works through external API.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        with app.app_context():
            token = request.cookies.get("token")
            response = requests.post(f"{BASE_API_URL}/token/verify/", json={"token": token})
            
            if response.status_code != 200:
                return render_template(
                    "login.html", data={"login_url": url_for("login", _external=True),
                                        "redirected_from": request.path}
                )

        return f(*args, **kwargs)
    return wrapper


@app.route("/", methods=["GET"])
def index():
    posts = requests.get(
        f"{BASE_API_URL}/posts/",
    )

    return render_template("index.html", data=posts.json())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        creds = dict(request.form)
        api_response = requests.post(
            f"{BASE_API_URL}/token/",
            json={"username": creds["username"], "password": creds["password"]},
        )
        token = api_response.json()["access"]

        expire_time = datetime.now() + timedelta(minutes=15)

        if request.form.get("redirected_from"):
            redirect_page = request.form.get("redirected_from")
        else:
            redirect_page = "/"

        response = make_response(redirect(redirect_page))

        response.set_cookie("token", token, expires=expire_time)

        return response
    else:
        return render_template(
            "login.html", data={"login_url": url_for("login", _external=True)}
        )


@app.route("/supersecret", methods=["GET"])
@auth_required
def supersecret():
    return render_template("index.html")
