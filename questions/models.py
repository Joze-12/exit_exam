from django.db import models
from ckeditor.fields import RichTextField
from random import sample
from academics.models import Course, Theme

class Question(models.Model):
    class ChooseFrom(models.TextChoices):
        ALL = "ALL", "All"
        COURSE = "COURSE", "Course"
        THEME = "THEME", "Theme"


    question_text = RichTextField(default="")
    explanation = RichTextField(default="")
    choose_from = models.CharField(max_length=6, choices=ChooseFrom.choices, default=ChooseFrom.ALL)
    course = models.ForeignKey("academics.Course", on_delete=models.SET_NULL, null=True, blank=True)
    theme = models.ForeignKey("academics.Theme", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.question_text
    
    def get_question_text(self):
        return self.question_text

    def set_question_text(self, new_text):
        self.question_text = new_text
        self.save()

    def get_explanation(self):
        return self.explanation

    def set_explanation(self, new_explanation):
        self.explanation = new_explanation
        self.save()

    def get_options(self):
        return self.options.all()

    def get_correct_option(self):
        try:
            return self.options.get(is_correct=True)
        except Options.DoesNotExist:
            return None
        
    def get_course(self):
        return self.course
    
    def set_course(self, course_object):
        if isinstance(course_object, Course):
            self.course = course_object
    
    def get_theme(self):
        return self.course.theme
    
    @staticmethod
    def get_questions_with_correct_options():
        return Question.objects.filter(options__is_correct=True).distinct()
    
    @staticmethod
    def get_total_questions():
        return Question.objects.count()
    
    @staticmethod
    def get_random_questions(num_questions):
        if num_questions <= 0:
            return []

        total_questions = Question.objects.count()
        if total_questions == 0:
            return []

        num_questions_to_fetch = min(num_questions, total_questions)

        # Fetch all questions and randomize their order
        all_questions = list(Question.objects.all().order_by('?'))

        # Get a random sample of specified number of questions
        return sample(all_questions, num_questions_to_fetch)
    
    @staticmethod
    def get_random_questions_by_course(course, num_questions):
        if num_questions <= 0:
            return []

        # Filter questions based on the given course
        all_questions = Question.objects.filter(course=course)

        total_questions = all_questions.count()
        if total_questions == 0:
            return []

        num_questions_to_fetch = min(num_questions, total_questions)

        # Randomize the order of filtered questions
        all_questions = list(all_questions.order_by('?'))

        # Get a random sample of specified number of questions
        return sample(all_questions, num_questions_to_fetch)
    
    @staticmethod
    def get_random_questions_by_theme(theme, num_questions):
        if num_questions <= 0:
            return []

        # Filter questions based on the given course
        all_questions = Question.objects.filter(theme=theme)

        total_questions = all_questions.count()
        if total_questions == 0:
            return []

        num_questions_to_fetch = min(num_questions, total_questions)

        # Randomize the order of filtered questions
        all_questions = list(all_questions.order_by('?'))

        # Get a random sample of specified number of questions
        return sample(all_questions, num_questions_to_fetch)
    

class Options(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    value = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def get_value(self):
        return self.value

    def set_value(self, new_value):
        self.value = new_value
        self.save()

    def is_correct_option(self):
        return self.is_correct

    def set_correct_option(self, is_correct):
        self.is_correct = is_correct
        self.save()

class Exam(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

class ExamQuestion(models.Model):
    question_text = RichTextField(default="")
    explanation = RichTextField(default="")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

class ExamOptions(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="exam_options")
    value = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

