import sys
import argparse
from classifier import FoodClassifier
from database import get_food_nutrition

def main():
    parser = argparse.ArgumentParser(description='NutriCheck - Food Recognition and Nutrition Analysis')
    parser.add_argument('image_path', help='Path to the food image')
    parser.add_argument('--custom-model', help='Path to custom trained model (optional)', default=None)
    
    args = parser.parse_args()
    
    print(f"\n Analyzing image: {args.image_path}")
    print("-" * 50)
    
    classifier = FoodClassifier(custom_model_path=args.custom_model)
    
    print("\n Top predictions:")
    predictions = classifier.classify(args.image_path, top_k=3)
    
    if classifier.custom_model:
        for i, (class_name, prob) in enumerate(predictions, 1):
            print(f"  {i}. {class_name}: {prob*100:.2f}%")
    else:
        # imagenet format: (class_id, class_name, probability)
        for i, (class_id, class_name, prob) in enumerate(predictions, 1):
            print(f"  {i}. {class_name}: {prob*100:.2f}%")
    
    food_name = classifier.get_food_name(args.image_path)
    print(f"\n  Most likely food: {food_name}")
    
    print("\n   Searching database for nutritional information...")
    nutrition = get_food_nutrition(food_name)
    
    if nutrition:
        print("\n   Nutritional Information Found:")
        print("-" * 50)
        print(f"  Food: {nutrition['name']}")
        print(f"  Calories: {nutrition['calories']} kcal")
        print(f"  Protein: {nutrition['protein']}g")
        print(f"  Carbs: {nutrition['carbs']}g")
        print(f"  Fat: {nutrition['fat']}g")
        print("-" * 50)
    else:
        print(f"\n   No nutritional data found for '{food_name}' in the database.")
        print("   The food was recognized but not in our nutrition database.")
        print("   Consider adding it to the database using seed_db.py")

if __name__ == "__main__":
    main()