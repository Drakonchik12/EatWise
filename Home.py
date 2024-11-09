import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import calendar
from datetime import datetime
import random
import subprocess
import csv
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb+srv://ingamatynina392:dracoshaa@cluster0.fgaoh2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["EatWise"]
addfood_collection = db["addfood"]

def AI_page():
    subprocess.run(["python", "AI.py"])
    
def Account_page():
    subprocess.run(["python", "Account.py"])
    
def Account_edit_page():
    subprocess.run(["python", "EditAccount.py"])
    
def Statistic_page():
    subprocess.run(["python", "Statistic.py"])
    
def Edit_password_page():
    subprocess.run(["python", "EditPassword.py"])

def Food_page():
    subprocess.run(["python", "search_food.py"])

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Calendar")
        self.root.geometry("1400x700")
        self.root.resizable(False, False)

        # Load user nickname from temp.csv
        self.user_nickname = self.load_nickname()
        
        # Background image
        self.bg_image = Image.open("background.png")  
        self.bg_image = self.bg_image.resize((1400, 700), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Canvas for background
        self.canvas = tk.Canvas(self.root, width=1400, height=700)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Current date initialization
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.today = datetime.now()
        
        # Main interface components
        self.create_widgets()
        self.update_calendar()
        
    def load_nickname(self):
        with open('temp.csv', newline='') as file:
            reader = csv.reader(file)
            user_nickname = next(reader)[0]
        return user_nickname

    def create_widgets(self):
        # Calendar frame
        self.calendar_frame = tk.Frame(self.root, bg="white", relief="solid", bd=2)
        self.calendar_frame.place(x=70, y=50, width=600, height=380)

        # Month and year header
        self.header = tk.Label(self.calendar_frame, text="", font=("Arial", 16), background="white")
        self.header.pack(pady=10)

        # Month navigation buttons
        self.prev_month_btn = tk.Button(self.calendar_frame, text="<", command=self.prev_month, width=5, height=2)
        self.prev_month_btn.pack(side="left", padx=10)
        self.next_month_btn = tk.Button(self.calendar_frame, text=">", command=self.next_month, width=5, height=2)
        self.next_month_btn.pack(side="right", padx=10)

        # Days of the week header
        self.days_frame = tk.Frame(self.calendar_frame, bg="white")
        self.days_frame.pack(pady=10)

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(self.days_frame, text=day, font=("Arial", 12), bg="white").grid(row=0, column=i)

        # Right block for today's date and food info
        self.date_frame = tk.Frame(self.root, bg="white", relief="solid", bd=2)
        self.date_frame.place(x=720, y=50, width=600, height=600)

        tk.Label(self.date_frame, text="Day:", font=("Arial", 14), bg="white").pack(pady=5)
        self.today_label = tk.Label(self.date_frame, text="", font=("Arial", 14), bg="white")
        self.today_label.pack(pady=5)
        
        # Food info area with scrollbar
        self.food_info_label = tk.Label(self.date_frame, text="Food for the Day:", font=("Arial", 14), bg="white")
        self.food_info_label.pack(pady=5)

        # Canvas for food entries with scrollbar
        self.food_canvas = tk.Canvas(self.date_frame, bg="white")
        self.food_canvas.pack(pady=5, fill="both", expand=True)

        # Scrollbar
        self.food_scrollbar = tk.Scrollbar(self.date_frame, orient="vertical", command=self.food_canvas.yview)
        self.food_scrollbar.pack(side="right", fill="y")

        # Frame inside canvas to hold the food entries
        self.food_info_container = tk.Frame(self.food_canvas, bg="white")
        self.food_info_container.bind(
            "<Configure>", lambda e: self.food_canvas.configure(scrollregion=self.food_canvas.bbox("all"))
        )
        self.food_canvas.create_window((0, 0), window=self.food_info_container, anchor="nw")
        
        today_date_str = self.today.strftime("%d/%m/%Y")
        self.show_food_for_day(today_date_str) 
        self.food_canvas.configure(yscrollcommand=self.food_scrollbar.set)

        # Lower left block for daily advice
        self.advice_frame = tk.Frame(self.root, bg="white", relief="solid", bd=2)
        self.advice_frame.place(x=370, y=450, width=300, height=200)

        self.advice_label = tk.Label(self.advice_frame, text="Advice of the Day:", font=("Arial", 14), bg="white")
        self.advice_label.pack(pady=5)
        
        self.advice_text = tk.Label(self.advice_frame, text="", wraplength=280, bg="white", justify="left")
        self.advice_text.pack(pady=10, padx=20, fill="both", expand=True)
        self.generate_advice()

        # Lower right block for action buttons
        self.action_frame = tk.Frame(self.root, bg="white", relief="solid", bd=2)
        self.action_frame.place(x=70, y=450, width=300, height=200)
        
        btn_my_account = tk.Button(self.action_frame, text="? My Account",command=Account_page, height='2', bg="lightyellow")
        btn_my_account.grid(row=1, column=0, sticky="ew", padx=1, pady=1)
        
        btn_my_account_edit = tk.Button(self.action_frame, text="* Password edit", command=Edit_password_page, height='2', bg="lightblue")
        btn_my_account_edit.grid(row=2, column=0, sticky="ew", padx=1, pady=1)
        
        btn_my_password_edit = tk.Button(self.action_frame, text="* Account edit",command=Account_edit_page, height='2', bg="lightpink")
        btn_my_password_edit.grid(row=3, column=0, sticky="ew", padx=1, pady=1)

        btn_my_stats = tk.Button(self.action_frame, text="? My Stats",command=Statistic_page, height='2', bg="lightyellow")
        btn_my_stats.grid(row=4, column=0, sticky="ew", padx=1, pady=1)

        btn_find_food = tk.Button(self.action_frame, text="+ Find Food", command=Food_page, height='2', bg="lightblue")
        btn_find_food.grid(row=5, column=0, sticky="ew", padx=1, pady=1)

        btn_chat_advice = tk.Button(self.action_frame, text="? Chat Advice", command=AI_page, height='2', bg="lightpink")
        btn_chat_advice.grid(row=6, column=0, sticky="ew", padx=1, pady=1)

        self.action_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)

    def update_calendar(self):
        for widget in self.days_frame.winfo_children():
            widget.destroy()

        month_name = calendar.month_name[self.month]
        self.header.config(text=f"{month_name} {self.year}")

        month_calendar = calendar.monthcalendar(self.year, self.month)
        
        for r, week in enumerate(month_calendar):
            for c, day in enumerate(week):
                if day != 0:
                    day_button = tk.Button(self.days_frame, text=str(day), width=5, height=2, relief="groove",
                                           command=lambda d=day: self.show_food_for_day(f"{d}/{self.month}/{self.year}"))
                    
                    if (day == self.today.day and 
                        self.year == self.today.year and 
                        self.month == self.today.month):
                        day_button.config(bg="green", fg="white")
                    day_button.grid(row=r + 1, column=c, padx=5, pady=5)

        self.today_label.config(text=self.today.strftime("%d %B %Y"))
        

    def show_food_for_day(self, date_str):
        
        
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        date_formatted = f"{date_obj.day}/{date_obj.month}/{date_obj.year}"
        self.today_label.config(text=date_formatted)
        
        with open("temp2.csv", mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile) # Опционально: добавляем заголовок "date"
            writer.writerow([date_formatted] ) 
        
        for widget in self.food_info_container.winfo_children():
            widget.destroy()

        food_entries = self.get_food_for_day(date_str)

        if food_entries:
            for entry in food_entries:
                food_frame = tk.Frame(self.food_info_container, bg="lightgray", bd=2,  width=600, relief="groove")
                food_frame.pack(fill="x", pady=5, padx=10)

                product_name_label = tk.Label(food_frame, text=entry["product_name"],  width=55, font=("Arial", 12, "bold"), bg="lightgray")
                product_name_label.pack(anchor="w", padx=10, pady=5)

                calorie_label = tk.Label(food_frame, text=f"Calories: {entry['calories']} kcal",  width=55, bg="lightgray", font=("Arial", 10))
                calorie_label.pack(anchor="w", padx=10)

                protein_label = tk.Label(food_frame, text=f"Protein: {entry.get('protein', 'N/A')}g",   width=55, bg="lightgray", font=("Arial", 10))
                protein_label.pack(anchor="w", padx=10)

                fat_label = tk.Label(food_frame, text=f"Fat: {entry.get('fat', 'N/A')}g", width=55, bg="lightgray", font=("Arial", 10))
                fat_label.pack(anchor="w", padx=10)

                carbs_label = tk.Label(food_frame, text=f"Carbohydrates: {entry.get('carbs', 'N/A')}g", width=55, bg="lightgray", font=("Arial", 10))
                carbs_label.pack(anchor="w", padx=10) 
                
                delete_btn = tk.Button(food_frame, text="Delete", command=lambda e=entry: self.delete_food_entry(e["product_name"], date_str), bg="red", fg="white")
                delete_btn.pack(anchor="e", padx=10)
        else:
            tk.Label(self.food_info_container, text="No food entries found for this date.", font=("Arial", 12)).pack(pady=20)

    def get_food_for_day(self, date_str):
        return list(addfood_collection.find({"date": date_str}))

    def delete_food_entry(self, product_name, date):
        result = addfood_collection.delete_one({"product_name": product_name, "date": date})
        if result.deleted_count > 0:
            messagebox.showinfo("Success", f"Product '{product_name}' deleted.")
            self.show_food_for_day(date)  # Refresh the view
        else:
            messagebox.showerror("Error", "Failed to delete product.")

    def generate_advice(self):
        advice_list = [
            "Stay hydrated by drinking enough water.",
            "Include more fruits and vegetables in your diet.",
            "Take a walk every day to stay active.",
            "Make time for relaxation and mental health.",
            "Avoid processed foods for better health.",
            "Aim to get enough sleep every night."
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

# Main application
root = tk.Tk()
app = CalendarApp(root)
root.mainloop()
