import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import requests
import csv
from pymongo import MongoClient
from datetime import datetime


connection_string = "mongodb+srv://ingamatynina392:dracoshaa@cluster0.fgaoh2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# Подключение к MongoDB
client = MongoClient(connection_string)
db = client.EatWise
collection = db.addfood
# Open Food Facts API URL for searching food by barcode or generic keyword
API_URL = "https://world.openfoodfacts.org/cgi/search.pl"

# Function to call the Open Food Facts API and get food data
def search_food():
    query = entry.get().strip()
    if not query:
        return

    params = {
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }
    
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        products = data.get('products', [])
        
        # Clear previous search results
        tree.delete(*tree.get_children())
        
        # Populate TreeView with results
        for product in products:
            name = product.get('product_name', 'N/A')
            brand = product.get('brands', 'N/A')
            categories = product.get('categories', 'N/A')
            nutriments = product.get('nutriments', {})

            calories = nutriments.get('energy-kcal_100g', 'N/A')
            protein = nutriments.get('proteins_100g', 'N/A')
            fat = nutriments.get('fat_100g', 'N/A')
            carbs = nutriments.get('carbohydrates_100g', 'N/A')
            
            tree.insert('', tk.END, values=(name, brand, categories, calories, protein, fat, carbs))
        
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"An error occurred: {e}")

# Function to read the user nickname from temp.csv
def get_user_nickname():
    with open("temp.csv", "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
    return rows[0][0] if rows else "Unknown User"

# Function to read the date from temp2.csv
def get_date():
    with open("temp2.csv", "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
    return rows[0][0] if rows else datetime.now().strftime("%Y-%m-%d")

# Function to add selected product's PFC and calorie data to MongoDB
def add_pfc_calories():
    selected_item = tree.selection()
    if not selected_item:
        return

    item = tree.item(selected_item[0])
    name, brand, categories, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g = item['values']
    
    if calories_per_100g == 'N/A':
        messagebox.showerror("Calorie Information", "Calorie information is not available for this product.")
        return

    try:
        weight = float(simpledialog.askstring("Enter Weight", f"Enter the weight of {name} in grams:"))
        
        # Calculate total PFC and calories based on weight
        total_calories = (weight * float(calories_per_100g)) / 100 if calories_per_100g != 'N/A' else 'N/A'
        total_protein = (weight * float(protein_per_100g)) / 100 if protein_per_100g != 'N/A' else 'N/A'
        total_fat = (weight * float(fat_per_100g)) / 100 if fat_per_100g != 'N/A' else 'N/A'
        total_carbs = (weight * float(carbs_per_100g)) / 100 if carbs_per_100g != 'N/A' else 'N/A'
        
        messagebox.showinfo(
            "Nutritional Calculation", 
            f"For {weight}g of {name}:\n"
            f"Total Calories: {total_calories:.2f} kcal\n"
            f"Total Protein: {total_protein:.2f} g\n"
            f"Total Fat: {total_fat:.2f} g\n"
            f"Total Carbohydrates: {total_carbs:.2f} g"
        )

        # Get user nickname and date
        user_nickname = get_user_nickname()
        date = get_date()

        # Store data in MongoDB
        food_data = {
            "user_nickname": user_nickname,
            "product_name": name,
            "calories": total_calories,
            "protein": total_protein,
            "fat": total_fat,
            "carbs": total_carbs,
            "date": date
        }
        
        collection.insert_one(food_data)
       
        
    except (ValueError, TypeError):
        messagebox.showerror("Input Error", "Please enter a valid number for weight.")

# Set up the main window
root = tk.Tk()
root.title("Food Search App with PFC")
root.geometry("800x500")
root.config(bg='#135670')

frame = tk.Frame(root)
frame.pack(pady=10)
label = tk.Label(frame, text="Enter Food Name:")
label.pack(side=tk.LEFT)
entry = tk.Entry(frame, width=30)
entry.pack(side=tk.LEFT, padx=10)

search_button = tk.Button(root, text="Search", command=search_food)
search_button.pack(pady=10)

columns = ("Name", "Brand", "Categories", "Calories per 100g", "Protein per 100g", "Fat per 100g", "Carbs per 100g")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Name", text="Name")
tree.heading("Brand", text="Brand")
tree.heading("Categories", text="Categories")
tree.heading("Calories per 100g", text="Calories per 100g (kcal)")
tree.heading("Protein per 100g", text="Protein per 100g (g)")
tree.heading("Fat per 100g", text="Fat per 100g (g)")
tree.heading("Carbs per 100g", text="Carbs per 100g (g)")
tree.pack(fill=tk.BOTH, expand=True)

add_button = tk.Button(root, text="Add Selected Product", command=add_pfc_calories)
add_button.pack(pady=10)

root.mainloop()
