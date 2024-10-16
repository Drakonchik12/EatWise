import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pymongo import MongoClient
import subprocess

# Функция подключения к MongoDB и проверки учетных данных
def check_credentials(email, password):
    # Строка подключения с заменой <db_password> на ваш реальный пароль
    connection_string = "mongodb+srv://ingamatynina392:dracoshaa@cluster0.fgaoh2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    
    # Подключение к MongoDB
    client = MongoClient(connection_string)
    db = client.EatWise
    users_collection = db.users
    
    # Поиск пользователя по email
    user = users_collection.find_one({"email": email})
    
    if user:
        # Проверка пароля
        if user["password"] == password:
            return True
        else:
            return False
    else:
        return None

def on_login():
    login = entry_login.get()
    password = entry_password.get()

    # Проверка учетных данных пользователя
    result = check_credentials(login, password)
    
    if result is True:
        messagebox.showinfo("Success", "Login successful!")
        # Запуск другого файла при успешной аутентификации
        subprocess.run(["python", "another_file.py"])
    elif result is False:
        messagebox.showerror("Error", "Invalid password!")
    else:
        messagebox.showerror("Error", "User not found!")

def on_register():
    # Запуск файла регистрации
    root.destroy()
    subprocess.run(["python", "Regestration_1_.py"])
    # Закрытие текущего окна
    

root = tk.Tk()
root.title("Login Window")
root.geometry("1400x700")
root.resizable(False, False)

# Создание холста для фона
canvas = tk.Canvas(root, width=1400, height=700)
canvas.pack(fill="both", expand=True)

# Загрузка и установка фонового изображения
try:
    image = Image.open("background.png")  # Замените на путь к вашему файлу
    background_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=background_image)
except Exception as e:
    print(f"Error loading image: {e}")
    canvas.config(bg="#f0f0f0")

label_auth = tk.Label(canvas, text="Welcome to EatWise", font=("Arial", 24, "bold"), fg="black", bg="#E0E6C4")
label_auth.pack(pady=100)

label_us = tk.Label(canvas, text="Email", font=("Arial", 18, "bold"), fg="black", bg="#CFE1B9")
label_us.pack(pady=0)
entry_login = tk.Entry(canvas, width=35, font=("Arial", 24), fg="black", insertbackground="black", highlightthickness=0, bd=2)
entry_login.pack(pady=10)
entry_login.insert(0, "email@gmail.com")

label_ps = tk.Label(canvas, text="Password", font=("Arial", 18, "bold"), fg="black", bg="#B9DAAD")
label_ps.pack(pady=0)
entry_password = tk.Entry(canvas, width=35, show="*", font=("Arial", 24), fg="black", insertbackground="black", highlightthickness=0, bd=2)
entry_password.pack(pady=20)
entry_password.insert(0, "Password")

button_login = tk.Button(canvas, text="Login", width=17, font=("Arial", 16), command=on_login, bg="#0A5381", fg="white", bd=0)
button_login.pack(pady=10)

button_register = tk.Button(canvas, text="Register", width=17, font=("Arial", 16), command=on_register, bg="#0A5381", fg="white", bd=0)
button_register.pack(pady=10)

root.mainloop()
