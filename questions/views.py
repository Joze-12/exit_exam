from django.shortcuts import render, redirect
from .forms import *
from .models import *

def create_question_with_options(request, default=None):
    template_name = "question/create_question_with_options.html"
    
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        option_formset = OptionFormset(request.POST)

        print(int(request.POST.get("selected_option")))
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
