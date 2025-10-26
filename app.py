# app.py
import streamlit as st
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Connect to MongoDB Atlas
load_dotenv()
mongo_url = os.getenv("MONGODB_CONNECTION_URL")
client = MongoClient(mongo_url)
db = client['user_age_analysis']
collection = db['users']

st.title("FinBench: User Analytics & Standing")

# User Input Form
st.header("Enter Your Details")
age = st.number_input("Age", min_value=18, max_value=100, value=30)
job = st.selectbox("Job", sorted(collection.distinct("job")))
marital = st.selectbox("Marital Status", ["married", "single", "divorced"])
housing = st.selectbox("Housing Loan", ["yes", "no"])
loan = st.selectbox("Personal Loan", ["yes", "no"])

if st.button("Check My Standing"):
    # Age Buckets
    age_buckets = [0, 18, 25, 35, 50, 100]
    age_bucket_names = ["0-17", "18-24", "25-34", "35-49", "50+"]
    
    age_bucket_agg = collection.aggregate([
        {"$bucket": {
            "groupBy": "$age",
            "boundaries": age_buckets,
            "default": "Other",
            "output": {"count": {"$sum": 1}}
        }}
    ])
    
    user_age_bucket = None
    counts = {}
    for idx, bucket in enumerate(age_bucket_agg):
        counts[age_bucket_names[idx]] = bucket['count']
        if age >= age_buckets[idx] and age < age_buckets[idx+1]:
            user_age_bucket = age_bucket_names[idx]
    
    st.write(f"Your age group: **{user_age_bucket}**")

    # Group by Job + Marital Status
    job_group = collection.aggregate([
        {"$match": {"job": job, "marital": marital}},
        {"$group": {"_id": "$job", "totalUsers": {"$sum": 1}}}
    ])
    
    total_similar = 0
    for j in job_group:
        total_similar = j['totalUsers']
    
    st.write(f"Number of users with job **{job}** and marital status **{marital}**: **{total_similar}**")

    # Chart Age Distribution
    st.bar_chart(pd.DataFrame.from_dict(counts, orient='index', columns=['Users']))
