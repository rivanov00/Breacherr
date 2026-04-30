import re

def analyze_password(password: str):
    """
    Analyzes password strength and returns a score and feedback.
    """
    if not password:
        return {"score": 0, "label": "N/A", "feedback": "Няма открита парола."}

    score = 0
    feedback = []

    # Length check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Паролата е твърде къса (мин. 8 знака).")

    # Complexity checks
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Липсват главни букви.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Липсват цифри.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Липсват специални символи.")

    if len(password) >= 12:
        score += 1

    labels = ["Много слаба", "Слаба", "Средна", "Добра", "Силна", "Отлична"]
    label = labels[min(score, 5)]

    # Estimation of crack time (simplified)
    # 0-1: seconds, 2: minutes, 3: days, 4: years, 5: centuries
    crack_times = [
        "секунди", "няколко минути", "няколко часа", 
        "месеци", "години", "векове"
    ]
    crack_time = crack_times[min(score, 5)]

    return {
        "score": score, # 0 to 5
        "label": label,
        "crack_time": crack_time,
        "feedback": feedback
    }
