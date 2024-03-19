from django.db import models
from django.utils import timezone

from student_app.models import Student, Grade, Group

class Subject(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subjects')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

class QuizType(models.Model):
    name = models.CharField(max_length=455)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    title = models.CharField(max_length=455)
    quiz_type = models.ForeignKey(QuizType, on_delete=models.CASCADE, related_name='quizes')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

    deadline = models.DurationField(default=timezone.timedelta(minutes=30))
    max_questions = models.BigIntegerField(default=30)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, blank=True)
    no_permission_students = models.ManyToManyField(Student, blank=True)

    maximum_attempts = models.PositiveIntegerField(default=2)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']

class UserAskedAnswer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField()
    random_quizes = models.ManyToManyField(Question)
    answers = models.ManyToManyField(UserAskedAnswer)

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
