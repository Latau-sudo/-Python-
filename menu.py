# menu part
# 浏览菜单、按名称/价格/分类搜索

from data_source import Menu, all_categories, all_foods, get_food
from utils import (
    print_title,
    print_section,
    print_header,
    print_row,
    print_line,
    print_inform,
    print_warning,
    format_money,
    format_quantity,
    read_text,
    read_int,
    read_float,
)


def dishes_of(category):
    if category in Menu:
        return Menu[category]
    return []


def status_text(food):
    if not food["available"]:
        return "off menu"
    if food["stock"] <= 0:
        return "sold out"
    return "on sale"


def show_food_detail(food):
    print_section(food["name"])
    print_line("-")
    print(f"  ID       : {food['id']}")
    print(f"  Category : {food['category']}")
    print(f"  Price    : {format_money(food['price'])}")
    print(f"  Stock    : {format_quantity(food['stock'])}")
    print(f"  Status   : {status_text(food)}")
    print(f"  Describe : {food['describe']}")


def show_category(category):
    print_section(category)
    dishes = dishes_of(category)

    if len(dishes) == 0:
        print_inform("Nothing in this category today.")
        return

    print_header(["ID", "Name", "Price", "Stock", "Status"])
    for food in dishes:
        print_row(
            [
                food["id"],
                food["name"],
                format_money(food["price"]),
                format_quantity(food["stock"]),
                status_text(food),
            ]
        )


def show_menu():
    print_title("Our Menu")

    for category in all_categories:
        show_category(category)

    print()
    print_inform(f"{len(all_foods)} dishes on the menu today.")
    print_inform("Type the ID of a dish when you want to add it to your cart.")


def match_name(food, keyword):
    #不区分大小写
    return keyword.lower() in food["name"].lower()


def search_by_name(keyword):
    results = []
    for food in all_foods:
        if match_name(food, keyword):
            results.append(food)
    return results


def search_by_price(low_price, high_price):
    results = []
    for food in all_foods:
        price = food["price"]
        if price >= low_price and price <= high_price:
            results.append(food)
    return results


def search_by_category(keyword):
    results = []
    for food in all_foods:
        if keyword.lower() in food["category"].lower():
            results.append(food)
    return results


def show_results(results, title):
    print_title(title, False)

    if len(results) == 0:
        print_inform("No dish matches what you are looking for.")
        return

    print_header(["ID", "Name", "Category", "Price"])
    for food in results:
        print_row(
            [
                food["id"],
                food["name"],
                food["category"],
                format_money(food["price"]),
            ]
        )

    print()
    print_inform(f"{len(results)} dish(es) found.")


def search_menu():
    # 返回结果列表
    print_title("Search")

    print("  1. Search by name")
    print("  2. Search by price range")
    print("  3. Search by category")
    print("  0. Back")
    print_line("-")

    choice = read_int("Your choice: ", 0, 3)

    if choice == 0:
        return []

    if choice == 1:
        keyword = read_text("Type part of the dish name: ")
        results = search_by_name(keyword)
        show_results(results, f"Result of '{keyword}'")
        return results

    if choice == 2:
        low_price = read_float("Lowest price : ", 0)
        high_price = read_float("Highest price: ", low_price)
        results = search_by_price(low_price, high_price)
        show_results(results, f"Price {format_money(low_price)} - {format_money(high_price)}")
        return results

    keyword = read_text("Type part of the category name: ")
    results = search_by_category(keyword)
    show_results(results, f"Category with '{keyword}'")
    return results


def ask_food_id(prompt="Dish ID (0 to cancel): "):
    # 按 ID 取菜品，输入 0 取消，输错重问
    while True:
        text = read_text(prompt)

        if text == "0":
            return None

        food = get_food(text)

        if food is None:
            print_warning(f"There is no dish with ID '{text}'. Look at the ID column.")
            continue

        return food


def ask_dish(results):
    # 只能从给定的结果里挑
    if len(results) == 0:
        return None

    print_inform("Type the ID of the dish you want, 0 to cancel.")
    food = ask_food_id()

    if food is None:
        return None

    i = 0
    while i < len(results):
        if results[i]["id"] == food["id"]:
            return food
        i = i + 1

    print_warning("This dish is not in the list above.")
    return None
