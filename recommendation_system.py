# recommendation_system.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk
from nltk.corpus import stopwords

def initialize_recommendation_system():
    # Download NLTK stop words (if not already downloaded)
    #nltk.download('stopwords')

    # Load the dataset (replace 'your_dataset.csv' with your actual dataset)
    data = pd.read_csv('FoodIngredients.csv', index_col=0)

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['Cleaned_Ingredients'])

    # Calculate cosine similarities between recipes based on TF-IDF vectors
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    return cosine_sim, data
