import json
import random
import signal


# File Handling & Data Management

def load_questions(filename):
    with open(filename, "r") as file:
        return json.load(file)


def save_questions(filename, questions):
    with open(filename, "w") as file:
        json.dump(questions, file, indent=4)


# Question Display & Answer Handling

class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException


def ask_question(q, time_limit=10):
    print("\n" + q["question"])

    for i, option in enumerate(q["options"], 1):
        print(f"{i}. {option}")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(time_limit)

    try:
        answer = input(
            f"\nYou have {time_limit} seconds. Enter option number: "
        )
        signal.alarm(0)  # Cancel timer if answered

    except TimeoutException:
        print("\nTime's up!")
        return False

    try:
        selected = q["options"][int(answer) - 1]

    except (ValueError, IndexError):
        print("Invalid input")
        return False

    if selected == q["answer"]:
        print("Correct")
        return True

    else:
        print("Wrong. Correct answer:", q["answer"])
        return False


# Quiz Flow Controller

def run_quiz():

    filename = "questions.json"
    questions = load_questions(filename)

    total_available = len(questions)

    while True:

        try:
            num_questions = int(
                input(
                    f"How many questions do you want? "
                    f"(Max {total_available}): "
                )
            )

            if num_questions > total_available:
                print(
                    f"Error: Only {total_available} questions available."
                )

            elif num_questions <= 0:
                print("Error: Enter a number greater than 0.")

            else:
                break

        except ValueError:
            print("Invalid input. Enter a number.")

    selected_questions = random.sample(
        questions,
        num_questions
    )

    score = 0
    incorrect = []

    for q in selected_questions:

        q["attempts"] += 1

        if ask_question(q):
            score += 1

        else:
            q["fail_count"] += 1
            incorrect.append(q)

    print("\nQuiz Finished")
    print(
        f"Score: {score}/{len(selected_questions)}"
    )

    # Review System & Performance Analysis

    if incorrect:

        print("\nReview Incorrect Answers:")

        for q in incorrect:

            fail_percent = (
                q["fail_count"] / q["attempts"]
            ) * 100

            print("\nQuestion:", q["question"])
            print("Correct Answer:", q["answer"])
            print(
                f"Failure Rate: {fail_percent:.2f}%"
            )

    # Statistics & Instructor Insights

    topic_stats = {}

    for q in questions:

        topic = q["topic"]

        if topic not in topic_stats:

            topic_stats[topic] = {
                "fail": 0,
                "attempts": 0
            }

        topic_stats[topic]["fail"] += q["fail_count"]
        topic_stats[topic]["attempts"] += q["attempts"]

    print("\nTopic-wise Statistics:")

    for topic, stats in topic_stats.items():

        if stats["attempts"] > 0:

            fail_rate = (
                stats["fail"] / stats["attempts"]
            ) * 100

            print(
                f"{topic}: {fail_rate:.2f}% failure rate"
            )

    save_questions(filename, questions)


# Program Entry Point
if __name__ == "__main__":
    run_quiz()
