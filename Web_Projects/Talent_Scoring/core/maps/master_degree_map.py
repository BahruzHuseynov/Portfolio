from core import models as core_models


def created_master_degree_map(question_id):
    questions = core_models.Questions.objects.filter(id=question_id). \
        values("question__answer_title", "question__id")
    return {question['question__answer_title']: question['question__id'] for question in questions}


def checked_user_master_degree_answer(user_answer, map_result):
    if user_answer >= 100:
        return map_result["100"]
    elif user_answer >= 80:
        return map_result["80"]
    elif user_answer >= 60:
        return map_result["60"]
    elif user_answer >= 40:
        return map_result["40"]
    else:
        return map_result["20"]
