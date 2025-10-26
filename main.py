# main.py
# For data/users.json

from pymongo import MongoClient
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

# Connect to MongoDB Atlas
load_dotenv()

mongo_url = os.getenv("MONGODB_CONNECTION_URL")

client = MongoClient(mongo_url)
db = client['user_age_analysis']
collection = db['users']

# Insert Sample Dataset (Run only once)
if collection.count_documents({}) == 0:
    users = [
        { "name": "Alice", "age": 23, "country": "USA" },
        { "name": "Bob", "age": 37, "country": "India" },
        { "name": "Charlie", "age": 15, "country": "USA" },
        { "name": "David", "age": 45, "country": "UK" },
        { "name": "Eva", "age": 60, "country": "India" },
        { "name": "Frank", "age": 29, "country": "USA" },
        { "name": "Grace", "age": 52, "country": "UK" }
    ]
    collection.insert_many(users)
    print("Dataset inserted successfully into MongoDB Atlas!")

# Aggregation: Group by Country
country_group = collection.aggregate([
    {"$group": {"_id": "$country", "totalUsers": {"$sum": 1}, "avgAge": {"$avg": "$age"}}}
])

countries = []
total_users = []
for item in country_group:
    countries.append(item['_id'])
    total_users.append(item['totalUsers'])

# Plot users per country
plt.figure(figsize=(6,4))
plt.bar(countries, total_users, color='skyblue')
plt.title("Users per Country")
plt.xlabel("Country")
plt.ylabel("Number of Users")
plt.show()

# Aggregation: Bucket by Age
age_bucket = collection.aggregate([
    {"$bucket": {
        "groupBy": "$age",
        "boundaries": [0, 18, 35, 60, 100],
        "default": "Other",
        "output": {"count": {"$sum": 1}, "users": {"$push": "$name"}}
    }}
])

# Prepare bucket data for plotting
buckets = ["0-17", "18-34", "35-59", "60+"]
counts = []

for bucket in age_bucket:
    counts.append(bucket['count'])

# Plot users per age bucket
plt.figure(figsize=(6,4))
plt.bar(buckets, counts, color='lightgreen')
plt.title("Users Age Distribution")
plt.xlabel("Age Buckets")
plt.ylabel("Number of Users")
plt.show()

# Optional: Print Age Bucket Details
age_bucket = collection.aggregate([
    {"$bucket": {
        "groupBy": "$age",
        "boundaries": [0, 18, 35, 60, 100],
        "default": "Other",
        "output": {"count": {"$sum": 1}, "users": {"$push": "$name"}}
    }}
])

print("\nAge Bucket Details:")
for bucket in age_bucket:
    print(bucket)

