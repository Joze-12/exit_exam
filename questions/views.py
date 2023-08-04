from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.views import View
from django.http import JsonResponse



def create_question_with_options(request, default=None):
    template_name = "question/create_question_with_options.html"
    
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        option_formset = OptionFormset(request.POST)

        if question_form.is_valid() and option_formset.is_valid():
            question = question_form.save()
            i = 1
            for form in option_formset.forms:
                if form.cleaned_data.get("value") is None:
                    continue
                else:
                    option = form.save(commit=False)
                    option.question = question
                    if int(request.POST.get("selected_option")) == i:
                        option.is_correct = True
                    option.save()
                    i+=1

            # Check if the "Add More Question" button was clicked.
            if request.POST.get("add_more_question") == "1":
                # Create new empty forms for the next question.
                question_form = QuestionForm()
                option_formset = OptionFormset(queryset=Options.objects.none())
                return render(
                    request, 
                    template_name,
                    {
                        "question_form": question_form,
                        "option_formset": option_formset,
                    }
                )
            else:
                return redirect("questions_list")

    else:
        question_form = QuestionForm(request.GET or None)
        option_formset = OptionFormset(queryset=Options.objects.none())

    return render(
        request, 
        template_name,
        {
            "question_form": question_form,
            "option_formset": option_formset,
        }
    )
    
def list_questions(request):
    questions = Question.objects.all()
    context = {
        "questions": questions
    }
    return render(request, "question/questions_list.html", context)

from django.http import HttpResponseRedirect
from django.urls import reverse

def start_practice(request):
    return render(request, 'dashboards/start_practice.html')

def fetch_questions(request):
    num_questions = int(request.GET.get('num_questions', 0))
    if num_questions <= 0:
        # Fetch all questions if the number is invalid or not provided
        questions = Question.objects.all()
    else:
        # Fetch random questions based on the specified number
        questions = Question.get_random_questions(num_questions)
    
    return render(request, 'dashboards/practice_questions.html', {'questions': questions})

def calculate_score(selected_options):
    total_questions = len(selected_options)
    if total_questions == 0:
        return 0.0  # Return 0 score if no questions were answered

    correct_count = sum(1 for option in selected_options if option.is_correct_option())
    return round(correct_count / total_questions * 100, 2)

def practice_result(request):
    if request.method == "POST":
        selected_options = []
        answered_question_ids = []

        # Collect selected options and the IDs of answered questions
        for question in Question.objects.all():
            option_id = request.POST.get(f'question_{question.id}')
            if option_id:
                option = Options.objects.get(pk=option_id)
                selected_options.append(option)
                answered_question_ids.append(question.id)

        score = calculate_score(selected_options)

        # Fetch the randomly selected questions that were answered
        questions = Question.objects.filter(pk__in=answered_question_ids)

        result = []
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            selected_option = None
            if selected_option_id:
                selected_option = Options.objects.get(pk=selected_option_id)

            correct_option = question.get_correct_option()
            explanation = question.explanation

            result.append({
                'question_text': question.question_text,
                'options': [
                    {'value': option.value, 'is_correct': option.is_correct_option()} 
                    for option in question.get_options()
                ],
                'selected_option': selected_option.value if selected_option else None,
                'correct_option': correct_option.value,
                'explanation': explanation,
            })

        context = {
            'score': score,
            'result': result,
        }

        return render(request, 'dashboards/practice_result.html', context)
    
    else:
        # Redirect to the start_practice view if accessed directly without selecting any options
        return HttpResponseRedirect(reverse('start_practice'))