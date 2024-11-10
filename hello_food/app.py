# from flask import Flask
from .sqlalchemy import Base, engine

# app = Flask(__name__)


# @app.route("/")
# def hello_world() -> str:
#     return "<p>Hello, World!</p>"

Base.metadata.create_all(engine)
