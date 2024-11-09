import csv
import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from CalorieCalculation import calculate_calories  # Предполагаем, что у вас есть такая функция в CalculateColories.py

# Функция для получения email пользователя из temp.csv
def get_user_email_from_csv():
    with open('temp.csv', newline='') as file:
        reader = csv.reader(file)
        user_nickname = next(reader)[0]
    return user_nickname


def update_email_in_addfood( new_email):
    client = MongoClient("mongodb+srv://ingamatynina392:dracoshaa@cluster0.fgaoh2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["EatWise"]
    addfood_collection = db["addfood"]
    
    old_email=get_user_email_from_csv()
    
    # Оновлення електронної пошти в усіх документах, де стара пошта
    result = addfood_collection.update_many(
        {"user_nickname": old_email},
        {"$set": {"user_nickname": new_email}}
    )
    
    with open('temp.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_email])
    
# MongoDB connection
client = MongoClient("mongodb+srv://ingamatynina392:dracoshaa@cluster0.fgaoh2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["EatWise"]
addfood_collection = db["addfood"]

# Функция для загрузки информации о пользователе
def load_user_info():
    user_email = get_user_email_from_csv()
    if not user_email:
        return
    
    user = db["users"].find_one({"email": user_email})
    if not user:
        messagebox.showerror("Error", "User not found!")
        return
    
    # Заполняем поля редактирования данными из базы
    username_entry.delete(0, tk.END)
    username_entry.insert(0, user['username'])
    email_entry.delete(0, tk.END)
    email_entry.insert(0, user['email'])
    dob_entry.delete(0, tk.END)
    dob_entry.insert(0, user['date_of_birth'])
    height_entry.delete(0, tk.END)
    height_entry.insert(0, user['height'])
    weight_entry.delete(0, tk.END)
    weight_entry.insert(0, user['weight'])
    gender_entry.delete(0, tk.END)
    gender_entry.insert(0, user['gender'])
    diet_type_entry.delete(0, tk.END)
    diet_type_entry.insert(0, user['diet_type'])
    calories_entry.delete(0, tk.END)
    calories_entry.insert(0, user['calories'])

# Функция для сохранения изменённой информации
def save_user_info():
    user_email = get_user_email_from_csv()
    if not user_email:
        messagebox.showerror("Error", "Failed to retrieve user email!")
        return
    
    # Получаем изменённые данные из полей
    updated_data = {
        "username": username_entry.get(),
        "email": email_entry.get(),
        "date_of_birth": dob_entry.get() if dob_entry.get() else None,  # Добавляем значение по умолчанию
        "height": height_entry.get() if height_entry.get() else None,
        "weight": weight_entry.get() if weight_entry.get() else None,
        "gender": gender_entry.get() if gender_entry.get() else None,
        "diet_type": diet_type_entry.get() if diet_type_entry.get() else None,
        "calories": calories_entry.get() if calories_entry.get() else None,
    }
    
    # Получаем данные пользователя из базы
    user = db["users"].find_one({"email": user_email})
    
    # Если какие-то поля не были изменены, сохраняем их из старых данных
    if not updated_data.get('height'):
        updated_data['height'] = user['height']
    if not updated_data.get('weight'):
        updated_data['weight'] = user['weight']
    if not updated_data.get('gender'):
        updated_data['gender'] = user['gender']
    if not updated_data.get('date_of_birth'):  # Проверяем 'date_of_birth'
        updated_data['date_of_birth'] = user['date_of_birth']
    if not updated_data.get('diet_type'):
        updated_data['diet_type'] = user['diet_type']
    
    # Если изменённые параметры требующие пересчёта калорий
    if updated_data.get('height') != user['height'] or updated_data.get('weight') != user['weight'] or updated_data.get('gender') != user['gender'] or updated_data.get('date_of_birth') != user['date_of_birth']:
        # Расчитываем калории
        updated_data['calories'] = calculate_calories(
            updated_data.get('gender'),
            int(updated_data.get('height') or user['height']),
            int(updated_data.get('weight') or user['weight']),
            updated_data.get('date_of_birth') or user['date_of_birth'],
            updated_data.get('diet_type') or user['diet_type']
        )
    
    # Обновляем данные в базе
    db["users"].update_one({"email": user_email}, {"$set": updated_data})
    
    new_email = email_entry.get()
    update_email_in_addfood( new_email)
    # Информируем пользователя о успешном сохранении
    messagebox.showinfo("Success", "User information updated successfully!")

# Основное окно приложения
app = tk.Tk()
app.title("Account edit")
app.geometry("500x400")
app.configure(bg='#E0E6C4')
app.resizable(False, False)

# Растягиваем колонки и строки
app.grid_columnconfigure(1, weight=1, uniform="equal")
for row in range(8):
    app.grid_rowconfigure(row, weight=1)

# Создание полей для редактирования данных
tk.Label(app, text="Username:",font=("Arial", 14), bg='#E0E6C4').grid(row=0, column=0, padx=10, pady=5, sticky='w')
username_entry = tk.Entry(app, font=("Arial", 14))
username_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

tk.Label(app, text="Email:",font=("Arial", 14), bg='#E0E6C4').grid(row=1, column=0, padx=10, pady=5, sticky='w')
email_entry = tk.Entry(app, font=("Arial", 14))
email_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

tk.Label(app, text="Date of Birth:",font=("Arial", 14), bg='#E0E6C4').grid(row=2, column=0, padx=10, pady=5, sticky='w')
dob_entry = tk.Entry(app, font=("Arial", 14))
dob_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

tk.Label(app, text="Height (cm):",font=("Arial", 14), bg='#E0E6C4').grid(row=3, column=0, padx=10, pady=5, sticky='w')
height_entry = tk.Entry(app, font=("Arial", 14))
height_entry.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

tk.Label(app, text="Weight (kg):",font=("Arial", 14), bg='#E0E6C4').grid(row=4, column=0, padx=10, pady=5, sticky='w')
weight_entry = tk.Entry(app, font=("Arial", 14))
weight_entry.grid(row=4, column=1, padx=10, pady=5, sticky='ew')

tk.Label(app, text="Gender:",font=("Arial", 14), bg='#E0E6C4').grid(row=5, column=0, padx=10, pady=5, sticky='w')
gender_entry = tk.Entry(app, font=("Arial", 14))
gender_entry.grid(row=5, column=1, padx=10, pady=5, sticky='ew')

tk.Label(app, text="Diet Type:",font=("Arial", 14), bg='#E0E6C4').grid(row=6, column=0, padx=10, pady=5, sticky='w')
diet_type_entry = tk.Entry(app, font=("Arial", 14))
diet_type_entry.grid(row=6, column=1, padx=10, pady=5, sticky='ew')

tk.Label(app, text="Daily Caloric Need:",font=("Arial", 14), bg='#E0E6C4').grid(row=7, column=0, padx=10, pady=5, sticky='w')
calories_entry = tk.Entry(app, font=("Arial", 14))
calories_entry.grid(row=7, column=1, padx=10, pady=5, sticky='ew')

# Кнопка для сохранения изменений
save_button = tk.Button(app, text="Save", command=save_user_info, bg='#0A5381', fg='white', font=("Arial", 14))
save_button.grid(row=8, column=0, columnspan=2, pady=10)

load_user_info()

# Запускаем приложение
app.mainloop()
