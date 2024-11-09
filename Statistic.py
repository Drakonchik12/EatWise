import tkinter as tk
from pymongo import MongoClient
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import csv

# MongoDB setup
client = MongoClient("mongodb+srv://ingamatynina392:dracoshaa@cluster0.fgaoh2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["EatWise"]
users_collection = db["users"]
addfood_collection = db["addfood"]

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Statictic")
        self.root.geometry("1400x700")
        root.config(bg='#135670')
        self.root.resizable(False, False)
        
        # Получение user_nickname из temp.csv
        self.user_nickname = self.get_nickname_from_csv()
        
        # Получение данных о норме калорий и БЖУ
        self.get_user_data()
        
        # Основной фрейм для отображения статистики
        self.stats_frame = tk.Frame(self.root, bg="white", relief="solid", bd=2)
        self.stats_frame.place(x=100, y=50, width=1200, height=600)

        tk.Label(self.stats_frame, text="Your Daily and Monthly Statistics:", font=("Arial", 14), bg="white").pack(pady=5)
        
        
        # Фрейм для размещения графиков в одной линии
        self.graph_frame = tk.Frame(self.stats_frame, bg="white")
        self.graph_frame.pack(fill="both", expand=True, pady=10 )
        
        # Отображение статистики
        self.show_user_statistics()

    def get_nickname_from_csv(self):
            with open('temp.csv', newline='') as file:
                reader = csv.reader(file)
                user_nickname = next(reader)[0]
            return user_nickname # Возвращает первый столбец (никнейм)

    def get_user_data(self):
        # Получение данных пользователя по нику из базы данных
        user_profile = users_collection.find_one({"user_nickname": self.user_nickname})

        if user_profile:
            self.daily_calories = user_profile.get("calories", 2000)
            self.daily_proteins = user_profile.get("daily_proteins", 75)
            self.daily_fats = user_profile.get("daily_fats", 70)
            self.daily_carbs = user_profile.get("daily_carbs", 250)
        else:
            # Значения по умолчанию
            self.daily_calories = 2000
            self.daily_proteins = 75
            self.daily_fats = 70
            self.daily_carbs = 250

    def show_user_statistics(self):
        # Получение статистики за последние 30 дней
        daily_stats = self.get_daily_statistics()
        
        # Отображение дневной статистики
        self.create_daily_chart(daily_stats)
        self.create_daily_nutrient_chart(daily_stats)
        
        # Расчет и отображение разбивки по БЖУ
        monthly_stats = self.get_monthly_nutrient_breakdown()
        self.create_nutrient_chart(monthly_stats)

    def get_daily_statistics(self):
        # Диапазон дат для последних 30 дней
        last_30_days = datetime.now() - timedelta(days=30)
        
        # Получение данных пользователя по дням за последние 30 дней
        user_data = addfood_collection.aggregate([
            {"$match": {
                "user_nickname": self.user_nickname,
                "date": {"$gte": last_30_days.strftime("%d/%m/%Y")}
            }},
            {"$group": {
                "_id": "$date",
                "total_calories": {"$sum": "$calories"},
                "total_proteins": {"$sum": "$protein"},
                "total_fats": {"$sum": "$fat"},
                "total_carbs": {"$sum": "$carbs"}
            }},
            {"$sort": {"_id": 1}}
        ])
        return list(user_data)

    def get_monthly_nutrient_breakdown(self):
        # Диапазон дат для последних 30 дней
        last_30_days = datetime.now() - timedelta(days=30)
        
        # Суммирование по БЖУ за последние 30 дней
        nutrient_totals = addfood_collection.aggregate([
            {"$match": {
                "user_nickname": self.user_nickname,
                "date": {"$gte": last_30_days.strftime("%d/%m/%Y")}
            }},
            {"$group": {
                "_id": None,
                "total_proteins": {"$sum": "$protein"},
                "total_fats": {"$sum": "$fat"},
                "total_carbs": {"$sum": "$carbs"}
            }}
        ])
        return list(nutrient_totals)[0] if nutrient_totals else {"total_proteins": 0, "total_fats": 0, "total_carbs": 0}

    def create_daily_chart(self, daily_stats):
        dates = [entry["_id"] for entry in daily_stats]
        calories = [entry["total_calories"] for entry in daily_stats]
        
        fig, ax = plt.subplots(figsize=(6, 3))
        
        ax.plot(dates, calories, marker='o', color="#135670", label="Consumed Calories")
        ax.axhline(self.daily_calories, color='red', linestyle='--', label="Daily Calorie Norm")
        ax.set_title("Daily Calorie Consumption (Last 30 Days)")
        ax.set_ylabel("Calories")
        ax.legend()
        ax.tick_params(axis='x', rotation=45)

        ax.set_xticklabels([])
        # Вставка графика в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.stats_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)
        
    def create_daily_nutrient_chart(self, daily_stats):
        dates = [entry["_id"] for entry in daily_stats]
        proteins = [entry["total_proteins"] for entry in daily_stats]
        fats = [entry["total_fats"] for entry in daily_stats]
        carbs = [entry["total_carbs"] for entry in daily_stats]

        # Размер графика
        fig, ax = plt.subplots(figsize=(4, 2))

        # Построение линий для каждого макроэлемента
        ax.plot(dates, proteins, marker='o', color="#FF9999", label="Proteins")
        ax.plot(dates, fats, marker='o', color="#66B2FF", label="Fats")
        ax.plot(dates, carbs, marker='o', color="#99FF99", label="Carbs")

        # Настройка заголовка и подписей
        ax.set_title("Daily Nutrient Breakdown (Proteins, Fats, Carbs) - Last 30 Days", fontsize=10)
        ax.set_ylabel("Grams", fontsize=8)
        ax.legend(fontsize=8)
        ax.tick_params(axis='x', rotation=45, labelsize=8)

        ax.set_xticklabels([])  # Убираем подписи оси X, если нужно

        # Вставка графика в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=10)


    def create_nutrient_chart(self, monthly_stats):
        labels = ["Proteins", "Fats", "Carbs"]
        values = [monthly_stats["total_proteins"], monthly_stats["total_fats"], monthly_stats["total_carbs"]]
        colors = ["#FF9999", "#66B2FF", "#99FF99"]

        fig, ax = plt.subplots(figsize=(4, 2))
        ax.pie(values, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
        ax.set_title("Monthly Nutrient Breakdown (Proteins, Fats, Carbs) - Last 30 Days")

        # Вставка круговой диаграммы в Tkinter
          # Вставка круговой диаграммы в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=10)

# Основное приложение
root = tk.Tk()
app = CalendarApp(root)
root.mainloop()
