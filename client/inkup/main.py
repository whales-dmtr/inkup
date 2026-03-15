import os
from datetime import datetime, timedelta
from functools import wraps

import requests
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask.helpers import make_response
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
            response = requests.post(
                f"{BASE_API_URL}/token/verify/", json={"token": token}
            )

            if response.status_code != 200:
                return render_template(
                    "login.html",
                    data={
                        "login_url": url_for("login", _external=True),
                        "redirected_from": request.path,
                    },
                )

        return f(*args, **kwargs)

    return wrapper


@app.route("/", methods=["GET"])
def index():
    posts = requests.get(
        f"{BASE_API_URL}/posts/",
    )
    urls = {
            "login": url_for("login"),
            "signup": url_for("signup"),
    }

    return render_template("index.html", data=posts.json(), urls=urls)


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

        redirect_page = request.form.get("redirected_from") or "/"
        response = make_response(redirect(redirect_page))

        response.set_cookie("token", token, expires=expire_time, httponly=True)

        return response
    else:
        return render_template(
            "login.html", data={"login_url": url_for("login", _external=True)}
        )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        creds = dict(request.form)
        api_response = requests.post(
            f"{BASE_API_URL}/users/register/",
            json={"username": creds["username"], "password": creds["password"]},
        )
        token = api_response.json()["access"]
        expire_time = datetime.now() + timedelta(minutes=15)

        response = make_response(redirect('/'))
        response.set_cookie("token", token, expires=expire_time, httponly=True)

        return response
    else:
        return render_template(
            "signup.html", data={"signup_url": url_for("signup", _external=True)}
        )



