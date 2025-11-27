import os
from supabase import create_client, Client
from dotenv import load_dotenv

#need to set up env for your db
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file")

supabase: Client = create_client(url, key)

def get_food_nutrition(food_name: str):
    try:
        response = supabase.table("foods").select("*").eq("name", food_name).execute()
        if response.data:
            return response.data[0]
        else:
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
