# load_bank_data.py
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
mongo_url = os.getenv("MONGODB_CONNECTION_URL")
client = MongoClient(mongo_url)
db = client['user_age_analysis']
collection = db['users']

# Load Bank Marketing dataset
df = pd.read_csv("data/bank-additional-full.csv", sep=";")

# Optional: select only relevant fields
df = df[['age', 'job', 'marital', 'housing', 'loan']]

# Convert to list of dicts
records = df.to_dict(orient='records')

# Insert into MongoDB only if collection is empty
if collection.count_documents({}) == 0:
    collection.insert_many(records)
    print("Bank Marketing dataset inserted successfully!")
else:
    print("Dataset already exists in MongoDB.")
