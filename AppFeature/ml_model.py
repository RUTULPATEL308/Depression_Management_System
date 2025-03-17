# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# import joblib

# # Load dataset
# df = pd.read_csv("mental_health_dataset.csv")

# # Convert categorical data to numerical (Example)
# df["sleep_quality"] = df["sleep_quality"].map({"Poor": 0, "Average": 1, "Good": 2})
# df["interest_in_activities"] = df["interest_in_activities"].map({"Lost": 0, "Decreased": 1, "Normal": 2})
# df["suicidal_thoughts"] = df["suicidal_thoughts"].map({"Yes": 1, "No": 0})

# # Define features and target
# X = df.drop(columns=["recommendation"])  # Features (User input data)
# y = df["recommendation"]  # Target (AI-generated recommendations)

# # Split dataset
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train model
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Save the model
# joblib.dump(model, "ai_mood_recommendation.pkl")
# print("Model trained and saved successfully!")


# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# import joblib

# # Sample Data with Recommendations
# data = {
#     "mood_level": [2, 3, 7, 1, 4],
#     "sleep_hours": [4, 5, 8, 3, 6],
#     "sleep_quality": ["Poor", "Average", "Good", "Poor", "Average"],
#     "interest_in_activities": ["Lost", "Decreased", "Normal", "Lost", "Decreased"],
#     "suicidal_thoughts": ["Yes", "No", "No", "Yes", "No"],
#     "recommendation": [
#         "Please seek immediate help. Contact a crisis helpline.",
#         "Consider talking to a therapist or a close friend about your feelings.",
#         "You're doing great! Keep up with your self-care routine.",
#         "Please reach out to a mental health professional as soon as possible.",
#         "Try engaging in small enjoyable activities to improve your mood."
#     ]
# }

# # Convert to DataFrame
# df = pd.DataFrame(data)

# # Encode categorical variables
# df["sleep_quality"] = df["sleep_quality"].map({"Poor": 0, "Average": 1, "Good": 2})
# df["interest_in_activities"] = df["interest_in_activities"].map({"Lost": 0, "Decreased": 1, "Normal": 2})
# df["suicidal_thoughts"] = df["suicidal_thoughts"].map({"Yes": 1, "No": 0})

# # Features & Target
# X = df.drop(columns=["recommendation"])
# y = df["recommendation"]  # Keep the target as text-based recommendations

# # Train Model
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Save the trained model
# joblib.dump(model, "ai_mood_recommendation.pkl")

# print("AI model trained successfully and saved as ai_mood_recommendation.pkl")

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import random

# Generate synthetic data
num_samples = 500  # Increase dataset size

data = {
    "mood_level": np.random.randint(1, 11, num_samples),  # Mood scale 1-10
    "sleep_hours": np.random.randint(2, 11, num_samples),  # Sleep hours 2-10
    "sleep_quality": np.random.choice(["Poor", "Average", "Good"], num_samples),
    "interest_in_activities": np.random.choice(["Lost", "Decreased", "Normal"], num_samples),
    "suicidal_thoughts": np.random.choice(["Yes", "No"], num_samples)
}

# Define possible recommendations
recommendations = [
    "Please seek immediate help. Contact a crisis helpline.",
    "Consider talking to a therapist or a close friend about your feelings.",
    "You're doing great! Keep up with your self-care routine.",
    "Please reach out to a mental health professional as soon as possible.",
    "Try engaging in small enjoyable activities to improve your mood.",
    "Maintain a healthy sleep schedule and balanced diet.",
    "Practice mindfulness and meditation to manage stress.",
    "Engage in regular physical exercise for mental well-being.",
    "Socialize with friends and family to boost your mood.",
    "Take breaks and engage in hobbies to reduce stress."
]

# Assign recommendations based on risk factors
recommendation_list = []
for i in range(num_samples):
    if data["suicidal_thoughts"][i] == "Yes" or data["mood_level"][i] <= 2:
        recommendation_list.append(recommendations[0])  # Crisis helpline
    elif data["mood_level"][i] <= 4:
        recommendation_list.append(random.choice(recommendations[1:5]))  # Therapy, small activities
    elif data["mood_level"][i] >= 8:
        recommendation_list.append(random.choice(recommendations[2:]))  # Positive reinforcement
    else:
        recommendation_list.append(random.choice(recommendations[3:]))  # General well-being tips

data["recommendation"] = recommendation_list

# Convert to DataFrame
df = pd.DataFrame(data)

# Encode categorical variables
df["sleep_quality"] = df["sleep_quality"].map({"Poor": 0, "Average": 1, "Good": 2})
df["interest_in_activities"] = df["interest_in_activities"].map({"Lost": 0, "Decreased": 1, "Normal": 2})
df["suicidal_thoughts"] = df["suicidal_thoughts"].map({"Yes": 1, "No": 0})

# Features & Target
X = df.drop(columns=["recommendation"])
y = df["recommendation"]

# Train Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=200, random_state=42)  # Increased estimators for better performance
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "ai_mood_recommendation.pkl")

# Display dataset summary
df.head()
