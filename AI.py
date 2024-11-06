import tkinter as tk
from g4f import ChatCompletion


def send_and_receive_message():
    user_message = user_input.get()

    # Виводим вопрос в Label
    question_label.config(text=f"User: {user_message}")

    # Проверка на тематику сообщения
    if any(keyword in user_message.lower() for keyword in ["Food", "Sport", "food", "sport"]):
        # Вызов g4f.ChatCompletion.create для получения ответа
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            stream=True,
        )

        # Получаем ответ в виде текста
        response_text = ' '.join([str(message) for message in response])
        response_text = response_text[:200]  # Обрезаем до 200 символов для краткости

        # Отображаем ответ в Label
        response_label.config(text=f"AI: {response_text}")
    else:
        # Если вопрос не о Marvel, еде или спорте, выводим сообщение об ограничении
        response_label.config(text="AI: Sorry, I can only answer questions related to Marvel, food, or sports.")

# Создание главного окна
app = tk.Tk()
app.title("Chat Application")
app.geometry('344x582')
app.config(bg='#E0E6C4')

# Создание элементов в окне
user_input = tk.Entry(app, width=34)
send_button = tk.Button(app, text="Отправить", command=send_and_receive_message)
question_label = tk.Label(app, text="", wraplength=300, justify="left", fg='white', bg='#E0E6C4')
response_label = tk.Label(app, text="", wraplength=300, justify="left", fg='white', bg='#E0E6C4')

# Размещение элементов в окне
user_input.place(x=15, y=550)
send_button.place(x=257, y=546)
question_label.place(x=10, y=10)
response_label.place(x=10, y=30)

# Запуск главного цикла событий
app.mainloop()
