from pymongo import MongoClient
from bson.objectid import ObjectId


# Строка подключения с заменой <db_password> на ваш реальный пароль
connection_string = "mongodb+srv://ingamatynina392:dracoshaa@cluster0.fgaoh2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Замените <db_password> на ваш пароль

# Подключение к MongoDB
client = MongoClient(connection_string)

# Создание базы данных EatWise
db = client.EatWise

# Создание коллекции users
users_collection = db.users

# Пример документа (пользователя) для вставки
user = {
    "login": "john_doe",
    "email": "john.doe@example.com",  # Email будет использоваться как уникальный ключ
    "password": "securepassword",
    "birthdate": "1990-01-01",  # Дата рождения
    "weight": 70,  # Вес в килограммах
    "height": 175,  # Рост в сантиметрах
    "gender": "male",  # Гендер
    "diet_type": "vegetarian",  # Тип питания
    "calories": 2000  # Ежедневное потребление калорий
}

# Вставка документа в коллекцию
user_id = users_collection.insert_one(user).inserted_id

print(f"Пользователь создан с ID: {user_id}")

# Вывод всех пользователей
for user in users_collection.find():
    print(user)
