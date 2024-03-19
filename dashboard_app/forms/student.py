from django.forms import ModelForm, TextInput, Select, Form, FileField, FileInput

from student_app.models import Grade, Group, Student

class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ['grade']
        widgets = {
            'grade': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kursni kiriting. . .'
            })
        }

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['grade', 'type_group', 'group_name']
        widgets = {
            'grade': Select(attrs={
                'class': 'form-control',
            }),
            'group_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Guruh nomini kiriting. . .',
            }),
            'type_group': Select(attrs={
                'class': 'form-control'
            })
        }

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['group', 'name']
        widgets = {
            'group': Select(attrs={
                'class': 'form-control',
            }),
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ism Familiyani kiriting. . .',
            })
        }

class StudentCreateExcelForm(Form):
    excel = FileField(widget=FileInput(attrs={
        'class': 'form-control',
        'id': 'excel',
    }))