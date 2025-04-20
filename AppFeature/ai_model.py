import joblib
import os
import pandas as pd
import random

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

# Define book recommendations
BOOK_RECOMMENDATIONS = {
    "Happy": [
        ("The Happiness Advantage", "https://amzn.to/3XYZ123"),
        ("The Power of Now", "https://amzn.to/3XYZ456")
    ],
    "Sad": [
        ("The Gifts of Imperfection", "https://amzn.to/3XYZ789"),
        ("Man’s Search for Meaning", "https://amzn.to/3XYZ012")
    ],
    "Anxious": [
        ("Dare", "https://amzn.to/3XYZ345"),
        ("The Anxiety and Phobia Workbook", "https://amzn.to/3XYZ678")
    ],
    "Stressed": [
        ("Burnout: The Secret to Unlocking the Stress Cycle", "https://amzn.to/3XYZ901"),
        ("The Relaxation and Stress Reduction Workbook", "https://amzn.to/3XYZ234")
    ],
    "Calm": [
        ("The Book of Joy", "https://amzn.to/3XYZ567"),
        ("Wherever You Go, There You Are", "https://amzn.to/3XYZ890")
    ],
    "Depressed": [
        ("Feeling Good: The New Mood Therapy", "https://amzn.to/3XYZ123"),
        ("Lost Connections", "https://amzn.to/3XYZ456")
    ]
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

        emotional_state = user_data.get("emotional_state", "Neutral")
        book_recommendation = random.choice(BOOK_RECOMMENDATIONS.get(emotional_state, [("A Mindfulness Guide for the Frazzled", "https://amzn.to/default")]))

        return {
            "AI_Recommendation": recommendation,
            "Book_Recommendation": book_recommendation[0],
            "Book_Link": book_recommendation[1]
        }
    except Exception as e:
        return f"Error generating recommendation: {str(e)}"


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
        "suicidal_thoughts": "Yes"
    }

    result = get_ai_recommendation(user_input)
    print("AI Recommendation:", result["AI_Recommendation"])
    print("Suggested Book:", result["Book_Recommendation"])
    print("Book Link:", result["Book_Link"])
