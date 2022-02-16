import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
SENDGRID_TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID", default="OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")

# this must match the test data structure
template_data = {
    "total_price_usd": "$14.95",
    "human_friendly_timestamp": "June 1st, 2019 10:00 AM",
    "products":[
        {"id":1, "name": "Product 1"},
        {"id":2, "name": "Product 2"},
        {"id":3, "name": "Product 3"},
        {"id":2, "name": "Product 2"},
        {"id":1, "name": "Product 1"}
    ]
} # or construct this dictionary dynamically based on the results of some other process :-D

client = SendGridAPIClient(SENDGRID_API_KEY)
print("CLIENT:", type(client))

message = Mail(from_email=SENDER_ADDRESS, to_emails=SENDER_ADDRESS)
message.template_id = SENDGRID_TEMPLATE_ID
message.dynamic_template_data = template_data
print("MESSAGE:", type(message))

try:
    response = client.send(message)
    print("RESPONSE:", type(response))
    print(response.status_code)
    print(response.body)
    print(response.headers)

except Exception as err:
    print(type(err))
    print(err)
