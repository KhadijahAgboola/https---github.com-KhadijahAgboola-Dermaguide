import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

skincare = pd.read_csv("C:\\Users\\Khadijat Agboola\\desktop\\Dermaguide\\skincare_data.csv")
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

# Select features for similarity computation
scaled_features = skincare[['Age Group', 'Monthly Spend']]

# Compute cosine similarity between rows
similarity_matrix = cosine_similarity(scaled_features)

# Function to recommend products
def recommend_for_skin_concern(skin_concern_id, top_n=2):
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

# Streamlit App Design
st.markdown(
    """
    <style>
        .stApp {
            background-color: #998577;
            color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title

st.title("Welcome to the Skincare Recommendation App🌸")
st.subheader("About the Developer")
st.write(
    """
    Hi, I am **Khadijat Agboola**, an expert in Machine Learning and Artificial Intelligence.  
    This app is designed to address a problem faced by a skincare brand by recommending suitable skincare products based on your skin concerns.  
    
    Whether you're dealing with acne, dark circle, dark spots or fine lines, this app is here to help you find the perfect product for your skin type and needs.
    
    """
)

# Skin Concern Dropdown
skin_concern = st.selectbox(
    "**What is your Skin Concern?**",
    options=["Select your skin concern"] + list(skin_concerns_mapping.keys()),
    format_func=lambda x: skin_concerns_mapping[x] if x in skin_concerns_mapping else x
)

# CSS to style the Streamlit success and error components
st.markdown(
    """
    <style>
        .stAlert {
            background-color: #998577; /* Match this to your page's background */
            color: black; /* Adjust text color for readability */
            border-radius: 5px;
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Recommendation Button
if st.button("Get Recommendations"):
    recommendations = recommend_for_skin_concern(skin_concern)
    if isinstance(recommendations, list):
        st.markdown(
            f"""<div class="stAlert">
                <strong>These are the recommended products for {skin_concerns_mapping[skin_concern]}:</strong>
                {', '.join(recommendations)}
            </div>""",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""<div class="stAlert">
                <strong>Error:</strong> {recommendations}
            </div>""",
            unsafe_allow_html=True
        )