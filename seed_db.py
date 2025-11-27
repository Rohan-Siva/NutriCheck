from database import supabase

#simple food db setup

foods_data = [
    {"name": "pizza", "calories": 266, "protein": 11, "carbs": 33, "fat": 10},
    {"name": "cheeseburger", "calories": 303, "protein": 15, "carbs": 30, "fat": 14},
    {"name": "hotdog", "calories": 290, "protein": 10, "carbs": 2, "fat": 26},
    {"name": "Granny_Smith", "calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2}, # Apple
    {"name": "strawberry", "calories": 32, "protein": 0.7, "carbs": 7.7, "fat": 0.3},
    {"name": "orange", "calories": 47, "protein": 0.9, "carbs": 12, "fat": 0.1},
    {"name": "banana", "calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3},
    {"name": "bagel", "calories": 250, "protein": 10, "carbs": 49, "fat": 1.5},
    {"name": "pretzel", "calories": 380, "protein": 9, "carbs": 80, "fat": 3},
    {"name": "mashed_potato", "calories": 88, "protein": 1.7, "carbs": 15, "fat": 2.8},
    {"name": "broccoli", "calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4},
    {"name": "cauliflower", "calories": 25, "protein": 1.9, "carbs": 5, "fat": 0.3},
    {"name": "zucchini", "calories": 17, "protein": 1.2, "carbs": 3.1, "fat": 0.3},
    {"name": "spaghetti_squash", "calories": 31, "protein": 0.6, "carbs": 7, "fat": 0.6},
    {"name": "acorn_squash", "calories": 40, "protein": 0.8, "carbs": 10, "fat": 0.1},
    {"name": "cucumber", "calories": 15, "protein": 0.7, "carbs": 3.6, "fat": 0.1},
    {"name": "bell_pepper", "calories": 20, "protein": 0.9, "carbs": 4.6, "fat": 0.2},
    {"name": "mushroom", "calories": 22, "protein": 3.1, "carbs": 3.3, "fat": 0.3},
    {"name": "corn", "calories": 86, "protein": 3.2, "carbs": 19, "fat": 1.2},
    {"name": "espresso", "calories": 9, "protein": 0.1, "carbs": 1.7, "fat": 0.2},
    {"name": "ice_cream", "calories": 207, "protein": 3.5, "carbs": 24, "fat": 11},
    {"name": "chocolate_sauce", "calories": 541, "protein": 2, "carbs": 55, "fat": 35}, # per 100g approx
    {"name": "carbonara", "calories": 580, "protein": 20, "carbs": 45, "fat": 35}, # approx per serving
    {"name": "guacamole", "calories": 160, "protein": 2, "carbs": 9, "fat": 15},
    {"name": "french_loaf", "calories": 289, "protein": 12, "carbs": 56, "fat": 1.7}
]

def seed():
    print("Seeding database...")
    for food in foods_data:
        try:
            existing = supabase.table("foods").select("*").eq("name", food["name"]).execute()
            if not existing.data:
                data = supabase.table("foods").insert(food).execute()
                print(f"Inserted: {food['name']}")
            else:
                print(f"Skipped (already exists): {food['name']}")
        except Exception as e:
            print(f"Error inserting {food['name']}: {e}")
    print("Seeding complete.")

if __name__ == "__main__":
    seed()
