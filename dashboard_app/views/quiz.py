from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone


from student_app.models import Grade
from ..forms.quiz import SubjectForm, QuestionAddForm, QuestionForm, QuizTypeForm, QuizForm, ResultForm
from quiz_app.models import Subject, Question, Answer, QuizType, Quiz, Result
from student_app.models import Group, Student

from dashboard_app.methods import get_duration_in_minutes

# Decorators
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test


# Group
@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def subject_list(request):
    subjects = Subject.objects.all()
    grades = Grade.objects.all()

    ctx = {

        # Main
        'subjects': subjects,
        'grades': grades,
        'subject_all': True,
    }

    return render(request, 'dashboard/quiz/subject/subject_list.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def subject_list_by_grade_id(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    subjects = grade.subjects.all()
    grades = Grade.objects.all()

    ctx = {

        # Main
        'grade': grade,
        'subjects': subjects,
        'grades': grades,
        'pk': pk,
        'subject_all': False,
    }

    return render(request, 'dashboard/quiz/subject/subject_list.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def subject_create(request):
    form = SubjectForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{form.cleaned_data['title']}</b> muvaffaqqiyatli qo'shildi!")
            return redirect('subject_list')

    ctx = {
        # Main
        'form': form,
    }

    return render(request, 'dashboard/quiz/subject/subject_create.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def subject_edit(request, pk):
    instance = get_object_or_404(Subject, pk=pk)
    form = SubjectForm(instance=instance)

    questions_add = QuestionAddForm()

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{form.cleaned_data['title']}</b> muvaffaqqiyatli o'zgartirildi!")
            return redirect('subject_list')

    ctx = {
        # Main
        'form': form,
        'questions_add': questions_add,

        'instance': instance,
    }

    return render(request, 'dashboard/quiz/subject/subject_edit.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def subject_delete(request, pk):
    instance = get_object_or_404(Subject, pk=pk)
    messages.success(request, f"<b>{instance.title}</b> muvaffaqqiyatli o'chirildi!")
    instance.delete()

    return redirect('subject_list')

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def subject_checked_delete(request):
    if request.method == 'POST':
        subject_ids = request.POST.getlist('subject_ids')
        Subject.objects.filter(id__in=subject_ids).delete()

        messages.success(request, f"Tanlanganlar muvaffaqqiyatli o'chirildi!")
        return redirect('subject_list')

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def subject_add_question(request, subject_id):
    instance = get_object_or_404(Subject, pk=subject_id)

    if request.method == "POST":
        form = QuestionAddForm(request.POST)
        if form.is_valid():
            question_blocks = request.POST.get('questions').split('+++++')

            # Initialize a list to store questions and choices as dictionaries
            questions_list = []

            # Iterate through each question block and split into question and choices
            for block in question_blocks:
                lines = block.strip().split('\n')

                # Extract question text (first line) and choices (remaining lines)
                question_text = lines[0].strip()
                choices = [choice.strip()[2:] for choice in lines[1:] if choice.startswith('#')]

                # Create a dictionary for each question and append to the list
                question_dict = {'question': question_text, 'choices': choices}
                questions_list.append(question_dict)

                try:
                    # Create question
                    question = Question.objects.create(subject=instance, text=question_text, is_active=True)
                    print('44444444444')
                    for i in range(0, len(lines[1:]), 2):
                        print()
                        if lines[1:][i + 1].startswith('#'):
                            Answer.objects.create(question=question, text=lines[1:][i + 1][1:], is_correct=True)
                        else:
                            Answer.objects.create(question=question, text=lines[1:][i + 1], is_correct=False)
                except:
                    pass
            #
            # # Print the resulting list of questions
            # for question in questions_list:
            #     print("Question:", question['question'])
            #     print("Choices:", question['choices'])
            #     print("====")
            return redirect('subject_edit', pk=subject_id)
        else:
            return redirect('subject_edit', pk=subject_id)
    else:
        return redirect('subject_edit', pk=subject_id)


@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def subject_question_answer_is_active(request, question_id):
    instance = get_object_or_404(Question, pk=question_id)

    instance.is_active = not instance.is_active
    instance.save()

    return JsonResponse({'is_active': instance.is_active})

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def subject_question_detail(request, question_id):
    instance = get_object_or_404(Question, pk=question_id)
    form = QuestionForm(instance=instance)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=instance)
        if form.is_valid():
            print('#################################')
            print(request.POST)
            form.save()

            # Radio button
            true_answer_id = request.POST.get(f"question_{instance.id}")

            for choice in instance.answers.all():
                answer = get_object_or_404(Answer, pk=choice.id)
                new_answer = request.POST.get(f"answer_{choice.id}")
                answer.text = new_answer

                answer.is_correct = False

                answer.save()
            true_answer = get_object_or_404(Answer, pk=true_answer_id)
            true_answer.is_correct = True
            true_answer.save()

            messages.success(request, f"<b>{form.cleaned_data['text']}</b> muvaffaqqiyatli o'zgartirildi!")
            return redirect('subject_edit', pk=instance.subject.id)

    ctx = {
        # Main
        'form': form,

        'instance': instance,
    }

    return render(request, 'dashboard/quiz/subject/question_edit.html', ctx)

# Quiz type
@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def quiz_type_list(request):
    quiz_types = QuizType.objects.all()

    ctx = {

        # Main
        'quiz_types': quiz_types,
    }

    return render(request, 'dashboard/quiz/quiz_type/quiz_type_list.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def quiz_type_create(request):
    form = QuizTypeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{form.cleaned_data['name']}</b> muvaffaqqiyatli qo'shildi!")
            return redirect('quiz_type_list')

    ctx = {

        # Main
        'form': form,
    }

    return render(request, 'dashboard/quiz/quiz_type/quiz_type_create.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def quiz_type_edit(request, pk):
    instance = get_object_or_404(QuizType, pk=pk)
    form = QuizTypeForm(instance=instance)

    if request.method == "POST":
        form = QuizTypeForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{form.cleaned_data['name']}</b> muvaffaqqiyatli o'zgartirildi!")
            return redirect('quiz_type_list')

    ctx = {
        # Main
        'form': form,

        'instance': instance,
    }

    return render(request, 'dashboard/quiz/quiz_type/quiz_type_edit.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def quiz_type_delete(request, pk):
    instance = get_object_or_404(QuizType, pk=pk)
    messages.success(request, f"<b>{instance.name}</b> muvaffaqqiyatli o'chirildi!")
    instance.delete()

    return redirect('quiz_type_list')

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def quiz_type_checked_delete(request):
    if request.method == 'POST':
        quiz_type_ids = request.POST.getlist('quiz_type_ids')
        QuizType.objects.filter(id__in=quiz_type_ids).delete()

        messages.success(request, f"Tanlanganlar muvaffaqqiyatli o'chirildi!")
        return redirect('quiz_type_list')


# Quiz ++++
@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def quiz_list(request):
    quizes = Quiz.objects.all()

    ctx = {

        # Main
        'quizes': quizes,
    }

    return render(request, 'dashboard/quiz/quizes/list.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def quiz_create(request):
    form = QuizForm()
    if request.method == "POST":
        data = request.POST

        title = data['title']
        quiz_type_id = int(data['quiz_type'])
        start_time_str = f"{data['start_time_0']} {data['start_time_1']}"
        end_time_str = f"{data['end_time_0']} {data['end_time_1']}"
        deadline_str = data['deadline']
        max_questions = int(data['max_questions'])
        subject_id = int(data['subject'])
        group_ids = request.POST.getlist('groups')
        no_permission_student_ids = request.POST.getlist('no_permission_students')
        maximum_attempts = int(data['maximum_attempts'])
        if data.get('status'):
            status = True
        else:
            status = False

        # Datelarni timezone'ga moslash
        start_time = timezone.datetime.strptime(start_time_str, "%d.%m.%Y %H:%M:%S")
        end_time = timezone.datetime.strptime(end_time_str, "%d.%m.%Y %H:%M:%S")

        # QuizType, Subject, Group, Student modellaridan ma'lumotlarni olish
        quiz_type = QuizType.objects.get(pk=quiz_type_id)
        subject = Subject.objects.get(pk=subject_id)
        # groups = Group.objects.filter(pk__in=group_ids)
        # no_permission_students = Student.objects.filter(pk__in=no_permission_student_ids)

        # Quiz obyektini yaratish
        quiz = Quiz.objects.create(
            title=title,
            quiz_type=quiz_type,
            start_time=start_time,
            end_time=end_time,
            deadline=timezone.timedelta(hours=int(deadline_str[:2]), minutes=int(deadline_str[3:5])),
            max_questions=max_questions,
            subject=subject,
            maximum_attempts=maximum_attempts,
            status=status
        )

        # Many-to-many field'larni qo'shish
        quiz.groups.add(*group_ids)
        quiz.no_permission_students.add(*no_permission_student_ids)
        quiz.save()

        return redirect('quiz_list')
    ctx = {

        # Main
        'form': form,
    }

    return render(request, 'dashboard/quiz/quizes/create.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def quiz_edit(request, pk):
    instance = get_object_or_404(Quiz, pk=pk)
    form = QuizForm(instance=instance)

    if request.method == "POST":
        data = request.POST

        # Formdan ma'lumotlarni olish

        # Ma'lumotlarni olish
        title = data['title']
        quiz_type_id = int(data['quiz_type'])
        start_time_str = f"{data['start_time_0']} {data['start_time_1']}"
        end_time_str = f"{data['end_time_0']} {data['end_time_1']}"
        deadline_str = data['deadline']
        max_questions = int(data['max_questions'])
        subject_id = int(data['subject'])
        group_ids = request.POST.getlist('groups')
        no_permission_student_ids = request.POST.getlist('no_permission_students')
        maximum_attempts = int(data['maximum_attempts'])
        status = bool(data.get('status'))

        # Datelarni timezone'ga moslash
        start_time = timezone.datetime.strptime(start_time_str, "%d.%m.%Y %H:%M:%S")
        end_time = timezone.datetime.strptime(end_time_str, "%d.%m.%Y %H:%M:%S")

        # QuizType, Subject, Group, Student modellaridan ma'lumotlarni olish
        quiz_type = QuizType.objects.get(pk=quiz_type_id)
        subject = Subject.objects.get(pk=subject_id)

        # Obyekt ma'lumotlarini yangilash
        instance.title = title
        instance.quiz_type = quiz_type
        instance.start_time = start_time
        instance.end_time = end_time
        instance.deadline = timezone.timedelta(hours=int(deadline_str[:2]), minutes=int(deadline_str[3:5]))
        instance.max_questions = max_questions
        instance.subject = subject
        instance.maximum_attempts = maximum_attempts
        instance.status = status

        # Many-to-many field'larni qo'shish
        instance.groups.set(group_ids)
        instance.no_permission_students.set(no_permission_student_ids)

        # Obyektni saqlash
        instance.save()

        messages.success(request, f"<b>{title}</b> muvaffaqqiyatli o'zgartirildi!")
        return redirect('quiz_list')

    ctx = {
        # Main
        'form': form,

        'instance': instance,
    }

    return render(request, 'dashboard/quiz/quizes/edit.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def quiz_delete(request, pk):
    instance = get_object_or_404(Quiz, pk=pk)
    messages.success(request, f"<b>{instance.title}</b> muvaffaqqiyatli o'chirildi!")
    instance.delete()

    return redirect('quiz_list')

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def quiz_checked_delete(request):
    if request.method == 'POST':
        quiz_ids = request.POST.getlist('quiz_ids')
        Quiz.objects.filter(id__in=quiz_ids).delete()

        messages.success(request, f"Tanlanganlar muvaffaqqiyatli o'chirildi!")
        return redirect('quiz_list')

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def quiz_is_active(request, quiz_id):
    instance = get_object_or_404(Quiz, pk=quiz_id)

    instance.status = not instance.status
    instance.save()

    return JsonResponse({'status': instance.status})


# Result ++++
@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def result_list(request):
    results = Result.objects.all()
    quizes = Quiz.objects.all()

    ctx = {

        # Main
        'results': results,
        'quizes': quizes
    }

    return render(request, 'dashboard/quiz/results/list.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def result_list_by_quiz_id(request, pk):
    quiz = Quiz.objects.get(id=pk)
    results = Result.objects.filter(quiz=quiz)

    ctx = {

        # Main
        'results': results,
        'quiz': quiz
    }

    return render(request, 'dashboard/quiz/results/list-quiz.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def excel_create_results_by_quiz_id(request, pk):
    quiz = Quiz.objects.get(id=pk)
    results = Result.objects.filter(quiz=quiz)


    ctx = {

        # Main
        'results': results,
        'quiz': quiz
    }

    return render(request, 'dashboard/quiz/results/list-quiz.html', ctx)
@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_superuser, login_url='/dashboard/')
def result_create(request):
    form = ResultForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            student = get_object_or_404(Student, pk=int(request.POST['student']))
            form.save()

            messages.success(request, f"<b>{student}</b> natijasi muvaffaqqiyatli qo'shildi!")
            return redirect('result_list')
        else:
            messages.error(request, "<b>Xatolik!</b> Bu talabaning urinishlar soni tugagan!")


    ctx = {

        # Main
        'form': form,
    }

    return render(request, 'dashboard/quiz/results/create.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_superuser, login_url='/dashboard/')
def result_edit(request, pk):
    instance = get_object_or_404(Result, pk=pk)
    form = ResultForm(instance=instance)

    if request.method == "POST":
        form = ResultForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            messages.success(request, f"<b>{instance.student}</b> natijasi muvaffaqqiyatli o'zgartirildi!")
            return redirect('result_list')
        else:
            print(form.errors)

    ctx = {
        # Main
        'form': form,

        'instance': instance,
    }

    return render(request, 'dashboard/quiz/results/edit.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_superuser, login_url='/dashboard/')
def result_delete(request, pk):
    instance = get_object_or_404(Result, pk=pk)
    messages.success(request, f"<b>{instance.student}</b> natijasi muvaffaqqiyatli o'chirildi!")
    instance.delete()

    return redirect('quiz_list')

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_superuser, login_url='/dashboard/')
def result_checked_delete(request):
    if request.method == 'POST':
        result_ids = request.POST.getlist('result_ids')
        Result.objects.filter(id__in=result_ids).delete()

        messages.success(request, f"Tanlanganlar muvaffaqqiyatli o'chirildi!")
        return redirect('result_list')
