products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

print(products)
# TODO: write some Python code here to produce the desired output

#Grocery Store Name Customization

from math import prod
import os
import datetime

store_name = os.getenv("STORE_NAME", default = "DELUCCHI'S MARKET")
store_url = os.getenv("STORE_URL", default = "www.delucchismarket.com")


running_total = 0
selected_ids = [] #blank list to store the selected ids in
matching_products = [] #blank list to store the information of any matching product that had been selected
tax_rate = .0875

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
    print("CHECKOUT AT:", now.strftime("%Y-%m-%d %I:%M %p"))
    print("---------------------------------")
    print("PURCHASED PRODUCTS:")

    for selected_id in selected_ids:
        matching_products = [x for x in products if str(x["id"]) == str(selected_id)]
        matching_product = matching_products[0]
        print(" ...", matching_product["name"], ("(" + str(to_usd(matching_product["price"])) + ")"))
        running_total = running_total + matching_product["price"]

    print("---------------------------------")
    print("SUBTOTAL: " + str(to_usd(running_total)))
    tax_amount= running_total*tax_rate
    print("TAX: " + str(to_usd(tax_amount)))
    final_total = running_total + tax_amount
    print("TOTAL: " + str(to_usd(final_total)))
    print("---------------------------------")
    print("THANKS, SEE YOU AGAIN SOON!")
