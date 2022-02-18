# shopping-cart
Improve your grocery store's operations by using this code to automate receipts!

## Setup
Install any necessary packages from the 'requirements.txt' file:
```sh
pip install -r requirements.txt
```
## Configuring Sales Tax Rate (Bonus)
Navigate to your projects directory and create a '.env' file:
```sh
touch .env
```

Next, locate your .env file and open it with a text editor (Note: Mac users may have trouble finding their '.env' file since finder automatically hides files that start with a '.' In order to find your file click Cmd + Shift + '.' to reveal hidden files.)

Add your store's tax rate, name, and website url to your '.env' file following the format of the example below:

```sh
TAX_RATE = 0.0875
STORE_NAME="DELUCCHI'S MARKET"
STORE_URL="www.delucchismarket.com"
```

If it does not exist already, create a '.gitignore' file:
```sh
touch .gitignore
```
Similar to your '.env' file, find and open your '.gitignore' file. Copy the following code into the file so that your environment variables are not published publically to github:
```sh
.env
```
## Integrating with a CSV File Datastore (Bonus)
To customize your inventory of products, navigate to the 'data' subdirectory/folder within your directory. Create a copy of the 'default_products.csv' file and name it 'products.csv'. You can now open and edit any of the fields to customize your inventory, including adding new products!

You'll also need to add some code to your .gitignore file to ensure that your custom inventory 'products' file does not get tracked by version control. To do so, add the following code to your '.gitignore' file:

```sh
data/products.csv
!data/default_products.csv
```


## Sending Receipts via Email (Bonus)
[Sign up for a SendGrid account](https://signup.sendgrid.com/), then follow the instructions to complete your "Single Sender Verification", clicking the link in a confirmation email to verify your account. You should also be able to access this via the settings menu:

![](https://user-images.githubusercontent.com/1328807/85074750-0cb54c00-b18b-11ea-940f-769cbcde53ad.png)


Then [create a SendGrid API Key](https://app.sendgrid.com/settings/api_keys) with "full access" permissions. In your '.env' file, store the API Key value in an [environment variable](/notes/environment-variables/README.md) called `SENDGRID_API_KEY`.

Also set an environment variable called `SENDER_ADDRESS` to be the same email address as the single sender address you just associated with your SendGrid account.

Navigate to https://sendgrid.com/dynamic_templates and press the "Create Template" button on the top right. Give it a name like "example-receipt", and click "Save". At this time, you should see your template's unique identifier (e.g. "d-54e6165cdec4441383382d7455f327ea"). Copy this value and store it in an environment variable called `SENDGRID_TEMPLATE_ID`.

Your '.env' file should now look something like the example below:

```sh
TAX_RATE = 0.0875
STORE_NAME="DELUCCHI'S MARKET"
STORE_URL="www.delucchismarket.com"
SENDGRID_API_KEY = "whatever your API Key is"
SENDGRID_TEMPLATE_ID = "d-54e6165cdec4441383382d7455f327ea"
SENDER_ADDRESS = "john.picker3@gmail.com"
```

Back in the SendGrid platform, click "Add Version" to create a new version of a "Blank Template" and select the "Code Editor" as your desired editing mechanism.

At this point you should be able to paste the following HTML into the "Code" tab, and the corresponding example data in the "Test Data" tab, and save each after you're done editing them.

Example "Code" template which will specify the structure of all emails:

```html
<img src="https://www.shareicon.net/data/128x128/2016/05/04/759867_food_512x512.png">

<h3>Hello this is your receipt from {{store_name}}</h3>

<p>Receipt Date: {{human_friendly_timestamp}}</p>

<p>Products purchased:<p>

<ul>
{{#each products}}
	<li>{{this.name}} . . . {{this.price}}</li>
{{/each}}
</ul>

<p>Subtotal: {{subtotal_usd}}</p>
<p>Tax: {{tax_amount_usd}}</p>
<p>Total: {{total_cost_usd}}</p>
```

Example "Test Data" which will populate the template:

```html
{
    "store_name": "Delucchi's Market",
    "subtotal_usd": "$85.00",
    "tax_amount_usd": "14.99",
    "total_cost_usd": "$99.99",
    "human_friendly_timestamp": "July 4th, 2099 10:00 AM",
    "products":[
        {"id": 100, "name": "Product 100", "price":"$2.99"},
        {"id": 200, "name": "Product 200", "price":"$12.99"},
        {"id": 300, "name": "Product 300", "price":"$22.99"},
        {"id": 500, "name": "Product 500", "price":"$20.99"},
        {"id": 600, "name": "Product 600", "price":"$14.99"}
    ]
}
```

## Now you're ready to create the receipt!
Now you can run the following code to enter the product ids, create the receipt, and send a copy of the receipt to an email:
```sh
python shopping_cart.py
```

## Integrating with Google Sheets Datastore (Bonus)
(Note: For this bonus, you will be running the 'shopping_cart_google.py' file.)

First, you will need to create and download Google API credentials. To do so, follow the instructions below:

Visit the [Google Developer Console](https://console.developers.google.com/cloud-resource-manager). Create a new project, or select an existing one. Click on your project, then from the project page, search for the "Google Sheets API" and enable it. Also search for the "Google Drive API" and enable it.

From either API page, or from the [API Credentials](https://console.developers.google.com/apis/credentials) page, follow a process to create and download credentials to use the APIs:
  1. Click "Create Credentials" for a "Service Account". Follow the prompt to create a new service account named something like "spreadsheet-service", and add a role of "Editor".
  2. Click on the newly created service account from the "Service Accounts" section, and click "Add Key" to create a new "JSON" credentials file for that service account. Download the resulting .json file (this might happen automatically).
  3. Rename the file "google-credentials.json". Then move a copy of the credentials file into your project repository, into a subdirectory called "auth". Note its filepath; it should look something like "auth/google-credentials.json".

Add the credentials filepath to your repository's '.gitignore' file to ensure it does not get tracked in version control or uploaded to GitHub:

```sh
auth/google-credentials.json
google-credentials.json
*.json
```

Next, you will update your '.env' file to include an additional environment variable. You should create a new environment variable called `GOOGLE_SHEET_ID` and set it equal to `"1ItN7Cc2Yn4K90cMIsxi2P045Gzw0y2JHB_EkV4mXXpI"`.

Your '.env' file should now look something like this:

```sh
TAX_RATE = 0.0875
STORE_NAME="DELUCCHI'S MARKET"
STORE_URL="www.delucchismarket.com"
SENDGRID_API_KEY = "whatever your API Key is"
SENDGRID_TEMPLATE_ID = "d-54e6165cdec4441383382d7455f327ea"
SENDER_ADDRESS = "john.picker3@gmail.com"
GOOGLE_SHEET_ID = "1ItN7Cc2Yn4K90cMIsxi2P045Gzw0y2JHB_EkV4mXXpI"
```

Make sure to save your '.env' and '.gitignore' files. Now you can run the following code:

```sh
python shopping_cart_google.py
```

Python will pull the product inventory from the google sheet based off the unique identifier you set as the `GOOGLE_SHEET_ID` environment variable.
