import tkinter as tk
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the AI model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# Sample detailed responses for specific questions
DETAILED_RESPONSES = {
    "healthy snack options": (
        "Some healthy snack options include:\n"
        "- Greek yogurt with berries: A great source of protein and antioxidants.\n"
        "- Hummus with carrot sticks: Provides fiber and healthy fats.\n"
        "- A handful of mixed nuts: Rich in healthy fats, protein, and fiber.\n"
        "- Apple slices with almond butter: Offers fiber, vitamins, and healthy fats.\n"
        "- Cottage cheese with pineapple: A protein-packed snack with a sweet twist."
    ),
    "recipe for a quick breakfast": (
        "A quick breakfast recipe is a smoothie:\n"
        "- Blend 1 banana, a handful of spinach, 1 cup of almond milk, and a scoop of protein powder.\n"
        "You can also add a tablespoon of peanut butter or some oats for extra nutrients. "
        "It's quick, nutritious, and delicious!"
    ),
    "benefits of eating fruits and vegetables": (
        "Eating fruits and vegetables has numerous benefits:\n"
        "- They are high in essential vitamins and minerals, such as vitamin C and potassium.\n"
        "- They are rich in dietary fiber, which aids digestion and helps maintain a healthy weight.\n"
        "- Regular consumption can lower the risk of chronic diseases, including heart disease and diabetes.\n"
        "- They can improve skin health and provide hydration."
    ),
    "incorporate more protein": (
        "To incorporate more protein into your diet, consider these options:\n"
        "- Include lean meats like chicken, turkey, and fish in your meals.\n"
        "- Incorporate plant-based sources like beans, lentils, and chickpeas.\n"
        "- Use dairy products like Greek yogurt, cottage cheese, and milk.\n"
        "- Consider protein shakes or bars for a quick boost, especially after workouts."
    ),
    "low-carb meal ideas": (
        "Some low-carb meal ideas include:\n"
        "- Grilled chicken with steamed broccoli and a side salad.\n"
        "- Zucchini noodles with marinara sauce and meatballs.\n"
        "- A salad topped with salmon, avocado, and mixed greens.\n"
        "- Cauliflower rice stir-fry with vegetables and shrimp.\n"
        "- Omelette with spinach, mushrooms, and cheese."
    ),
    "effective exercises for weight loss": (
        "Effective exercises for weight loss include:\n"
        "- High-Intensity Interval Training (HIIT): Short bursts of intense exercise followed by rest.\n"
        "- Strength training: Building muscle can increase your resting metabolic rate.\n"
        "- Cardiovascular exercises like running, cycling, or swimming: Great for burning calories.\n"
        "- Circuit training: Combining different exercises for a full-body workout in a short time."
    ),
    "benefits of strength training": (
        "Strength training has several benefits:\n"
        "- Increases muscle mass, which boosts metabolism.\n"
        "- Improves bone density and reduces the risk of osteoporosis.\n"
        "- Enhances joint stability and reduces the risk of injury.\n"
        "- Improves overall body composition and body fat percentage."
    ),
    "stay motivated to work out": (
        "To stay motivated to work out:\n"
        "- Set realistic and achievable fitness goals to keep track of your progress.\n"
        "- Find a workout buddy to make exercising more enjoyable and hold each other accountable.\n"
        "- Change up your routine regularly to keep things interesting.\n"
        "- Reward yourself for reaching milestones to maintain motivation."
    ),
    "good stretches after a workout": (
        "Some good stretches to do after a workout include:\n"
        "- Hamstring stretch: Sit and reach for your toes to stretch the back of your legs.\n"
        "- Quadriceps stretch: Stand on one leg and pull your opposite foot to your glutes.\n"
        "- Shoulder stretch: Bring one arm across your body and hold it with the opposite hand.\n"
        "- Child’s pose: A great stretch for your back, hips, and shoulders."
    ),
    "improve cardiovascular fitness": (
        "To improve cardiovascular fitness, try:\n"
        "- Incorporating more aerobic activities like running, swimming, or cycling into your routine.\n"
        "- Gradually increasing the intensity and duration of your workouts.\n"
        "- Including interval training to boost heart health and stamina.\n"
        "- Staying active throughout the day by walking or taking the stairs."
    ),
    "difference between HIIT and steady-state cardio": (
        "HIIT (High-Intensity Interval Training) involves short bursts of intense exercise followed by rest or low-intensity periods, promoting efficient calorie burning and improving cardiovascular fitness. Steady-state cardio involves maintaining a consistent, moderate level of exertion for an extended period, helping to build endurance and burn fat."
    ),
    # Add more detailed responses as needed
}

# Function to generate the AI's response
def generate_response(input_text, chat_history_ids=None):
    # Check for specific questions for detailed responses
    for question, response in DETAILED_RESPONSES.items():
        if question in input_text.lower():
            return response, chat_history_ids

    # If no specific question matches, generate a response from the model
    new_input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors="pt")
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response, chat_history_ids

# Tkinter setup
root = tk.Tk()
root.title("AI Chat - Food & Fitness")
root.geometry("500x500")

# Chat history variable to maintain conversation
chat_history_ids = None

# Display message in chat window
def display_message(text, sender):
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"{sender}: {text}\n\n")
    chat_log.config(state=tk.DISABLED)
    chat_log.yview(tk.END)

# Send message when the user presses "Send"
def send_message():
    global chat_history_ids
    user_input = user_entry.get().strip()
    user_entry.delete(0, tk.END)

    if user_input:
        display_message(user_input, "You")

        # Generate a response with more detailed answers
        response, chat_history_ids = generate_response(user_input, chat_history_ids)
        
        display_message(response, "Bot")

# Set up the chat window
chat_log = tk.Text(root, bg="white", state=tk.DISABLED, wrap=tk.WORD)
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# User input entry
user_entry = tk.Entry(root, width=70)
user_entry.pack(padx=10, pady=(0, 10), side=tk.LEFT)
user_entry.bind("<Return>", lambda event: send_message())

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=(0, 10), padx=10, side=tk.RIGHT)

# Run the application
root.mainloop()
