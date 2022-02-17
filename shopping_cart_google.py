import email
from math import prod
import os
from dotenv import load_dotenv
import datetime

# The following code enables us to pull the inventory from a google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv() #> invoking this function loads contents of the ".env" file into the script's environment...

DOCUMENT_ID = os.getenv("GOOGLE_SHEET_ID", default="OOPS")
SHEET_NAME = os.getenv("SHEET_NAME", default="Products-2021")

# an OS-agnostic (Windows-safe) way to reference the "auth/google-credentials.json" filepath:
CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "auth", "google-credentials.json")

AUTH_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
    "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)
print("CREDS:", type(credentials)) #> <class 'oauth2client.service_account.ServiceAccountCredentials'>

client = gspread.authorize(credentials)
print("CLIENT:", type(client)) #> <class 'gspread.client.Client'>

#
# READ SHEET VALUES
#
# see: https://gspread.readthedocs.io/en/latest/api.html#client
# ...  https://gspread.readthedocs.io/en/latest/api.html#gspread.models.Spreadsheet
# ...  https://gspread.readthedocs.io/en/latest/api.html#gspread.models.Worksheet

print("-----------------")
print("READING DOCUMENT...")

doc = client.open_by_key(DOCUMENT_ID)
print("DOC:", type(doc), doc.title) #> <class 'gspread.models.Spreadsheet'>

sheet = doc.worksheet(SHEET_NAME)
print("SHEET:", type(sheet), sheet.title)#> <class 'gspread.models.Worksheet'>

products = sheet.get_all_records()

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

# TODO: write some Python code here to produce the desired output

#Grocery Store Name Customization

# ... where they can be accessed / read via the os module as usual:
tax_rate = float(os.getenv("TAX_RATE", default = 0.0875))
store_name = os.getenv("STORE_NAME", default = "DELUCCHI'S MARKET")
store_url = os.getenv("STORE_URL", default = "www.delucchismarket.com")


running_total = 0
selected_ids = [] #blank list to store the selected ids in
matching_products = [] #blank list to store the information of any matching product that had been selected
email_receipt_list_dict = []

#ASK FOR USER INPUT
while True:
    product_id = input("Please input a product identifier or type 'DONE': ")
    if product_id == "DONE":
        break

#validates input to ensure user enters an existing id from the list of products
    if not any(str(x['id']) == str(product_id) for x in products):
        print("Product not scanned. Incorrect product identifier entered. Please try again.")
        continue
    else:
        selected_ids.append(product_id)


#DISPLAY OUTPUT

if __name__ == "__main__":

    print("---------------------------------")
    print(store_name)
    print(store_url)
    print("---------------------------------")
    now = datetime.datetime.now()
    checkout_time = now.strftime("%Y-%m-%d %I:%M %p")
    print("CHECKOUT AT:", checkout_time)
    print("---------------------------------")
    print("PURCHASED PRODUCTS:")



    for selected_id in selected_ids:
        matching_products = [x for x in products if str(x["id"]) == str(selected_id)]
        matching_product = matching_products[0]
        print(" ...", matching_product["name"], ("(" + str(to_usd(matching_product["price"])) + ")"))
        running_total = running_total + matching_product["price"]
        receipt_dict = {'id':matching_product["id"],'name':matching_product["name"], 'price':str(to_usd(matching_product["price"]))}
        email_receipt_list_dict.append(receipt_dict) #this saves the products selecvted in a list of dictionaries to later help produce the email receipt

    print("---------------------------------")
    print("SUBTOTAL: " + str(to_usd(running_total)))
    tax_amount= running_total*tax_rate
    print("TAX: " + str(to_usd(tax_amount)))
    final_total = running_total + tax_amount
    print("TOTAL: " + str(to_usd(final_total)))
    print("---------------------------------")
    print("THANKS, SEE YOU AGAIN SOON!")
    print("---------------------------------")


# ASKS IF CUSTOMER WANTS COPY OF RECEIPT SENT TO EMAIL, VALIDATES INPUT, AND SENDS EMAIl
#this stores the valid choices in a list

while True:
    valid_choices = ['Y', 'N']
    email_receipt = input("Would you like a copy of your receipt emailed to you? Please choose 'Y' for Yes or 'N' for No: ")

    if email_receipt in valid_choices:
        if email_receipt == 'Y':
            customer_address = input("Please enter your email: ")
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail

            load_dotenv()

            SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
            SENDGRID_TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID", default="OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
            SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")

            # this must match the test data structure
            template_data = {
                "store_name" : store_name,
                "subtotal_usd": str(to_usd(running_total)),
                "tax_amount_usd": str(to_usd(tax_amount)),
                "total_cost_usd": str(to_usd(final_total)),
                "human_friendly_timestamp": str(checkout_time),
                "products":email_receipt_list_dict
            }

            client = SendGridAPIClient(SENDGRID_API_KEY)
            print("CLIENT:", type(client))

            message = Mail(from_email=SENDER_ADDRESS, to_emails=customer_address)
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
            break
        if email_receipt == 'N':
            break
    else:
        print("Oops incorrect entry. Please try again")
        continue
