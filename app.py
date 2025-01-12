from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# TheMealDB API URL
BASE_URL = 'https://www.themealdb.com/api/json/v1/1'

# Main route for the app
@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = []
    search_query = ''
    
    if request.method == 'POST':
        # If the form is submitted
        search_query = request.form.get('search_query', '')
        recipes = search_recipes(search_query)
    
    return render_template('index.html', recipes=recipes, search_query=search_query)

# Function to search recipes based on query
def search_recipes(query):
    url = f'{BASE_URL}/search.php'
    params = {'s': query}  # 's' is the search parameter for meal name
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('meals', [])
        else:
            print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
            return []
    except Exception as e:
        print(f"Error fetching recipes: {e}")
        return []

# Route to view the details of a specific recipe
@app.route('/meal/<meal_id>')
def view_meal(meal_id):
    url = f'{BASE_URL}/lookup.php'
    params = {'i': meal_id}  # 'i' is the ingredient ID to fetch details
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            meal_data = response.json()
            
            if 'meals' in meal_data and meal_data['meals']:
                meal = meal_data['meals'][0]
                return render_template('view_meal.html', meal=meal)
            else:
                return "Meal not found", 404
        else:
            print(f"Error: Unable to fetch meal details (Status Code: {response.status_code})")
            return f"Error fetching meal details", 500
    except Exception as e:
        return f"Error fetching meal data: {e}", 500

