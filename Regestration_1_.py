import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import csv
import pymongo
import subprocess

# Подключение к MongoDB
client = pymongo.MongoClient("mongodb+srv://ingamatynina392:dracoshaa@cluster0.fgaoh2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["EatWise"]
users_collection = db["users"]

def on_login():
    root.destroy()
    subprocess.run(["python", "Log_in.py"])

def on_register():
    # Получение данных из полей ввода
    username = entry_login.get()
    email = entry_post.get()
    password = entry_password.get()
    confirm_password = entry_password2.get()

    # Проверка заполненности полей
    if not username or not email or not password or not confirm_password:
        messagebox.showerror("Error", "All fields must be filled!")
        return

    # Проверка совпадения паролей
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    # Проверка наличия пользователя в базе данных
    existing_user = users_collection.find_one({"email": email})
    if existing_user:
        messagebox.showerror("Error", "User with this email already exists!")
        return

    # Запись данных во временный файл CSV
    with open('temp_registration_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, email, password])
    root.destroy()
    subprocess.run(["python", "Regestration_2_.py"])
    

    # Переход на следующую вкладку
    root.destroy()
    # Здесь вы можете запустить новый файл или окно, используя subprocess или другую команду
    # subprocess.run(["python", "next_window.py"])

root = tk.Tk()
root.title("Login Window")
root.geometry("1400x700")
root.resizable(False, False)

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

label_auth = tk.Label(canvas, text="Regestration to EatWise - step 1", font=("Arial", 24, "bold"), fg="black", bg="#E0E6C4")
label_auth.pack(pady=40)


label_us = tk.Label(canvas, text="Username", font=("Arial", 18, "bold"), fg="black", bg="#DEE5C3")
label_us.pack(pady=0)
entry_login = tk.Entry(canvas, width=35, font=("Arial", 24), fg="black", insertbackground="black", highlightthickness=0, bd=2)
entry_login.pack(pady=10)
entry_login.insert(0, "Username")

label_post = tk.Label(canvas, text="Email address", font=("Arial", 18, "bold"), fg="black", bg="#CFE1B9")
label_post.pack(pady=0)
entry_post = tk.Entry(canvas, width=35, font=("Arial", 24), fg="black", insertbackground="black", highlightthickness=0, bd=2)
entry_post.pack(pady=10)
entry_post.insert(0, "User@gmail.com")

label_ps = tk.Label(canvas, text="Password", font=("Arial", 18, "bold"), fg="black", bg="#C0DBB0")
label_ps.pack(pady=0)
entry_password = tk.Entry(canvas, width=35, show="*", font=("Arial", 24), fg="black", insertbackground="black", highlightthickness=0, bd=2)
entry_password.pack(pady=10)
entry_password.insert(0, "Password")

label_ps2 = tk.Label(canvas, text="Confirm password", font=("Arial", 18, "bold"), fg="black", bg="#ABD6A8")
label_ps2.pack(pady=0)
entry_password2 = tk.Entry(canvas, width=35, show="*", font=("Arial", 24), fg="black", insertbackground="black", highlightthickness=0, bd=2)
entry_password2.pack(pady=10)
entry_password2.insert(0, "Password")

button_register = tk.Button(canvas, text="Register", width=17, font=("Arial", 16), command=on_register, bg="#0A5381", fg="white", bd=0)
button_register.pack(pady=10)

button_login = tk.Button(canvas, text="Login", width=17, font=("Arial", 16), command=on_login, bg="#0A5381", fg="white", bd=0)
button_login.pack(pady=10)

root.mainloop()
