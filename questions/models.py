from django.db import models
from ckeditor.fields import RichTextField

class Question(models.Model):
    question_text = RichTextField(default="")
    explanation = RichTextField(default="")
    is_exam_question = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

class Options(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    value = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)


class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title