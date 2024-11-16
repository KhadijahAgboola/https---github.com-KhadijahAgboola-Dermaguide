import pickle
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the similarity matrix and product mapping from the pickle file
model = pickle.load(open('derma.pkl', 'rb'))
similarity_matrix, product_mapping = model  # Unpack the tuple

# Load the skincare product dataset
skincare = pd.read_csv('skincare.csv')  # Make sure 'skincare.csv' exists and has the correct format

# Function to recommend products (though it's not necessary to use a function, I kept it to maintain the recommendation logic)
def recommend_for_user(user_id, top_n=2):
    try:
        # Get the most similar users based on the user_id
        similar_users = similarity_matrix[user_id].argsort()[-top_n-1:-1][::-1]
        
        # Collect product recommendations based on the similar users' preferences
        recommendations = []
        for similar_user in similar_users:
            # Get the preferred product (encoded value) of the similar user
            recommended_product_encoded = skincare.iloc[similar_user]['Skincare Products']
            
            # If it's a single product (int or float), map it to the product name
            if isinstance(recommended_product_encoded, (int, float)):
                recommended_product = product_mapping[int(recommended_product_encoded)]
                recommendations.append(recommended_product)
            else:
                # If it's a list of products, handle that case
                recommended_products = [product_mapping[product] for product in recommended_product_encoded]
                recommendations.append(recommended_products)
        
        return recommendations
    except IndexError:
        return ["Invalid User ID. Please try again."]

@app.route('/')
def index():
    # Render the home page with no recommendations initially
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the user ID from the form
        user_id = int(request.form.get('user_id'))
        
        # Get product recommendations for the user
        recommendations = recommend_for_user(user_id)
        
        # Pass the recommendations to the HTML page
        return render_template('index.html', recommendations=recommendations)
    except Exception as e:
        # Handle exceptions and display error
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)

