#data_source part
#Storing food data: using lists and dictionaries
#About our dishes:
#food_name:names of the dishes
#category:categories of the dishes 
#price:the price of the dish
#stock:the stock of the remaining dishes 
#describe:the descirbes of the dish
#id:the unique number of the dish, used by the cart, the bill and the menu
#available:True = we sell it today, False = we do not sell it today

#Food categories:
category_food = "main food"
category_drink = "drinks"
category_dessert = "desserts"
category_snack = "snacks"

#the display turns:
all_categories = [
    category_food,
    category_drink,
    category_dessert,
    category_snack,
]

#Full Menu Display :
Menu = {
    category_food: [
        {
            "id":"M01",
            "name":"Beef burger",
            "category": category_food,
            "price":15.0,
            "stock":500,
            "describe":"Handmade beef patties.",
            "available":True,
        },
        {
            "id":"M02",
            "name":"Cheese Pizza",
            "category": category_food,
            "price":38.0,
            "stock":500,
            "describe":"Bacon with cheese.",
            "available":True,
        },
        {
            "id":"M03",
            "name":"Tomato meat sauce pasta",
            "category": category_food,
            "price":25.0,
            "stock":500,
            "describe":"nothing.",
            "available":True,
        },
        {
            "id":"M04",
            "name":"Traditional steak",
            "category": category_food,
            "price":30.0,
            "stock":500,
            "describe":"nothing.",
            "available":True,
        },
    ],

    category_drink: [
        {
            "id":"D01",
            "name":"Coca-cola",
            "category": category_drink,
            "price":6.0,
            "stock":500,
            "describe":"330ml,ice/room temperature",
            "available":True,
        },
        {
            "id":"D02",
            "name":"lemonade",
            "category": category_drink,
            "price":12.0,
            "stock":420,
            "describe":"300ml,ice/hot",
            "available":True,
        },
        {
            "id":"D03",
            "name":"milk tea",
            "category": category_drink,
            "price":10.0,
            "stock":500,
            "describe":"only for hot drink",
            "available":True,
        },
        {
            "id":"D04",
            "name":"Coffee",
            "category": category_drink,
            "price":11.0,
            "stock":400,
            "describe":"a little bitter.",
            "available":True,
        },
    ],

    category_snack: [
        {
            "id":"S01",
            "name":"French fries",
            "category":category_snack,
            "price":8.0,
            "stock":600,
            "describe":"Crispy,with ketchup.",
            "available":True,
        },
        {
            "id":"S02",
            "name":"Chicken wings",
            "category": category_snack,
            "price":14.0,
            "stock":300,
            "describe":"Spicy or original taste.",
            "available":True,
        },
        {
            "id":"S03",
            "name":"Onion rings",
            "category": category_snack,
            "price":9.0,
            "stock":350,
            "describe":"Crispy golden onion rings.",
            "available":True,
        },
        {
            "id":"S04",
            "name":"Popcorn chicken",
            "category": category_snack,
            "price":12.0,
            "stock":280,
            "describe":"Mini crispy chicken nuggets.",
            "available":True,
        },
    ],

    category_dessert:[
        {
            "id":"W01",
            "name":"Tiramisu",
            "category": category_dessert,
            "price":18.0,
            "stock":200,
            "describe":"Classic Italian coffee dessert.",
            "available":True,
        },
        {
            "id":"W02",
            "name":"Mango Mousse",
            "category": category_dessert,
            "price":16.0,
            "stock":150,
            "describe":"Fresh mango flavor, cold.",
            "available":True,
        },
        {
            "id":"W03",
            "name":"Chocolate Lava Cake",
            "category": category_dessert,
            "price":20.0,
            "stock":120,
            "describe":"Warm center with flowing chocolate sauce.",
            "available":True,
        },
        {
            "id":"W04",
            "name":"Vanilla Panna Cotta",
            "category": category_dessert,
            "price":17.0,
            "stock":180,
            "describe":"Silky vanilla jelly with berry jam.",
            "available":True,
        },
    ],
}

# 1. A flat list of every dish, in the display order of all_categories
#    The menu, the search and the recommendation all walk through this list.
# ============================================================================
all_foods = []
for _category in all_categories:
    for _food in Menu[_category]:
        all_foods.append(_food)


# 2. Find one dish by its id, return None when there is no such dish
# ============================================================================
def get_food(food_id):
    if food_id is None:
        return None

    key = str(food_id).strip().upper()
    for food in all_foods:
        if food["id"].upper() == key:
            return food
    return None


# 3. How many dishes we sell today
# ============================================================================
def available_count():
    total = 0
    for food in all_foods:
        if food["available"]:
            total = total + 1
    return total