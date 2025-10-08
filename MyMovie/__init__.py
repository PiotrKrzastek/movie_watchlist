from os import getenv
from flask import Flask
from MyMovie.routes import *
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.mongo_uri = getenv("DBURI")
    app.secret_key = "ABCD"

    app.db = MongoClient(app.mongo_uri).movies_app

    app.register_blueprint(Auth)
    app.register_blueprint(Util)
    app.register_blueprint(Movies)

    return app
