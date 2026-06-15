import pandas as pd
import random
import datetime

foods = {
    "Dairy": ["Milk", "Yogurt", "Cheese", "Butter"],
    "Fruit": ["Apple", "Banana", "Orange", "Grapes"],
    "Vegetables": ["Lettuce", "Carrot", "Tomato", "Cucumber"],
    "Meat": ["Chicken", "Beef", "Pork", "Turkey"],
    "Grains": ["Rice", "Bread", "Pasta", "Oats"],
    "Other": ["Juice", "Eggs", "Sauce", "Nuts"]
}

rows = []

today = datetime.date.today()

for _ in range(200):
    category = random.choice(list(foods.keys()))
    food = random.choice(foods[category])
    quantity = random.randint(1, 10)

    days_offset = random.randint(-5, 20)
    expiration = today + datetime.timedelta(days=days_offset)

    rows.append({
        "Food": food,
        "Quantity": quantity,
        "Category": category,
        "Expiration": str(expiration)
    })

df = pd.DataFrame(rows)
df.to_csv("inventory.csv", index=False)

print("Created inventory.csv with 200 rows")
