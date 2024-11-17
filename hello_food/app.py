from flask import Flask
from .sql import Base, engine
from .user import get_trial_user_factory, get_user_repository
from .address import get_address_factory
from .update_driver import update_sql_entities


app = Flask(__name__)

Base.metadata.create_all(engine)


@app.route("/")
def hello() -> str:

    return "<p>Oh hi!</p>"


def create_user() -> str:
    f = get_trial_user_factory()
    user = f.create_from_json(
        {
            "email": "hi@gmail.com",
            "name": "mike",
            "meals_per_week": "2",
            "trial_end_date": "123123",
            "discount_value": "0.2",
            "address": {
                "unit": "U 18",
                "street_name": "Green",
                "suburb": "Brisbane",
                "postcode": "4000",
            },
        }
    )
    print(user)

    return "<p>Success</p>"


@app.route("/get")
def get_user() -> str:
    f = get_user_repository()
    user = f.get_from_email("hi@gmail.com")
    if user is not None:
        print(user)
        print(user.address)
    else:
        print("No user found")

    return "<p>Successful get</p>"


@app.route("/update_meals")
def update_meals() -> str:
    f = get_user_repository()
    a_f = get_address_factory()
    new_address = a_f.create_from_values("U 42", "Brown", "Rockhampton", 4300)
    user = f.get_from_email("hi@gmail.com")
    if user is not None:
        user.meals_per_week = 42
        user.address = new_address
        update_sql_entities(user)

    return "<p>Successful get</p>"


create_user()
