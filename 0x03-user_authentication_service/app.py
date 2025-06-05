#!/usr/bin/env python3
"""Basic Flask App"""
from flask import Flask, jsonify
from auth import Auth

AUTH =  Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome() -> str:
    """Welcome route that returns a json message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """Handler to register a user"""


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
