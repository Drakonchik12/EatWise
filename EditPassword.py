import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
import csv

# Подключение к MongoDB
def connect_to_mongo():
    connection_string = "mongodb+srv://ingamatynina392:dracoshaa@cluster0.fgaoh2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(connection_string)
    db = client.EatWise
    return db.users

# Функция для изменения пароля
def change_password(email, old_password, new_password, confirm_password):
    users_collection = connect_to_mongo()
    user = users_collection.find_one({"email": email})

    if not user:
        messagebox.showerror("Error", "User not found!")
        return False

    if user["password"] != old_password:
        messagebox.showerror("Error", "Old password is incorrect!")
        return False

    if new_password != confirm_password:
        messagebox.showerror("Error", "New passwords do not match!")
        return False

    # Обновление пароля
    users_collection.update_one({"email": email}, {"$set": {"password": new_password}})
    messagebox.showinfo("Success", "Password changed successfully!")
    return True

# Загрузка email из файла temp.csv
def get_email_from_file():
    try:
        with open('temp.csv', 'r') as file:
            reader = csv.reader(file)
            return next(reader)[0]
    except Exception as e:
        print(f"Error reading email from file: {e}")
        return None

# Функция для обработки нажатия кнопки смены пароля
def on_change_password():
    old_password = entry_old_password.get()
    new_password = entry_new_password.get()
    confirm_password = entry_confirm_password.get()

    if change_password(email, old_password, new_password, confirm_password):
        root.destroy()

# Создание графического интерфейса
root = tk.Tk()
root.title("Change Password")
root.geometry("500x400")
root.resizable(False, False)
root.config(bg='#E0E6C4')

email = get_email_from_file()

# Проверка, если email загружен
if not email:
    messagebox.showerror("Error", "No email found. Please log in again.")
    root.destroy()

# Поля для смены пароля
tk.Label(root, text="Change Password", font=("Arial", 18, "bold"), bg='#E0E6C4').pack(pady=20)

tk.Label(root, text="Old Password", font=("Arial", 14), bg='#E0E6C4').pack(pady=5)
entry_old_password = tk.Entry(root, width=30, show="*", font=("Arial", 14))
entry_old_password.pack(pady=5)

tk.Label(root, text="New Password", font=("Arial", 14),bg='#E0E6C4').pack(pady=5)
entry_new_password = tk.Entry(root, width=30, show="*", font=("Arial", 14))
entry_new_password.pack(pady=5)

tk.Label(root, text="Confirm New Password", font=("Arial", 14),bg='#E0E6C4').pack(pady=5)
entry_confirm_password = tk.Entry(root, width=30, show="*", font=("Arial", 14))
entry_confirm_password.pack(pady=5)

# Кнопка для изменения пароля
button_change_password = tk.Button(root, text="Change Password", command=on_change_password, font=("Arial", 14), bg="#0A5381", fg="white")
button_change_password.pack(pady=20)

root.mainloop()
