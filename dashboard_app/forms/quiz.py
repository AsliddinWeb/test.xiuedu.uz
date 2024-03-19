from django import forms

from quiz_app.models import Subject, Question, QuizType, Quiz, Result
from student_app.models import Student, Group


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['title', 'grade']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fan nomini kiriting. . .'
            }),
            'grade': forms.Select(attrs={
                'class': 'form-control',
            })
        }

class QuestionAddForm(forms.Form):
    questions = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Savollarni kiriting. . .'
    }), required=True)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'is_active']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }

class QuizTypeForm(forms.ModelForm):
    class Meta:
        model = QuizType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Imtihon turini kiriting. . .'
            })
        }

group_choices = [(group.id, group.group_name) for group in Group.objects.all()]
student_choices = [(student.id, student.name) for student in Student.objects.all()]

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'quiz_type', 'start_time', 'end_time', 'deadline', 'max_questions', 'subject', 'groups', 'no_permission_students', 'maximum_attempts', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Imtihon nomini kiriting. . .'
            }),
            'quiz_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'start_time': forms.SplitDateTimeWidget(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.SplitDateTimeWidget(attrs={
                'class': 'form-control',
            }),
            'deadline': forms.TimeInput(attrs={
                'class': 'form-control',
            }),
            'max_questions': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Savollar soni. . ."
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
            }),
            'groups': forms.SelectMultiple(choices=group_choices, attrs={
                'class': 'form-control'
            }),
            'no_permission_students': forms.SelectMultiple(choices=student_choices, attrs={
                'class': 'form-control'
            }),
            'maximum_attempts': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            })
        }

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'quiz', 'score', 'status']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control',
            }),
            'score': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'quiz': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            })
        }