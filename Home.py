import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import calendar
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Calendar")
        self.root.geometry("1400x700")
        self.root.resizable(False, False)

        # Загрузка фона
        self.bg_image = Image.open("background.png")  # Загрузка фонового изображения
        self.bg_image = self.bg_image.resize((1400, 700), Image.ANTIALIAS)
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
        # Создаем заголовок для года и месяца
        self.header = tk.Label(self.root, text="", font=("Arial", 16), bg="#ffcc99")
        self.header.place(x=600, y=20)

        # Кнопки для переключения месяцев
        self.prev_month_btn = tk.Button(self.root, text="<", command=self.prev_month, width=5, height=2, bg="#ffcc99")
        self.prev_month_btn.place(x=500, y=20)

        self.next_month_btn = tk.Button(self.root, text=">", command=self.next_month, width=5, height=2, bg="#ffcc99")
        self.next_month_btn.place(x=750, y=20)

        # Место для календаря
        self.days_frame = tk.Frame(self.root, bg="white")
        self.days_frame.place(x=150, y=80, width=1100, height=400)

        # Заголовки дней недели
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(self.root, text=day, font=("Arial", 12), bg="white").place(x=160 + i * 150, y=60)

        # Нижние блоки
        self.create_bottom_blocks()

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
                    day_button.grid(row=r, column=c, padx=5, pady=5)

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

    def create_bottom_blocks(self):
        # Первый блок с кнопками
        action_frame = tk.Frame(self.root, bg="white")
        action_frame.place(x=100, y=500, width=1200, height=80)

        tk.Button(action_frame, text="+ Add Meal", width=15, height=2, bg="lightgreen").place(x=50, y=20)
        tk.Button(action_frame, text="? My Stats", width=15, height=2, bg="lightyellow").place(x=500, y=20)
        tk.Button(action_frame, text="? Find Food", width=15, height=2, bg="lightblue").place(x=950, y=20)

        # Второй блок с текущей датой
        date_frame = tk.Frame(self.root, bg="lightgray", relief="solid", bd=1)
        date_frame.place(x=100, y=600, width=1200, height=50)

        tk.Label(date_frame, text="Today:", font=("Arial", 12), bg="lightgray").place(x=10, y=10)
        tk.Label(date_frame, text=self.today.strftime("%d %B %Y"), font=("Arial", 12), bg="lightgray").place(x=100, y=10)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
