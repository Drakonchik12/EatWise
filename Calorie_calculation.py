from datetime import datetime


def calculate_calories(gender, height_cm, weight_kg, dob_str, diet_type):
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()

    height_cm = float(height_cm)
    weight_kg = float(weight_kg)
    age = calculate_age(dob)
    
    if diet_type not in ["maintenance", "loss", "gain"]:
        diet_type = "maintenance"
    # Basal Metabolic Rate (BMR) calculation based on the Mifflin-St Jeor Equation
    if gender.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif gender.lower() == "female":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        raise ValueError("Invalid gender. Please use 'male' or 'female'.")

    # Calculate calorie needs based on activity level or diet type
    # Default to "maintenance" if an invalid or empty diet_type is provided
    diet_type = diet_type.lower()

    if diet_type == "loss":
        daily_calories = bmr * 1.2  # Reduce calories for weight loss
    elif diet_type == "gain":
        daily_calories = bmr * 1.5  # Increase calories for weight gain
    else:
        daily_calories = bmr * 1.3  # Default to maintenance calories

    return round(daily_calories)

# Example usage
def calculate_age(birthdate):
   
    today = datetime.today()
    
    # Calculate age by subtracting years
    age = today.year - birthdate.year
    
    # Check if the birthday has occurred yet this year, if not subtract 1 year from age
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1

    return age
