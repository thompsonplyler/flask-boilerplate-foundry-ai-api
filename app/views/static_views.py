# Standard Library imports

# Core Flask imports
from flask import render_template, jsonify

# Third-party imports
from flask_login import login_required

# App imports
from ..permissions import roles_required


def index():
    return render_template("index.html")


def register():
    return render_template("register.html")


def login():
    return render_template("login.html")

def test_connection():
    return jsonify({"message": "success"})


@login_required
def settings():
    return render_template("settings.html")


@login_required
@roles_required(["admin"])
def admin():
    return render_template("admin.html")
