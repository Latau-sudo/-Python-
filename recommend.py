# recommend part

from data_source import (
    all_foods,
    category_food,
    category_drink,
    category_dessert,
    category_snack,
)
from utils import (
    print_title,
    print_header,
    print_row,
    print_inform,
    print_line,
    format_money,
)

MAX_TIPS = 3


def category_quantity(cart, category):
    total = 0
    for item in cart:
        if item["food"]["category"] == category:
            total = total + item["quant"]
    return total


def is_in_cart(cart, food_id):
    for item in cart:
        if item["food"]["id"] == food_id:
            return True
    return False


def has_name(cart, keyword):
    for item in cart:
        if keyword.lower() in item["food"]["name"].lower():
            return True
    return False


def find_dish(keyword, category=None):
    # 只挑还能卖的菜
    for food in all_foods:
        if not food["available"] or food["stock"] <= 0:
            continue
        if category is not None and food["category"] != category:
            continue
        if keyword.lower() in food["name"].lower():
            return food
    return None


def add_tip(tips, food, reason):
    if food is None:
        return

    for tip in tips:
        if tip["food"]["id"] == food["id"]:
            return

    if len(tips) < MAX_TIPS:
        tips.append({"food": food, "reason": reason})


def suggest(cart):
    # 返回 [{"food": 菜品, "reason": 理由}]，最多 MAX_TIPS 条
    tips = []

    if len(cart) == 0:
        add_tip(tips, find_dish("Cheese Pizza"), "Our most ordered main dish, a good start.")
        add_tip(tips, find_dish("Coca-cola"), "Ice cold, goes with almost everything.")
        add_tip(tips, find_dish("Tiramisu"), "A classic dessert to close the meal.")
        return tips

    main_num = category_quantity(cart, category_food)
    drink_num = category_quantity(cart, category_drink)
    dessert_num = category_quantity(cart, category_dessert)
    snack_num = category_quantity(cart, category_snack)

    # 有炸鸡配可乐
    if has_name(cart, "chicken") and not is_in_cart(cart, "D01"):
        add_tip(tips, find_dish("Coca-cola"), "Fried chicken and ice-cold cola is a classic pair.")

    # 有主食没饮品
    if main_num > 0 and drink_num == 0:
        add_tip(tips, find_dish("lemonade"), "A main course is heavy, a cold lemonade cleans the mouth.")

    # 有主食没甜点
    if main_num > 0 and dessert_num == 0:
        add_tip(tips, find_dish("Tiramisu"), "Finish a main course with something sweet.")

    # 有甜点没饮品
    if dessert_num > 0 and drink_num == 0:
        add_tip(tips, find_dish("Coffee"), "Coffee is the classic partner of a dessert.")

    # 只有小吃甜点，缺主食
    if main_num == 0 and (snack_num > 0 or dessert_num > 0):
        add_tip(tips, find_dish("Beef burger"), "You only picked snacks, a main dish will fill you up.")

    # 只有饮品
    if main_num == 0 and snack_num == 0 and dessert_num == 0 and drink_num > 0:
        add_tip(tips, find_dish("French fries"), "French fries are the easiest thing to eat with a drink.")

    return tips


def show_recommend(cart):
    # 打印并返回推荐列表
    print_title("Recommendation")

    tips = suggest(cart)

    if len(tips) == 0:
        print_inform("Your cart already looks complete, enjoy your meal!")
        return []

    print_header(["ID", "Name", "Category", "Price"])
    i = 0
    while i < len(tips):
        food = tips[i]["food"]
        print_row(
            [
                food["id"],
                food["name"],
                food["category"],
                format_money(food["price"]),
            ]
        )
        print(f"      Why: {tips[i]['reason']}")
        i = i + 1

    print_line("-")
    print_inform(f"{len(tips)} suggestion(s) based on what is in your cart.")
    return tips
