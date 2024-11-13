from flask import Flask
from .sqlalchemy import Base, engine, session_maker
from .user import TrialUserSqlFactory, TrialUserSqlRepository


app = Flask(__name__)

Base.metadata.create_all(engine)


@app.route("/")
def hello() -> str:

    return "<p>Oh hi!</p>"


@app.route("/create")
def create_user() -> str:
    f = TrialUserSqlFactory()
    user = f.create_from_json(
        {
            "email": "hi@gmail.com",
            "name": "mike",
            "meals_per_week": "2",
            "trial_end_date": "123123",
            "discount_value": "0.2",
        }
    )
    print(user)

    return "<p>Success</p>"


@app.route("/get")
def get_user() -> str:
    f = TrialUserSqlRepository()
    user = f.get_from_email("hi@gmail.com")
    print(user)

    return "<p>Successful get</p>"
