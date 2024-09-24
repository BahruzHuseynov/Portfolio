from core import models as core_models


def created_profession_map(question_id):
    questions = core_models.Questions.objects.filter(id=question_id). \
        values("question__answer_title", "question__id")
    return {question['question__answer_title']: question['question__id'] for question in questions}


def checked_user_profession_answer(user_answer, map_result):
    if user_answer >= 600:
        return map_result["700"]
    elif user_answer >= 500:
        return map_result["600"]
    elif user_answer >= 400:
        return map_result["500"]
    elif user_answer >= 300:
        return map_result["400"]
    else:
        return map_result["300"]
