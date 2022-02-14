# shopping-cart
Improve your grocery store's operations by using this code to automate receipts!

## Setup

If using third party packages, create a virtual environment:
```sh
conda create -n shoppingcart-env python=3.8
```
Then activate that virtual environment:
```sh
conda activate shoppingcart-env
```
Install any necessary packages from the 'requirements.txt' file:
```sh
pip install -r requirements.txt
```

## Customization

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
Similar to your .env file, find and open your '.gitignore' file. Copy the following code into the file so that your environment variables are not published publically to github:
```sh
.env
```

Now you can run the following code to enter your products and create the receipt:
```sh
python shopping_cart.py
```
