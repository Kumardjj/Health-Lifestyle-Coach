import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Health & Lifestyle Coach", layout="centered")

def calculate_health_profile(user):
    recommendations = []
    score = 0
    
    # BMI Logic
    if user['BMI'] < 18.5:
        recommendations.append("Increase calorie intake with balanced protein meals (underweight).")
        score += 6
    elif user['BMI'] <= 24.9:
        recommendations.append("Your BMI is in a healthy range - maintain your current diet and activity.")
        score += 9
    elif user['BMI'] > 30.0:
        recommendations.append("High BMI - focus on portion control and consistent cardio.")
        score += 5
    else:
        recommendations.append("Slightly overweight - focus on moderate cardio.")
        score += 7
        
    # Water Intake
    if user['water'] < 1.5:
        recommendations.append("Increase water intake to at least 2.5 liters per day.")
        score += 5
    elif user['water'] < 2.5:
        recommendations.append("Drink slightly more water, aim for 2.5 liters per day.")
        score += 7
    else:
        recommendations.append("Excellent hydration habits! Keep it up.")
        score += 10

    # Workout Frequency
    if user['workout_freq'] < 2:
        recommendations.append("Low activity. Aim for at least 3 days of movement.")
        score += 4
    elif user['workout_freq'] <= 4:
        recommendations.append("Good consistency! Consider an active recovery day.")
        score += 8
    else:
        recommendations.append("Highly active! Ensure proper sleep and recovery.")
        score += 10

    # Meals
    if user['meals'] < 3:
        recommendations.append("Eating too infrequently can cause energy crashes.")
        score += 6
    else:
        recommendations.append("Optimal meal frequency for metabolism.")
        score += 10

    final_score = round(score / 4, 1) # Normalizing to 10
    return recommendations, final_score

# --- UI LAYOUT ---
st.title("🏃‍♂️ Health & Lifestyle Coach")
st.write("Adjust your metrics below to see your personalized health score and diet tips.")

with st.sidebar:
    st.header("Your Metrics")
    age = st.slider("Age", 18, 100, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    weight = st.number_input("Weight (kg)", 40, 200, 70)
    height = st.number_input("Height (cm)", 120, 220, 170)
    
    # Calculate BMI
    bmi = round(weight / ((height/100)**2), 1)
    
    workout_freq = st.slider("Workout Days/Week", 0, 7, 3)
    exercise_type = st.selectbox("Exercise Type", ["Gym", "Cardio", "Yoga", "Walking", "None"])
    water = st.slider("Water Intake (Liters)", 0.5, 5.0, 2.0, 0.1)
    meals = st.slider("Daily Meal Frequency", 1, 6, 3)

user_data = {
    'BMI': bmi, 'workout_freq': workout_freq, 
    'physical_exercise': exercise_type, 'water': water, 'meals': meals
}

# --- PROCESS & DISPLAY ---
recs, l_score = calculate_health_profile(user_data)

col1, col2 = st.columns([1, 1])

with col1:
    st.metric("Lifestyle Score", f"{l_score}/10")
    st.subheader("Recommendations:")
    for r in recs:
        st.write(f"- {r}")

with col2:
    # Visualization
    categories = ['BMI', 'Water', 'Workout', 'Meals']
    # Mapping inputs to 0-10 scale for bar chart
    values = [
        np.clip((25 - abs(bmi - 22)) / 25 * 10, 0, 10),
        np.clip(water / 2.5 * 10, 0, 10),
        np.clip(workout_freq / 5 * 10, 0, 10),
        np.clip(meals / 4 * 10, 0, 10)
    ]
    
    fig, ax = plt.subplots()
    ax.bar(categories, values, color=['#66b3ff','#99ff99','#ffcc99','#ff9999'])
    ax.set_ylim(0, 10)
    ax.set_title("Health Profile Breakdown")
    st.pyplot(fig)