# -*- coding: utf-8 -*-
"""Skincare Solution.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11hWhHTpMPv6tyWjcxn7hkvQS_Aj5_66k

# **Problem Statement**
We are a personalized skincare brand, and we are looking for someone who is skilled in using Typeform and can also create recommendation algorithms. As a specialist, your job will involve creating user-friendly Typeform surveys and forms to collect the data we need. You will also be responsible for developing and improving recommendation algorithms based on the data we collect. This will involve analyzing user preferences, behavior, and patterns to create personalized recommendations.

# **Solution**
Typeform created: Link Below
https://oroni7j6an3.typeform.com/to/MJ6DKbTd

# **Building the model**
## 1. About the Data
The dataset consists of user preferences, behavior, and attributes like age, skin type, skin concerns, allergies, and product satisfaction. This data can help you make personalized recommendations based on patterns found in similar users.
## 2. Building the Recommendation System (Content-Based Filtering)
I have chosen this type of recommendation system because it suggests products or routines based on the user's features (age group, skin type, concerns, etc.). Since we don’t have user feedback on products yet, recommending products based on the preferences of similar users won’t be possible hence Collaborative Filtering won’t be suitable.
"""

import pandas as pd
import numpy as np

skincare=pd.read_csv('/content/skincare_survey_data.csv')

# Add a user_id column to uniquely identify each user
skincare['user_id'] = skincare.index

skincare.head()

skincare.info()

skincare.isnull().sum()

skincare['Allergies/Skin Conditions'].value_counts()

#Converting categorical data into numeric values
from sklearn.preprocessing import LabelEncoder

# List of columns to encode
columns_to_encode = [
    'Gender', 'Skin Type', 'Skin Concerns', 'Breakouts Frequency', 'Allergies/Skin Conditions',
    'Skincare Products', 'Routine Frequency', 'Satisfaction with Products', 'Environment',
    'Sensitivity to New Products', 'Skin Irritation from Ingredients', 'Avoided Ingredients',
    'Skincare Goals', 'Purchase Frequency', 'Purchase Location', 'Recommendation Preference',
    'Willingness to Try New Products', 'Sunscreen Use'
]

# Initialize the LabelEncoder
label_encoder = LabelEncoder()

# Apply label encoding to each column
for column in columns_to_encode:
    skincare[column] = label_encoder.fit_transform(skincare[column])

# Check the first few rows of the updated dataframe
print(skincare.head())

#Standardizing 'Age Group' and 'Monthly Spend' columns
from sklearn.preprocessing import StandardScaler

# Map Age Group to numerical values
age_group_mapping = {
    'Under 18': 0,
    '18-25': 1,
    '26-35': 2,
    '36-45': 3,
    '46+': 4
}
skincare['Age Group'] = skincare['Age Group'].map(age_group_mapping)

# Map Monthly Spend to numerical values
monthly_spend_mapping = {
    'Less than $50': 0,
    '$50-$100': 1,
    'More than $100': 2
}
skincare['Monthly Spend'] = skincare['Monthly Spend'].map(monthly_spend_mapping)

# Initialize the StandardScaler
scaler = StandardScaler()

# Standardize the 'Age Group' and 'Monthly Spend' columns
skincare[['Age Group', 'Monthly Spend']] = scaler.fit_transform(skincare[['Age Group', 'Monthly Spend']])

# Check the first few rows of the updated dataframe
print(skincare[['Age Group', 'Monthly Spend']].head())

"""# Feature Engineering"""

#Behavior-Based Features:
#1.Create Breakout Severity by combining Breakouts Frequency and Acne Concern
skincare['Breakout Severity'] = skincare['Breakouts Frequency'] * (skincare['Skin Concerns'] == 'Acne').astype(int)

#2.Create Sensitivity Risk based on product sensitivity and irritation risk
skincare['Sensitivity Risk'] = skincare['Sensitivity to New Products'] + skincare['Skin Irritation from Ingredients']

#Product Preferences
#1.Create binary feature for moisturizer preference
skincare['Moisturizer User'] = skincare['Skincare Products'].apply(lambda x: 1 if '2' in str(x) else 0)

#2.Create a 'Heavy Routine' feature for users who use Cleanser, Moisturizer, and Sunscreen
skincare['Heavy Routine'] = skincare['Skincare Products'].apply(lambda x: 1 if all(product in str(x) for product in ['0', '2', '4']) else 0)

# Multiply Satisfaction with Routine Frequency to create a correlation feature
skincare['Satisfaction vs Routine'] = skincare['Satisfaction with Products'] * skincare['Routine Frequency']

# Multiply Satisfaction with Breakouts Frequency to create a correlation feature
skincare['Satisfaction vs Breakouts'] = skincare['Satisfaction with Products'] * skincare['Breakouts Frequency']

# Create an interaction feature between Skin Type and Sensitivity to New Products
skincare['SkinType-Sensitivity Interaction'] = skincare['Skin Type'] * skincare['Sensitivity to New Products']

#Clustering
from sklearn.cluster import KMeans

# Select routine-related features for clustering
routine_features = skincare[['Routine Frequency', 'Breakout Severity']]
kmeans = KMeans(n_clusters=3, random_state=0)
skincare['Routine Cluster'] = kmeans.fit_predict(routine_features)

# Select skin type and environment for clustering
kmeans = KMeans(n_clusters=3, random_state=0)
skincare['SkinType-Environment Cluster'] = kmeans.fit_predict(skincare[['Skin Type', 'Environment']])

# Select satisfaction and spending behavior for clustering
kmeans = KMeans(n_clusters=3, random_state=0)
skincare['Satisfaction-Spend Cluster'] = kmeans.fit_predict(skincare[['Satisfaction with Products', 'Monthly Spend']])

# prompt: download skincare as a csv file

from google.colab import files

skincare.to_csv('skincare_processed.csv', encoding = 'utf-8-sig')
files.download('skincare_processed.csv')

skincare.head()

from sklearn.metrics.pairwise import cosine_similarity
scaled_features = skincare[['Age Group', 'Monthly Spend']]

# Compute cosine similarity between users
similarity_matrix = cosine_similarity(scaled_features)

def recommend_for_user(user_id, top_n=3):
    # Get the most similar users based on the user_id
    similar_users = similarity_matrix[user_id].argsort()[-top_n-1:-1][::-1]

    # Recommend products based on similar users' preferences
    recommendations = []
    for similar_user in similar_users:
        # Collect the preferred products or routines of similar users
        recommended_products = skincare.iloc[similar_user]['Skincare Products']
        recommendations.append(recommended_products)

    return recommendations

# Example: Recommend for user with user_id = 4
print(recommend_for_user(4))

from sklearn.metrics.pairwise import cosine_similarity

scaled_features = skincare[['Age Group', 'Monthly Spend']]

# Compute cosine similarity between users
similarity_matrix = cosine_similarity(scaled_features)

# Mapping encoded values to product names
product_mapping = {
    0: 'Cleanser',
    1: 'Exfoliant',
    2: 'Moisturizer',
    3: 'Serum',
    4: 'Sunscreen',
    5: 'Toner'
}

# Mapping encoded values to Skin Concerns
skin_concerns = {
    0: 'Acne',
    1: 'Dark circle',
    2: 'Dark spots',
    3: 'Fine lines',
    4: 'Redness',
    5: 'Wrinkles'
}

def recommend_for_user(user_id, top_n=2):
    # Get the most similar users based on the user_id
    similar_users = similarity_matrix[user_id].argsort()[-top_n-1:-1][::-1]

    # Recommend products based on similar users' preferences
    recommendations = []
    for similar_user in similar_users:
        # Collect the preferred product (encoded value) of the similar user
        recommended_product_encoded = skincare.iloc[similar_user]['Skincare Products']

        # Check if the value is a single encoded product (float/int) and map it to the product name
        if isinstance(recommended_product_encoded, (int, float)):
            recommended_product = product_mapping[int(recommended_product_encoded)]
            recommendations.append(recommended_product)
        else:
            # Handle if the value is a list of products
            recommended_products = [product_mapping[product] for product in recommended_product_encoded]
            recommendations.append(recommended_products)

    return recommendations

# Example: Recommend for user with user_id = 4
recommendations = recommend_for_user(4)
for i, rec in enumerate(recommendations, start=1):
    print(f"Recommendation from similar user {i}: {rec}")

from sklearn.metrics.pairwise import cosine_similarity

# Select features for similarity computation
scaled_features = skincare[['Age Group', 'Monthly Spend']]

# Compute cosine similarity between rows (now considering Skin Concerns)
similarity_matrix = cosine_similarity(scaled_features)

# Mapping encoded values to product names
product_mapping = {
    0: 'Cleanser',
    1: 'Exfoliant',
    2: 'Moisturizer',
    3: 'Serum',
    4: 'Sunscreen',
    5: 'Toner'
}

# Mapping encoded values to Skin Concerns
skin_concerns_mapping = {
    0: 'Acne',
    1: 'Dark circle',
    2: 'Dark spots',
    3: 'Fine lines',
    4: 'Redness',
    5: 'Wrinkles'
}

def recommend_for_skin_concern(skin_concern_id, top_n=3):
    # Filter rows matching the given skin concern
    concern_indices = skincare.index[skincare['Skin Concerns'] == skin_concern_id].tolist()

    # Handle cases where no matching skin concerns are found
    if not concern_indices:
        return f"No users with the specified skin concern: {skin_concerns_mapping.get(skin_concern_id, 'Unknown')}"

    # Use the first matching row to find similar rows
    concern_idx = concern_indices[0]
    similar_indices = similarity_matrix[concern_idx].argsort()[-top_n-1:-1][::-1]

    # Recommend products based on similar rows
    recommendations = []
    for idx in similar_indices:
        recommended_product_encoded = skincare.iloc[idx]['Skincare Products']
        recommended_product = product_mapping[int(recommended_product_encoded)]
        recommendations.append(recommended_product)

    return recommendations

# Example: Recommend for skin concern ID 0 ('Acne')
skin_concern_id = 0  # Replace with desired skin concern ID
recommendations = recommend_for_skin_concern(skin_concern_id)
if isinstance(recommendations, list):
    print(f"Recommendations for skin concern '{skin_concerns_mapping[skin_concern_id]}': {recommendations}")
else:
    print(recommendations)

import pickle

with open('derma.pkl', 'wb') as f:
    pickle.dump((recommend_for_user), f)

# #Real model code
# # Get the encoded user inputs (these should have been passed to the function earlier)
# from sklearn.metrics.pairwise import cosine_similarity
# # Filter the skincare dataset based on the encoded user inputs
# filtered_data = skincare[['Gender','Skin Type','Skin Concerns']]

# similarity_matrix = cosine_similarity(filtered_data)

# # Mapping encoded values to product names
# product_mapping = {
#     0: 'Cleanser',
#     1: 'Exfoliant',
#     2: 'Moisturizer',
#     3: 'Serum',
#     4: 'Sunscreen',
#     5: 'Toner'
# }

# # If there are no exact matches, handle this case
# if filtered_data.empty:
#     print("No recommendations available for this combination.")

# # Get the first index of the filtered data as the base for similarity comparison
# base_user_index = filtered_data.index[0]

# # Find similar users based on the base user's index in the similarity matrix
# similar_users = similarity_matrix[base_user_index].argsort()[-3-1:-1][::-1]

# # Recommend products based on similar users' preferences
# recommendations = []
# for similar_user in similar_users:
#     # Collect the preferred product (encoded value) of the similar user
#     recommended_product_encoded = skincare.iloc[similar_user]['Skincare Products']

#     # Check if the value is a single encoded product (float/int) and map it to the product name
#     if isinstance(recommended_product_encoded, (int, float)):
#         recommended_product = product_mapping[int(recommended_product_encoded)]
#         recommendations.append(recommended_product)
#     else:
#         # Handle if the value is a list of products
#         recommended_products = [product_mapping[product] for product in recommended_product_encoded]
#         recommendations.append(recommended_products)

# # Return the recommendations list
# print (recommendations)

import pickle

# Save the similarity matrix and product mapping to a pickle file
with open('derma.pkl', 'wb') as f:
    # You can pickle the similarity matrix and product mapping together
    pickle.dump((similarity_matrix, product_mapping), f)