import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import csv
from pymongo import MongoClient
import pymongo
from CalorieCalculation import calculate_calories
import subprocess



# MongoDB setup
client = pymongo.MongoClient("mongodb+srv://ingamatynina392:dracoshaa@cluster0.fgaoh2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["EatWise"]
collection = db["users"]

years = list(range(1980, 2025))  # Years from 1950 to 2024
months = list(range(1, 13))  # 1-12 for months
days = list(range(1, 32))  # 1-31 for days

genders = ["Male", "Female"]
diet_types = ["loss", "maintenance", "gain"]

def validate_float_input(value_if_allowed):
    if value_if_allowed == "" or value_if_allowed == ".":
        return True
    try:
        float(value_if_allowed)
        return True
    except ValueError:
        return False
    


def read_csv_data():
    try:
        with open('temp_registration_data.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Ensure row is not empty
                    username, email, password = row[:3]  # Assuming the first 3 columns are username, email, and password
                    return username, email, password
    except FileNotFoundError:
        messagebox.showwarning("File Error", "CSV file not found!")
        return None, None, None

def clear_csv_file():
    with open('temp_registration_data.csv', mode='w', newline='') as file:
        file.truncate()  # Removes all content
    print("CSV file has been cleared.")

# Function to save data to CSV and MongoDB
def on_register():
    # Get username, email, and password from CSV
    username, email, password = read_csv_data()

    # Get data from entry fields
    selected_year = year_var.get()
    selected_month = month_var.get()
    selected_day = day_var.get()

    # Check if the date is fully selected
    if selected_year != "Year" and selected_month != "Month" and selected_day != "Day":
        # Combine the selected year, month, and day into a string
        dob = f"{selected_year}-{selected_month}-{selected_day}"

    height = entry_post.get()
    weight = entry_password.get()
    gender = gender_var.get()
    diet_type = diet_var.get()

    # Ensure CSV data and entry fields are populated
    if username and email and password and dob and height and weight and gender and diet_type:
        # Save the combined data to MongoDB
        calories = calculate_calories(gender, height, weight, dob, diet_type)
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "date_of_birth": dob,
            "height": height,
            "weight": weight,
            "gender": gender,
            "diet_type": diet_type,
            "calories": calories,
        }
        collection.insert_one(user_data)
        
        with open('temp.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username])

        messagebox.showinfo("Success", "Data saved to MongoDB!")
        root.destroy()
        subprocess.run(["python", "LogIn.py"]) 
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields")
        
       

root = tk.Tk()
root.title("Login Window")
root.geometry("1400x700")
root.resizable(False, False)



vcmd = (root.register(validate_float_input), '%P')

# Create a canvas to hold the background image
canvas = tk.Canvas(root, width=1400, height=700)
canvas.pack(fill="both", expand=True)

# Load and set the background image using Pillow
try:
    image = Image.open("background.png")  # Replace with your file path
    background_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=background_image)
except Exception as e:
    print(f"Error loading image: {e}")
    canvas.config(bg="#f0f0f0")

label_auth = tk.Label(canvas, text="Registration to EatWise - Step 2 \n Information about you", font=("Arial", 24, "bold"), fg="black", bg="#E0E6C4")
label_auth.place(relx=0.5, y=50, anchor="center")

# Date of Birth
label_us = tk.Label(canvas, text="Date of Birth", font=("Arial", 18, "bold"), fg="black", bg="#DEE5C3")
label_us.place(relx=0.5, y=150, anchor="center")

# Frame to hold the date dropdowns in a row
date_frame = tk.Frame(canvas, bg="#DEE5C3")
date_frame.place(relx=0.5, y=200, anchor="center")

# Combobox for Year
year_var = tk.StringVar()
year_combo = ttk.Combobox(date_frame, textvariable=year_var, values=years, font=("Arial", 14), width=8)
year_combo.set("Year")
year_combo.pack(side="left", padx=5)

# Combobox for Month
month_var = tk.StringVar()
month_combo = ttk.Combobox(date_frame, textvariable=month_var, values=months, font=("Arial", 14), width=8)
month_combo.set("Month")
month_combo.pack(side="left", padx=5)

# Combobox for Day
day_var = tk.StringVar()
day_combo = ttk.Combobox(date_frame, textvariable=day_var, values=days, font=("Arial", 14), width=8)
day_combo.set("Day")
day_combo.pack(side="left", padx=5)

# Height
label_post = tk.Label(canvas, text="Height", font=("Arial", 18, "bold"), fg="black", bg="#CFE1B9")
label_post.place(relx=0.5, y=250, anchor="center")
entry_post = tk.Entry(canvas, width=35, font=("Arial", 18), fg="black", insertbackground="black", highlightthickness=0, bd=2, validatecommand=vcmd)
entry_post.place(relx=0.5, y=290, anchor="center")

# Weight
label_ps = tk.Label(canvas, text="Weight", font=("Arial", 18, "bold"), fg="black", bg="#C0DBB0")
label_ps.place(relx=0.5, y=340, anchor="center")
entry_password = tk.Entry(canvas, width=35, font=("Arial", 18), fg="black", insertbackground="black", highlightthickness=0, bd=2, validatecommand=vcmd)
entry_password.place(relx=0.5, y=380, anchor="center")

# Gender Dropdown
label_p = tk.Label(canvas, text="Gender", font=("Arial", 18, "bold"), fg="black", bg="#ABD6A8")
label_p.place(relx=0.5, y=430, anchor="center")
gender_var = tk.StringVar()
gender_combo = ttk.Combobox(canvas, textvariable=gender_var, values=genders, font=("Arial", 14), width=20)
gender_combo.set("Select Gender")
gender_combo.place(relx=0.5, y=470, anchor="center")

# Type of Diet Dropdown
label_ = tk.Label(canvas, text="Type of Diet", font=("Arial", 18, "bold"), fg="black", bg="#99D09F")
label_.place(relx=0.5, y=520, anchor="center")
diet_var = tk.StringVar()
diet_combo = ttk.Combobox(canvas, textvariable=diet_var, values=diet_types, font=("Arial", 14), width=20)
diet_combo.set("Select Diet Type")
diet_combo.place(relx=0.5, y=560, anchor="center")

# Ready button
button_login = tk.Button(canvas, text="Ready", width=17, font=("Arial", 16), command=on_register, bg="#0A5381", fg="white", bd=0)
button_login.place(relx=0.5, y=610, anchor="center")

root.mainloop()
