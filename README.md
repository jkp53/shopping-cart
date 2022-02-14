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
Install the dotenv package:
```sh
pip install python-dotenv #note: NOT just "dotenv"
```
Create a ".env" file and .gitignore file in your present working directory by running the following code:

```sh
touch .env
#my_file = ".env"
#with open(my_file, "w") as file:
#    file.write(STORE_NAME="JOHN'S GROCERY MARKET")

#my_file = write()
#STORE_URL="www.johnsgrocerymarket.com"
#TAX_RATE=0.0875

touch .gitignore
```

TAX_RATE = .0875
STORE_NAME="JOHN'S GROCERY MARKET"
STORE_URL="www.johnsgrocerymarket.com"

## Usage (including store customization)

Set a custom name and website url for your grocery store by changing the name and url in the quotation marks. Then create your receipt by running the 'python game.py' code.

```sh
#STORE_NAME="JOHN'S GROCERY MARKET" #STORE_URL="www.johnsgrocerymarket.com" python #game.py
```
