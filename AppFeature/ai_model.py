def get_ai_recommendation(data):
    """
    Simple AI logic to generate a recommendation based on user input.
    """
    recommendations = []

    # Check if the mood is too low
    if data["mood_level"] <= 3:
        recommendations.append("Consider talking to a therapist or a close friend about your feelings.")

    # Sleep issues
    if data["sleep_hours"] < 5 or data["sleep_quality"] == "Poor":
        recommendations.append("Try maintaining a regular sleep schedule and avoiding screens before bed.")

    # Low interest in activities
    if data["interest_in_activities"] in ["Decreased", "Lost"]:
        recommendations.append("Engage in activities you once enjoyed, even if they seem difficult at first.")

    # Suicidal thoughts
    if data["suicidal_thoughts"]:
        recommendations.append("Please reach out to a crisis helpline immediately. You're not alone.")

    # General well-being
    if not recommendations:
        recommendations.append("You're doing great! Keep up with your self-care routine.")

    return recommendations
