# main part

import utils
import data_source
import menu
import cart
import recommend
import bill

MENU_MIN = 0
MENU_MAX = 6


def show_main_menu():
    utils.print_title("Main Menu")
    print("  1. Browse the menu")
    print("  2. Search a dish")
    print("  3. Add a dish to the cart")
    print("  4. View / edit the cart")
    print("  5. Get a recommendation")
    print("  6. Check out and pay")
    print("  0. Exit")
    utils.print_line("-")


def show_cart_brief(shopping_cart):

    if cart.is_empty(shopping_cart):
        print("Cart: empty")
        return
    print(
        f"Cart: {cart.line_count(shopping_cart)} line(s), "
        f"{cart.item_count(shopping_cart)} item(s), "
        f"{utils.format_money(cart.calc_cart(shopping_cart))}"
    )


def add_dish(shopping_cart, food):
    # 先看能不能卖、还能加几份，再交给 cart
    if food is None:
        return False

    if not food["available"]:
        utils.print_warning(f"{food['name']} is not sold today.")
        return False

    remain = cart.add_max(shopping_cart, food)
    if remain <= 0:
        utils.print_warning(f"No more {food['name']} can be added, the stock is used up.")
        return False

    buy_num = utils.read_int(
        f"How many {food['name']}? (1-{remain}, 0 to cancel): ", 0, remain
    )
    if buy_num == 0:
        return False

    return cart.add_food(shopping_cart, food, buy_num)


def do_browse(shopping_cart):
    menu.show_menu()

    if utils.read_yes_no("Add a dish now? (y/n): "):
        do_add(shopping_cart)


def do_search(shopping_cart):
    results = menu.search_menu()

    if len(results) == 0:
        return

    if utils.read_yes_no("Add one of them to the cart? (y/n): "):
        food = menu.ask_dish(results)
        add_dish(shopping_cart, food)


def do_add(shopping_cart):
    food = menu.ask_food_id()

    if food is None:
        return

    menu.show_food_detail(food)
    add_dish(shopping_cart, food)


def change_quantity(shopping_cart):
    food = menu.ask_food_id("Dish ID to change: ")

    if food is None:
        return

    item = cart.find_food(shopping_cart, food["id"])
    if item is None:
        utils.print_warning(f"{food['name']} is not in your cart.")
        return

    new_num = utils.read_int(
        f"New quantity for {food['name']} (1-{food['stock']}): ", 1, food["stock"]
    )
    cart.change_quant(shopping_cart, food["id"], new_num)


def remove_dish(shopping_cart):
    food = menu.ask_food_id("Dish ID to remove: ")

    if food is None:
        return

    cart.delete_food(shopping_cart, food["id"])


def do_cart(shopping_cart):
    while True:
        cart.show_cart(shopping_cart)

        if cart.is_empty(shopping_cart):
            return

        print()
        print("  1. Change the quantity of a dish")
        print("  2. Remove a dish")
        print("  3. Show the cart summary")
        print("  4. Add another dish")
        print("  0. Back to the main menu")
        utils.print_line("-")

        choice = utils.read_int("Your choice: ", 0, 4)

        if choice == 0:
            return
        elif choice == 1:
            change_quantity(shopping_cart)
        elif choice == 2:
            remove_dish(shopping_cart)
        elif choice == 3:
            cart.show_cart_summary(shopping_cart)
        else:
            do_add(shopping_cart)


def do_recommend(shopping_cart):
    tips = recommend.show_recommend(shopping_cart)

    if len(tips) == 0:
        return

    if not utils.read_yes_no("Add one suggestion to the cart? (y/n): "):
        return

    suggested = []
    for tip in tips:
        suggested.append(tip["food"])

    food = menu.ask_dish(suggested)
    add_dish(shopping_cart, food)


def do_checkout(shopping_cart, order_no, table_no):
    # 结账，返回订单号
    if cart.is_empty(shopping_cart):
        utils.print_warning("The cart is empty, there is nothing to pay.")
        return order_no

    problems = cart.check_cart(shopping_cart)
    if len(problems) > 0:
        for problem in problems:
            utils.print_warning(problem)
        utils.print_inform("Please fix the cart before paying.")
        return order_no

    cart.show_cart(shopping_cart)
    cart.show_cart_summary(shopping_cart)

    # 先复制chuan can，后面清空购物车不会影响小票
    lines = cart.cart_lines_for_bill(shopping_cart)
    bill_data = bill.make_bill(lines)
    bill.print_bill_brief(bill_data, order_no)

    if not utils.read_yes_no("Pay now? (y/n): "):
        utils.print_inform("Nothing is paid, your cart is kept.")
        return order_no

    paid = utils.read_float(
        f"Cash received (total is {utils.format_money(bill_data['total'])}): ",
        bill_data["total"],
    )

    change = bill.print_bill(bill_data, order_no, table_no, paid)

    # 购物车清空
    cart.reduce_stock(shopping_cart)
    cart.clear_cart(shopping_cart)

    utils.print_success(
        f"Order {order_no} paid. Change: {utils.format_money(change)}."
    )
    return order_no + 1


def run():
    utils.print_title("Restaurant Self-Service Ordering System")
    print("Welcome! Order your meal here, step by step.")
    print(f"We have {data_source.available_count()} dishes on the menu today.")

    table_no = utils.read_text("Table number (press Enter for take away): ", True)
    if table_no == "":
        table_no = "take away"

    shopping_cart = cart.empty_cart()
    order_no = bill.FIRST_ORDER_NO

    utils.print_inform(f"Table {table_no}, let's start.")

    while True:
        print()
        show_cart_brief(shopping_cart)
        show_main_menu()

        choice = utils.read_int("Your choice: ", MENU_MIN, MENU_MAX)

        if choice == 0:
            break
        elif choice == 1:
            do_browse(shopping_cart)
        elif choice == 2:
            do_search(shopping_cart)
        elif choice == 3:
            do_add(shopping_cart)
        elif choice == 4:
            do_cart(shopping_cart)
        elif choice == 5:
            do_recommend(shopping_cart)
        else:
            order_no = do_checkout(shopping_cart, order_no, table_no)

    if not cart.is_empty(shopping_cart):
        utils.print_warning("Your cart was not paid, the dishes are put back.")

    utils.print_title("Goodbye")
    print("Thank you, have a nice day!")


def main():
    # 防崩溃
    try:
        run()
    except KeyboardInterrupt:
        print()
        utils.print_warning("Program stopped by the keyboard.")
    except EOFError:
        print()
        utils.print_warning("Input closed, program stopped.")


if __name__ == "__main__":
    main()