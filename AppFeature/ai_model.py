# import joblib
# import os
# import pandas as pd

# # Load the trained model
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "ai_mood_recommendation.pkl")
# model = joblib.load(MODEL_PATH)

# # Define categorical encoding mappings OUTSIDE the function
# ENCODING_MAP = {
#     "sleep_quality": {"Poor": 0, "Average": 1, "Good": 2},
#     "interest_in_activities": {"Lost": 0, "Decreased": 1, "Normal": 2},
#     "suicidal_thoughts": {"Yes": 1, "No": 0},
# }

# # Define recommendation mappings
# RECOMMENDATION_MAP = {
#     1: "Please seek immediate help. Contact a crisis helpline.",
#     2: "Consider talking to a therapist or a close friend about your feelings.",
#     3: "You're doing great! Keep up with your self-care routine."
# }

# def get_ai_recommendation(user_data):
#     """
#     Convert user input to numerical data and get AI-generated recommendations.
#     """
#     try:
#         # Convert categorical values to numerical values
#         user_data["sleep_quality"] = ENCODING_MAP["sleep_quality"].get(user_data.get("sleep_quality", "Average"), 1)
#         user_data["interest_in_activities"] = ENCODING_MAP["interest_in_activities"].get(user_data.get("interest_in_activities", "Decreased"), 1)
#         user_data["suicidal_thoughts"] = ENCODING_MAP["suicidal_thoughts"].get(user_data.get("suicidal_thoughts", "No"), 0)

#         # Convert to DataFrame
#         data = pd.DataFrame([user_data])

#         # Make prediction (Now returns a recommendation string)
#         recommendation = model.predict(data)[0]

#         return recommendation

#     except Exception as e:
#         return f"Error processing request: {str(e)}"

import joblib
import os
import pandas as pd

# Load the trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ai_mood_recommendation.pkl")
model = joblib.load(MODEL_PATH)

# Define categorical encoding mappings OUTSIDE the function
ENCODING_MAP = {
    "sleep_quality": {"Poor": 0, "Average": 1, "Good": 2},
    "interest_in_activities": {"Lost": 0, "Decreased": 1, "Normal": 2},
    "suicidal_thoughts": {"Yes": 1, "No": 0},
}

def get_ai_recommendation(user_data):
    """
    Convert user input to numerical data and get AI-generated recommendations.
    """
    try:
        # Convert categorical values to numerical values
        user_data["sleep_quality"] = ENCODING_MAP["sleep_quality"].get(user_data.get("sleep_quality", "Average"), 1)
        user_data["interest_in_activities"] = ENCODING_MAP["interest_in_activities"].get(user_data.get("interest_in_activities", "Decreased"), 1)
        user_data["suicidal_thoughts"] = ENCODING_MAP["suicidal_thoughts"].get(user_data.get("suicidal_thoughts", "No"), 0)

        # Convert to DataFrame
        data = pd.DataFrame([user_data])

        # Make prediction (Returns an AI-generated recommendation string)
        recommendation = model.predict(data)[0]

        return recommendation

    except Exception as e:
        return f"Error processing request: {str(e)}"
