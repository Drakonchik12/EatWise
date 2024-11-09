import csv
import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# Function to read the user's email from temp.csv
def get_user_email_from_csv():
    with open('temp.csv', newline='') as file:
        reader = csv.reader(file)
        user_nickname = next(reader)[0]
    return user_nickname

# MongoDB connection
client = MongoClient("mongodb+srv://ingamatynina392:dracoshaa@cluster0.fgaoh2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["EatWise"]

# Function to load and display user information
def load_user_info():
    user_email = get_user_email_from_csv()
    if not user_email:
        return
    
    user = db["users"].find_one({"email": user_email})
    if not user:
        messagebox.showerror("Error", "User not found!")
        return
    
    # Display user information
    username_label.config(text=f"Username: {user['username']}")
    email_label.config(text=f"Email: {user['email']}")
    dob_label.config(text=f"Date of Birth: {user['date_of_birth']}")
    height_label.config(text=f"Height: {user['height']} cm")
    weight_label.config(text=f"Weight: {user['weight']} kg")
    gender_label.config(text=f"Gender: {user['gender']}")
    diet_type_label.config(text=f"Diet Type: {user['diet_type']}")
    calories_label.config(text=f"Daily Caloric Need: {user['calories']} kcal")

# Function to open user editing window
def open_edit_user_window():
    edit_window = tk.Toplevel(app)
    edit_window.title("Edit User Information")
    # Placeholder for edit functionality
    tk.Label(edit_window, text="Edit functionality coming soon!").pack()

# Function to open statistics window
def open_statistics_window():
    stats_window = tk.Toplevel(app)
    stats_window.title("Statistics")
    # Placeholder for statistics functionality
    tk.Label(stats_window, text="Statistics functionality coming soon!").pack()

# Main application window
app = tk.Tk()
app.title("Account")
app.geometry("600x500")
app.configure(bg='#E0E6C4')

# Frame for user information
info_frame = tk.Frame(app, bg='#ffffff', bd=1, relief=tk.GROOVE)
info_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)

# Header label for "Account"
account_header = tk.Label(info_frame, text="Account", bg='#ffffff', font=("Arial", 16, 'bold'))
account_header.pack(pady=10)

# Display user statistics labels
username_label = tk.Label(info_frame, text="Username: ", bg='#ffffff', font=("Arial", 12))
email_label = tk.Label(info_frame, text="Email: ", bg='#ffffff', font=("Arial", 12))
dob_label = tk.Label(info_frame, text="Date of Birth: ", bg='#ffffff', font=("Arial", 12))
height_label = tk.Label(info_frame, text="Height: ", bg='#ffffff', font=("Arial", 12))
weight_label = tk.Label(info_frame, text="Weight: ", bg='#ffffff', font=("Arial", 12))
gender_label = tk.Label(info_frame, text="Gender: ", bg='#ffffff', font=("Arial", 12))
diet_type_label = tk.Label(info_frame, text="Diet Type: ", bg='#ffffff', font=("Arial", 12))
calories_label = tk.Label(info_frame, text="Daily Caloric Need: ", bg='#ffffff', font=("Arial", 12))

for widget in [username_label, email_label, dob_label, height_label, weight_label, gender_label, diet_type_label, calories_label]:
    widget.pack(anchor='w', padx=10, pady=5)

# Frame to hold the buttons horizontally
buttons_frame = tk.Frame(info_frame, bg='#ffffff')
buttons_frame.pack(pady=10)

# Load user information on startup
load_user_info()

# Run application
app.mainloop()
