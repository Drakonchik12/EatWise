import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import calendar
from datetime import datetime
import random

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Calendar")
        self.root.geometry("1400x700")
        self.root.resizable(False, False)

        # Загрузка фонового изображения
        self.bg_image = Image.open("background.png")  
        self.bg_image = self.bg_image.resize((1400, 700), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Создание холста для фона
        self.canvas = tk.Canvas(self.root, width=1400, height=700)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Инициализация текущей даты
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.today = datetime.now()

        # Основные элементы интерфейса
        self.create_widgets()
        self.update_calendar()

    def create_widgets(self):
        # Левый верхний блок для календаря
        self.calendar_frame = tk.Frame(self.root, bg="white", relief="solid", bd=2)
        self.calendar_frame.place(x=70, y=50, width=600, height=350)

        # Заголовок для года и месяца
        self.header = tk.Label(self.calendar_frame, text="", font=("Arial", 16), background="white")
        self.header.pack(pady=10)

        # Кнопки для переключения месяцев
        self.prev_month_btn = tk.Button(self.calendar_frame, text="<", command=self.prev_month, width=5, height=2)
        self.prev_month_btn.pack(side="left", padx=10)

        self.next_month_btn = tk.Button(self.calendar_frame, text=">", command=self.next_month, width=5, height=2)
        self.next_month_btn.pack(side="right", padx=10)

        # Место для календаря
        self.days_frame = tk.Frame(self.calendar_frame, bg="white")
        self.days_frame.pack(pady=10)

        # Заголовки дней недели
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(self.days_frame, text=day, font=("Arial", 12), bg="white").grid(row=0, column=i)

        # Правый верхний блок для текущей даты
        self.date_frame = tk.Frame(self.root, bg="white", relief="solid", bd=2)
        self.date_frame.place(x=720, y=50, width=600, height=600)

        tk.Label(self.date_frame, text="Today:", font=("Arial", 14), bg="white").pack(pady=5)
        self.today_label = tk.Label(self.date_frame, text="", font=("Arial", 14), bg="white")
        self.today_label.pack(pady=5)

        # Нижний левый блок для совета дня
        self.advice_frame = tk.Frame(self.root, bg="white", relief="solid", bd=2)
        self.advice_frame.place(x=370, y=420, width=300, height=230)

        self.advice_label = tk.Label(self.advice_frame, text="Advice of the Day:", font=("Arial", 14), bg="white")
        self.advice_label.pack(pady=5)

        # Пример случайного совета дня
        self.advice_text = tk.Label(self.advice_frame, text="", wraplength=550, bg="white")
        self.advice_text.pack(pady=10)
        self.generate_advice()

        # Нижний правый блок для кнопок
        self.action_frame = tk.Frame(self.root, bg="white",relief="solid", bd=2)
        self.action_frame.place(x=70, y=420, width=300,  height=230)

        btn_add_meal = tk.Button(self.action_frame, text="+ Add Meal", height='3',  bg="lightgreen")
        btn_add_meal.grid(row=0, column=0, sticky="ew", padx=1, pady=1)

        btn_my_stats = tk.Button(self.action_frame, text="? My Stats", height='3', bg="lightyellow")
        btn_my_stats.grid(row=1, column=0, sticky="ew", padx=1, pady=1)

        btn_find_food = tk.Button(self.action_frame, text="? Find Food",height='3', bg="lightblue")
        btn_find_food.grid(row=2, column=0, sticky="ew", padx=1, pady=1)

        btn_chat_advice = tk.Button(self.action_frame, text="? Chat Advice", height='3', bg="lightpink")
        btn_chat_advice.grid(row=3, column=0, sticky="ew", padx=1, pady=1)

        # Равномерное распределение высоты кнопок
        self.action_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)   

    def update_calendar(self):
        # Очистка предыдущего календаря
        for widget in self.days_frame.winfo_children():
            widget.destroy()

        # Обновление заголовка месяца и года
        month_name = calendar.month_name[self.month]
        self.header.config(text=f"{month_name} {self.year}")

        # Получение календаря для указанного месяца и года
        month_calendar = calendar.monthcalendar(self.year, self.month)
        
        # Отображение календаря
        for r, week in enumerate(month_calendar):
            for c, day in enumerate(week):
                if day != 0:
                    day_button = tk.Button(self.days_frame, text=str(day), width=5, height=2, relief="groove",
                                           command=lambda d=day: self.show_day_popup(d))
                    
                    # Выделяем текущий день
                    if day == self.today.day and self.year == self.today.year and self.month == self.today.month:
                        day_button.config(bg="lightblue", fg="black")
                    day_button.grid(row=r + 1, column=c, padx=5, pady=5)  # +1 для учета заголовка дней

        # Обновление текущей даты
        self.today_label.config(text=self.today.strftime("%d %B %Y"))

    def generate_advice(self):
        # Пример случайных советов
        advice_list = [
            "Stay hydrated!",
            "Eat balanced meals!",
            "Exercise regularly!",
            "Get enough sleep!",
            "Take breaks during work!"
        ]
        self.advice_text.config(text=random.choice(advice_list))

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.update_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.update_calendar()

    def show_day_popup(self, day):
        date_str = f"{day}/{self.month}/{self.year}"
        messagebox.showinfo("Selected Date", f"Hello! You selected the date: {date_str}")

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
