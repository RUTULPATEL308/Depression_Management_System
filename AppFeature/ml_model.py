import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import random
import os

# Define book recommendations
BOOK_RECOMMENDATIONS = {
    "Depression": {"title": "The Noonday Demon: An Atlas of Depression", "link": "https://www.amazon.com/dp/1501123882"},
    "Anxiety": {"title": "The Anxiety and Phobia Workbook", "link": "https://www.amazon.com/dp/1626252157"},
    "Stress": {"title": "Burnout: The Secret to Unlocking the Stress Cycle", "link": "https://www.amazon.com/dp/198481706X"},
    "Mindfulness": {"title": "Wherever You Go, There You Are", "link": "https://www.amazon.com/dp/1401307787"},
    "General Well-being": {"title": "The Happiness Project", "link": "https://www.amazon.com/dp/006158326X"}
}

# Load the trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ai_mood_recommendation_v3.pkl")
model = joblib.load(MODEL_PATH)

# Define categorical encoding mappings
ENCODING_MAP = {
    "sleep_quality": {"Poor": 0, "Average": 1, "Good": 2},
    "interest_in_activities": {"Lost": 0, "Decreased": 1, "Normal": 2},
    "social_engagement": {"Isolated": 0, "Occasional": 1, "Frequent": 2},
    "energy_levels": {"Low": 0, "Normal": 1, "High": 2},
    "appetite_changes": {"Decrease": -1, "Normal": 0, "Increase": 1},
    "suicidal_thoughts": {"Yes": 1, "No": 0},
    "emotional_state": {
        "Happy": "emotional_state_Happy",
        "Sad": "emotional_state_Sad",
        "Anxious": "emotional_state_Anxious",
        "Stressed": "emotional_state_Stressed",
        "Calm": "emotional_state_Calm",
        "Depressed": "emotional_state_Depressed"
    }
}

def preprocess_user_data(user_data):
    """
    Convert user input dictionary into a model-compatible DataFrame.
    """
    try:
        user_data["sleep_quality"] = ENCODING_MAP["sleep_quality"].get(user_data.get("sleep_quality", "Average"), 1)
        user_data["interest_in_activities"] = ENCODING_MAP["interest_in_activities"].get(user_data.get("interest_in_activities", "Decreased"), 1)
        user_data["social_engagement"] = ENCODING_MAP["social_engagement"].get(user_data.get("social_engagement", "Occasional"), 1)
        user_data["energy_levels"] = ENCODING_MAP["energy_levels"].get(user_data.get("energy_levels", "Normal"), 1)
        user_data["appetite_changes"] = ENCODING_MAP["appetite_changes"].get(user_data.get("appetite_changes", "Normal"), 0)
        user_data["suicidal_thoughts"] = ENCODING_MAP["suicidal_thoughts"].get(user_data.get("suicidal_thoughts", "No"), 0)

        emotional_state = user_data.get("emotional_state", "Neutral")
        encoded_emotions = {key: 0 for key in ENCODING_MAP["emotional_state"].values()}
        if emotional_state in ENCODING_MAP["emotional_state"]:
            encoded_key = ENCODING_MAP["emotional_state"][emotional_state]
            encoded_emotions[encoded_key] = 1

        processed_data = {**user_data, **encoded_emotions}
        processed_data.pop("emotional_state", None)

        return pd.DataFrame([processed_data])

    except Exception as e:
        return f"Error processing user data: {str(e)}"

def get_book_recommendation(emotional_state):
    """
    Suggests a book based on emotional state.
    """
    if emotional_state in ["Sad", "Depressed"]:
        return BOOK_RECOMMENDATIONS["Depression"]
    elif emotional_state == "Anxious":
        return BOOK_RECOMMENDATIONS["Anxiety"]
    elif emotional_state == "Stressed":
        return BOOK_RECOMMENDATIONS["Stress"]
    elif emotional_state == "Calm":
        return BOOK_RECOMMENDATIONS["Mindfulness"]
    else:
        return BOOK_RECOMMENDATIONS["General Well-being"]

def get_ai_recommendation(user_data):
    """
    Generate an AI recommendation based on user input.
    """
    try:
        data = preprocess_user_data(user_data)
        if isinstance(data, str):
            return data

        missing_cols = set(model.feature_names_in_) - set(data.columns)
        for col in missing_cols:
            data[col] = 0

        data = data[model.feature_names_in_]

        recommendation = model.predict(data)[0]
        book_recommendation = get_book_recommendation(user_data.get("emotional_state", "Neutral"))

        return {
            "recommendation": recommendation,
            "book": book_recommendation["title"],
            "book_link": book_recommendation["link"]
        }

    except Exception as e:
        return f"Error generating recommendation: {str(e)}"

# Example Usage
if __name__ == "__main__":
    user_input = {
        "mood_level": 3,
        "emotional_state": "Sad",
        "sleep_hours": 4.5,
        "sleep_quality": "Poor",
        "appetite_changes": "Decrease",
        "energy_levels": "Low",
        "interest_in_activities": "Lost",
        "social_engagement": "Isolated",
        "suicidal_thoughts": "No"
    }

    response = get_ai_recommendation(user_input)
    print("AI Recommendation:", response["recommendation"])
    print("Suggested Book:", response["book"], "-", response["book_link"])
