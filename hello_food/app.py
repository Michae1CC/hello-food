from flask import Flask
from .sql import Base, engine, session_maker
from .user import TrialUserSqlFactory, TrialUserSqlRepository
from .update_driver import update_sql_entities


app = Flask(__name__)

Base.metadata.create_all(engine)


@app.route("/")
def hello() -> str:

    return "<p>Oh hi!</p>"


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


@app.route("/update_meals")
def update_meals() -> str:
    f = TrialUserSqlRepository()
    user = f.get_from_email("hi@gmail.com")
    if user is not None:
        user.meals_per_week = 42
        update_sql_entities(user)

    return "<p>Successful get</p>"


create_user()
