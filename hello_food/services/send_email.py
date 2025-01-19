from typing import Final

import boto3

_SES_CLIENT: Final = boto3.client("ses")
_HELLO_FOOD_SOURCE_EMAIL: Final[str] = "TODO"


def send_customer_email(customer_email: str, subject: str, body: str) -> None:
    _SES_CLIENT.send_email(
        Source=_HELLO_FOOD_SOURCE_EMAIL,
        Destination={
            "ToAddresses": [
                customer_email,
            ],
        },
        Message={
            "Subject": {"Data": subject},
            "Body": {
                "Text": {"Data": body},
            },
        },
        SourceArn="string",
    )
