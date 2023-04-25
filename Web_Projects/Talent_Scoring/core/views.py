from django.shortcuts import render, redirect
from django.urls import reverse

from core import models as core_model
from base_user import models as base_model
from core.maps.profession_map import created_profession_map, checked_user_profession_answer
from core.maps.bachelor_map import created_bachelor_map, checked_user_bachelor_answer
from core.maps.master_degree_map import created_master_degree_map, \
    checked_user_master_degree_answer
from core.maps.phd_map import created_phd_map, checked_user_phd_answer
from base_user.models import ResultAnswersModel
from core.forms import ContactForm



def home_view(request):
    return render(request, 'home/home.html')






def _create_answer_results_dict(*args):
    question, answer, weight_number, weight_type = args
    final_dict = {'question': question, 'answer': answer, 'weight_number': weight_number, 'weight_type': weight_type}

    if question in "Bakalavr" and question in "Magistiratura":

        final_dict['weight_type'] = "average_weight_multiply"

    return final_dict


def _get_answer_data(answer):
    return (answer.question_id.question_title,
            answer.answer_title,
            answer.answer_weight,
            answer.question_id.formula)


def _get_questions(answer_ids):
    data_list = []
    for answer_id in answer_ids:
        answer = core_model.Answers.objects.filter(id=int(answer_id)).last()
        answers = _get_answer_data(answer)
        answer_results = _create_answer_results_dict(*answers)
        data_list.append(answer_results)
    return data_list


def stage_one_view(request):
    if request.method == 'POST':
        age, fullname, answer_id_3, answer_id_4, answer_id_5 = _extract_stage_one_request_data(request)
        result_questions_data = _get_questions([answer_id_3, answer_id_4, answer_id_5])
        created_user = base_model.MyUser.objects.filter(id=request.user.id).last()

        _create_answer_results(created_user.id, result_questions_data)

        queryset = core_model.Answers.objects.filter(id=int(answer_id_4)).last()
        return redirect(_get_stage_url(queryset))
    stage = core_model.StageModel.objects.all().order_by('order_by')[0]
    questions = stage.stage_question_id.all().order_by('stage_question__stage_question_id__order_by')[:5]
    context = {'stage': stage, "questions": questions}
    return render(request, 'processes/first.html', context)


def _extract_stage_one_request_data(request):
    fullname = request.user.fullname
    age = request.POST.get('age')
    question_3 = request.POST.get('question-3')
    question_4 = request.POST.get('question-4')
    question_5 = request.POST.get('question-5')

    return age, fullname, question_3, question_4, question_5


def _get_stage_url(queryset):
    url = reverse("core:stage_two_page", kwargs={'q': queryset.answer_title})
    if 'orta' in queryset.answer_title:
        url = reverse("core:stage_three_page")
    return url


def _create_answer_results(created_user, result_questions_data):
    for result_question_data in result_questions_data:
        base_model.ResultAnswersModel.objects.create(
            user_id_id=created_user,
            question_name=result_question_data.get('question'),
            answer_name=result_question_data.get('answer'),
            weight_number=result_question_data.get('weight_number') if result_question_data.get('weight_number', False) else 0.0,
            weight_type=result_question_data.get('weight_type')
        )


def stage_two_view(request, q):
    if request.method == 'POST':
        question_6, question_7, question_8, question_9 = _get_stage_two_request_question_data(request)
        answer_6, answer_7, answer_8, answer_9 = _get_stage_two_request_answer_data(request)
        _create_answer_results(request.user.id,
                               _get_answer_stage_two(answer_6,
                                                     answer_7,
                                                     answer_8,
                                                     answer_9,
                                                     question_6,
                                                     question_7,
                                                     question_8,
                                                     question_9))
        url = reverse("core:stage_three_page")
        return redirect(url)

    stage = core_model.StageModel.objects.all().order_by('order_by')[1]
    context = {'questions': stage.stage_question_id.filter(related_question__answer_title=q).order_by('order_by'),
               'stage': stage}

    return render(request, 'processes/second.html', context)


def _get_answer_stage_two(answer_6, answer_7, answer_8, answer_9, question_6, question_7, question_8, question_9):
    finished_answer_data = []

    if answer_6:
        answer_id = checked_user_profession_answer(int(answer_6),
                                                   created_profession_map(question_6))
        result_questions_data = _get_questions([answer_id])
        finished_answer_data.append(result_questions_data[0])

    if answer_7:
        answer_id = checked_user_bachelor_answer(int(answer_7),
                                                 created_bachelor_map(question_7))
        print(answer_id)
        result_questions_data = _get_questions([answer_id])
        finished_answer_data.append(result_questions_data[0])

    if answer_8:
        answer_id = checked_user_master_degree_answer(int(answer_8),
                                                      created_master_degree_map(question_8))
        result_questions_data = _get_questions([answer_id])
        finished_answer_data.append(result_questions_data[0])

    if answer_9:
        answer_id = checked_user_phd_answer(int(answer_9), created_phd_map(question_9))
        result_questions_data = _get_questions([answer_id])
        finished_answer_data.append(result_questions_data[0])

    return finished_answer_data


def _get_stage_two_request_question_data(request):
    question_6 = request.POST.get('question-6')  # Pese
    question_7 = request.POST.get('question-7')  # Bakalavr
    question_8 = request.POST.get('question-8')  # Magistr
    question_9 = request.POST.get('question-9')  # PHD
    return question_6, question_7, question_8, question_9


def _get_stage_two_request_answer_data(request):
    answer_6 = request.POST.get('answer-6')  # Pese
    answer_7 = request.POST.get('answer-7')  # Bakalavr
    answer_8 = request.POST.get('answer-8')  # Magistr
    answer_9 = request.POST.get('answer-9')  # PHD
    return answer_6, answer_7, answer_8, answer_9


def stage_three_view(request):
    if request.method == 'POST':
        question_10, question_11, question_12, question_13 = _extract_stage_three_request_data(request)
        result_questions_data = _get_questions([question_10,
                                                question_11,
                                                question_12,
                                                question_13])

        _create_answer_results(request.user.id, result_questions_data)

        print(result_questions_data)
        print(question_10, '{question_10}')
        print(question_11, '{question_11}')
        print(question_12, '{question_12}')
        print(question_13, '{question_13}')

        # Updated your user model here
        url = reverse("core:result_page")
        return redirect(url)
    stage = core_model.StageModel.objects.all().order_by('order_by')[2]
    context = {'stage': stage,
               'questions': stage.stage_question_id.all().order_by('order_by')}

    return render(request, 'processes/third.html', context)


def _extract_stage_three_request_data(request):
    question_10 = request.POST.get('question-10')
    question_11 = 11
    question_12 = request.POST.get('question-12')
    question_13 = request.POST.get('question-13')
    return question_10, question_11, question_12, question_13


def result_view(request):
    total_weight = 0
    stage_two_weight = 0

    result_answers_data = ResultAnswersModel.objects.filter(user_id=request.user.id)

    for result_answer_data in result_answers_data:
        if result_answer_data.weight_type == 'average_weight_multiply':
            stage_two_weight += result_answer_data.weight_number
            print("Merhele 2 average_weight_multiply", result_answer_data, result_answer_data.weight_number)
            print(stage_two_weight)
        if result_answer_data.weight_type == 'multiply_weight':
            total_weight += result_answer_data.weight_number
            print("multiply_weight",result_answer_data, result_answer_data.weight_number)
        else:
            total_weight += 1

    url = reverse("core:fail_page")

    print(total_weight)

    my_user = base_model.MyUser.objects.filter(id=request.user.id).last()
    my_user.total_score = total_weight
    my_user.save()

    if total_weight < 2:
        url = reverse("core:success_page")

    return redirect(url)


def success_page_view(request):
    result_answers_data_delete = ResultAnswersModel.objects.filter(user_id=request.user.id)
    result_answers_data_delete.delete()
    return render(request, 'processes/success.html')


def fail_page_view(request):
    result_answers_data_delete = ResultAnswersModel.objects.filter(user_id=request.user.id)
    result_answers_data_delete.delete()
    return render(request, 'processes/fail.html')



def about_us_view(request):
    return render(request,
                  'about us/about.html',
                  {"about_data": core_model.AboutUs.objects.all().last()})


def contact_view(request):
    context = {}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:index")
        else:
            context['form'] = form
            return render(request, 'contact/contact.html', context)

    form = ContactForm()
    context['form'] = form
    return render(request, 'contact/contact.html', context)