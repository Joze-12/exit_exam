from django.shortcuts import render, redirect
from .forms import *
from .models import *

def create_question_with_options(request, default=None):
    template_name = "question/create_question_with_options.html"
    
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        option_formset = OptionFormset(request.POST)
        if option_formset.is_valid():
            question = question_form.save()
            selected_option_pk = request.POST.get("selected_option")
            
            for form in option_formset:
                    option = form.save(commit=False)
                    option.question = question
                    if selected_option_pk:
                        option.is_correct = option.pk == int(selected_option_pk)
                    option.save()
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
    return render(request, "question/questions_list", questions)
