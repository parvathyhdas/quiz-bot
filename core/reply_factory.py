
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not answer:
        return False, "Answer is empty or invalid."

    session_key = 'answer_for_question_{}'.format(current_question_id)
    session[session_key] = answer
    session.modified = True
    return True, "Answer recorded successfully."


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    PYTHON_QUESTION_LIST = [
        {"id": 1, "question": "What is Python?"},
        {"id": 2, "question": "What are Python modules?"},
        {"id": 3, "question": "What is PEP 8?"},
        # Add more questions as needed
    ]

    current_question_id = int(current_question_id)
    for index, question in enumerate(PYTHON_QUESTION_LIST):
        if question["id"] == current_question_id:
            if index + 1 < len(PYTHON_QUESTION_LIST):
                next_question = PYTHON_QUESTION_LIST[index + 1]
                return next_question["question"], next_question["id"]

    return "No more questions", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    PYTHON_QUESTION_LIST = [
        {"id": 1, "question": "What is Python?", "correct_answer": "A programming language"},
        {"id": 2, "question": "What are Python modules?", "correct_answer": "Reusable code files"},
        {"id": 3, "question": "What is PEP 8?", "correct_answer": "Style guide for Python code"},
        # Add more questions with their correct answers
    ]

    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = 0

    for question in PYTHON_QUESTION_LIST:
        session_key = 'answer_for_question_{}'.format(question["id"])
        if session_key in session:
            user_answer = session[session_key]
            if user_answer == question["correct_answer"]:
                correct_answers += 1

    score = (correct_answers / total_questions) * 100
    result_message = "You answered {} out of {} questions correctly. Your score is {:.2f}%.".format(
        correct_answers, total_questions, score
    )

    return result_message
