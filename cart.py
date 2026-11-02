# cart part
# Goal: add, remove, update and view the items of the shopping cart and calculate the cart total. 
# Cart item:
# "food": food_dictionary, "quant": number
# The cart is a list of such items. "food" points to the dictionary in data_source.py, so price or stock is the same data.

from data_source import all_categories
from utils import (
    print_line,
    print_title,
    print_warning,
    print_success,
    print_inform,
    print_header,
    print_row,
    format_money,
    format_quantity,
)#utils里的 后面导出

# 1.Initial cart and Basic state
#===========================================================
def empty_cart():
    # Build an empty cart
    cart = []
    return cart

# True when there is nothing in the cart
def is_empty(cart):
    if len(cart) == 0:
        return True
    else:
        return False

# Total number of dishes ，quantities added together
def item_count(cart):
    total_num = 0
    for item in cart:
        total_num = total_num + item["quant"]
    return total_num

# How many different dishes are in the cart
def line_count(cart):
    return len(cart)


# Return the cart item of this food, None when it is not in the cart
def find_food(cart, food_id):
    for item in cart:
        if item["food"]["id"] == food_id:
            return item
    return None


# How many more of this food can still be added:
# kitchen stock minus what is already in the cart
def add_max(cart, food):
    item = find_food(cart, food["id"])
    used = 0
    if item is not None:
        used = item["quant"]
    return food["stock"] - used


# 2. About Ordering
#   situation 1 -> the food is already in the cart, add to its quantity 
#   situation 2 -> the food is not in the cart, create a new cart item
# ==========================================================================

def add_food(cart, food, buy_num):
    if food is None:
        print_warning("This food does not exist.")
        return False
    
    if buy_num is None or buy_num <= 0:
        print_warning("Buy number can not be zero or negative!")
        return False
    
    if not food["available"]:
        print_warning(f"{food['name']} is not available today.")
        return False

    remain = add_max(cart, food)
    if buy_num > remain:
        print_warning(
            f"Only {remain}*{food['name']} can still be added "
            f"(stock is {food['stock']})."
        )
        return False

    exist_item = find_food(cart, food["id"])

    #if there has already existed the dish
    #add the number directly
    if exist_item is not None:
        exist_item["quant"] = exist_item["quant"] + buy_num
    else:
        #if there has nothing in crat
        #creat a new one
        new_item = {
            "food": food,
            "quant": buy_num,
        }
        cart.append(new_item)

    print_success(f"Added {buy_num}*{food['name']} to the cart.")
    return True

# Add a group of foods.
# If one food fails, the others are still tried, and a small report is shown.
def add_foods(cart, foods, buy_num):
    success = 0
    failed = 0
    for food in foods:
        if add_food(cart, food, buy_num):
            success = success + 1
        else:
            failed = failed + 1
    print_inform(f"{success} food added, {failed} food skipped.")
    return failed == 0


# 3. Change and delete
# ===========================================================================
#to change the number of the target food in cart
def change_quant(cart, food_id, new_num):
    target_item = find_food(cart, food_id)

    #can not find the target food
    if target_item is None:
        print_warning("This food is not in your cart.")
        return False
     
    #can not set negative number or zero
    if new_num is None or new_num <= 0:
        print_warning("Number can not be less than or equal to zero.")
        return False

    #number > stock
    if new_num > target_item["food"]["stock"]:
        print_warning(f"Only {target_item['food']['stock']} in stock.")
        return False

    target_item["quant"] = new_num
    print_success(f"Quantity of {target_item['food']['name']} changed to {new_num}.")
    return True


# Remove one food from the cart
def delete_food(cart, food_id):
    item = find_food(cart, food_id)
    if item is None:
        print_warning("This food is not in your cart.")
        return False

    cart.remove(item)
    print_success(f"{item['food']['name']} removed from the cart.")
    return True

# Remove everything, used after the bill is paid
def clear_cart(cart):
    cart.clear()


# 4. Calculating the subtotal
# ===========================================================================

# to calculate the total money in cart
def calc_cart(cart): 
    total_money = 0
    for item in cart:
        price = item["food"]["price"]
        num = item["quant"]
        total_money = total_money + price * num 
    return total_money

# Money spent on each category
#eg; how much it spend on drink
def category_total(cart, category):
    total = 0
    for item in cart:
        if item["food"]["category"] == category:
            total = total + item["food"]["price"] * item["quant"]
    return total

# count how many items we pick for one food type
def category_quantity(cart, category):
    total = 0
    for item in cart:
        if item["food"]["category"] == category:
            total = total + item["quant"]
    return total


#make a dictionary to save money for every food type
def category_summary(cart):
    summary = {}
    for category in all_categories:
        summary[category] = category_total(cart, category)
    return summary


# 5. Display
# ===========================================================================
# show all things in cart
def show_cart(cart):
    print_title("Your Cart")

    if is_empty(cart):
        print("The cart is empty. Let's take the order!")
        return
    print_header(["ID", "Name", "Price", "Quantity", "Subtotal"])

    i = 0
    while i < len(cart):
        item = cart[i]
        food = item["food"]
        subtotal = food["price"] * item["quant"]
        print_row(
            [
                food["id"],
                food["name"],
                format_money(food["price"]),
                format_quantity(item["quant"]),
                format_money(subtotal),
            ]
        )
        i = i + 1

    print_line("==========================================")
    print(
        f"Lines: {line_count(cart)}  "
        f"Items: {item_count(cart)}  "
        f"Total: {format_money(calc_cart(cart))}"
    )


# Show how the money is split between categories
def show_cart_summary(cart):
    print_title("Cart Summary")

    if is_empty(cart):
        print("The cart is empty.")
        return

    print_header(["Category", "Dishes", "Money"])

    i = 0
    while i < len(all_categories):
        category = all_categories[i]
        quantity = category_quantity(cart, category)
        money = category_total(cart, category)
        print_row(
            [category, str(quantity), format_money(money)]
        )
        i = i + 1

    print_line("=============================================")
    print_row(
        ["Total", str(item_count(cart)), format_money(calc_cart(cart))]
    )


# 6. Checkout support
# ===========================================================================
def check_cart(cart):
    # Return a list of problems found before paying, empty list means OK
    problems = []
    for item in cart:
        food = item["food"]
        if not food["available"]:
            problems.append(f"{food['name']} is no longer available today.")
        if item["quant"] > food["stock"]:
            problems.append(
                f"{food['name']}: you ordered {item['quant']}, "
                f"but only {food['stock']} left in stock."
            )
    return problems


def reduce_stock(cart):
    # reduce stock after customer pays the bil
    for item in cart:
        item["food"]["stock"] = item["food"]["stock"] - item["quant"]
        if item["food"]["stock"] < 0:
            item["food"]["stock"] = 0


def cart_lines_for_bill(cart):
    #make a copy of cart data for bill
    #do not change when the cart is cleared afterwards
    lines = []
    for item in cart:
        food = item["food"]
        lines.append(
            {
                "id": food["id"],
                "name": food["name"],
                "category": food["category"],
                "price": food["price"],
                "quant": item["quant"],
            }
        )
    return lines