
"""Online examination system with grading and result calculation."""

import hmac
import secrets

QUESTIONS = [
    {"q": "What is 2 + 2?", "answer": "4"},
    {"q": "Which keyword defines a function in Python?", "answer": "def"},
    {"q": "What does CPU stand for?", "answer": "Central Processing Unit"},
    {"q": "Which type is immutable: list or tuple?", "answer": "tuple"},
]

results = {}


def answers_match(given, correct):
    """Compare normalized answers securely."""
    given_bytes = given.strip().lower().encode("utf-8")
    correct_bytes = correct.strip().lower().encode("utf-8")
    return hmac.compare_digest(given_bytes, correct_bytes)


def pick_bonus_question():
    """Select a random bonus question securely."""
    return secrets.choice(QUESTIONS)["q"]


def grade_student(student_name, responses, penalties=None):
    """Calculate a student's score and record incorrect answers."""
    if penalties is None:
        penalties = {}

    score = 0
    for index, question in enumerate(QUESTIONS):
        given = responses.get(index, "")
        if answers_match(given, question["answer"]):
            score += 1
        else:
            penalties[student_name] = penalties.get(student_name, 0) + 1

    results[student_name] = score
    return score


def get_grade(score):
    """Return a letter grade based on the percentage score."""
    percent = score * 100 / len(QUESTIONS)

    if percent >= 90:
        return "A"
    if percent >= 60:
        return "B"
    return "C"


def class_average():
    """Calculate the average score of the class."""
    if not results:
        return 0
    return round(sum(results.values()) / len(results), 2)


def topper():
    """Return the name of the student with the highest score."""
    if not results:
        return None
    return max(results, key=results.get)


def main():
    """Run the online examination demonstration."""
    print("Bonus question:", pick_bonus_question())

    grade_student("Anil", {0: "4", 1: "def", 2: "Core Power Unit"})
    grade_student(
        "Divya",
        {0: "4", 1: "def", 2: "central processing unit", 3: "tuple"},
    )
    grade_student("Sameer", {0: "5", 3: "list"})

    for name, score in results.items():
        print(name, "scored", score, "grade", get_grade(score))

    average = class_average()
    print("Class average:", average)
    print("Topper:", topper())
    print(
        "Students who sat the exam:",
        ", ".join(sorted(results)),
        "| total:",
        len(results),
    )


if __name__ == "__main__":
    main()
