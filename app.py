from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk
from nltk.corpus import stopwords
from recommendation_system import initialize_recommendation_system
import os
import glob

# app.py

from flask import Flask, render_template, request, redirect, url_for
from recommendation_system import initialize_recommendation_system


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Disable template caching during development

@app.route('/')
def home():
    return render_template('index.html')


# Initialize the recommendation system and store the results globally
cosine_sim, data = initialize_recommendation_system()

# ... Rest of your Flask code ...
def get_recommendations(title, cosine_sim=cosine_sim, df=data):
    idx = df[df['Title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Top 5 similar recipes (excluding itself)
    recipe_indices = [i[0] for i in sim_scores]
    return df['Title'].iloc[recipe_indices].tolist()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        recipe_title = request.form['recipe_title']
        
        # Check if there is an exact match in the dataset
        exact_match = data[data['Title'] == recipe_title]
        
        if not exact_match.empty:
            # Redirect to the 'get_recommendations' route with the 'title' parameter
            return redirect(url_for('get_recommendations_route', title=recipe_title))
        else:
            # If no exact match, search for partial matches and get the first one
            partial_match = data[data['Title'].str.contains(recipe_title, case=False, na=False)]
            if not partial_match.empty:
                first_partial_match = partial_match.iloc[0]['Title']
                return redirect(url_for('get_recommendations_route', title=first_partial_match))
            else:
                return "Dish not found in the dataset. <a href='/'>Back to Home</a>"
    return render_template('index.html')

# Define a route for the 'get_recommendations' function
@app.route('/recommendations/<title>', methods=['GET','POST'])
def get_recommendations_route(title):
    recommendations = get_recommendations(title)
    if request.method == 'POST':
        title_new = request.form['recipeTitleInput']
        return  redirect(url_for('get_recommendations_route', title=title_new))
    return render_template('recommendations.html', recommendations=recommendations, recipe_title=title)

if __name__ == '__main__':
    app.run()

@app.route('/recipe', methods=['POST'])
def get_recipe_instructions_route():
    # Search for the recipe in the dataset based on the title
    title = request.form['title']
    recipe_data = data[data['Title'] == title]
    
    

    if not recipe_data.empty:
        # Assuming there's a column named 'Instructions' in your dataset
        instructions = recipe_data['Instructions'].iloc[0]
        first_image = recipe_data['Image_Name'].iloc[0]
        image_directory = os.path.join('static','FoodImages')

        # Use glob to search for image files with the search value in their names
        image_files = glob.glob(os.path.join(image_directory, f'*{first_image}*.jpg'))
        print('hello')
        # Check if there are matching image files
        if image_files:
            # Retrieve the first matching image file
            first_image = image_files[0]
            first_image = first_image[6:]
            print(first_image)
        # You can render an HTML template or return the instructions as plain text
        # Here's an example returning plain text:
        return render_template('instructions.html',instructions=instructions, recipe_title=title, recipe_img=first_image)
    return redirect(url_for('home'))
    
  
