from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Permission
from django.contrib.auth.decorators import login_required, user_passes_test

# Random
import random

# Time
from django.utils import timezone

# Responses
from django.http import JsonResponse, HttpResponse

from student_app.models import Student, Group, Grade
from quiz_app.models import Quiz, Result, UserAskedAnswer, Answer

#######

def get_random_questions(quiz, num_questions):
    # Ma'lumotlarni model orqali olish
    all_questions = quiz.subject.questions.filter(is_active=True)

    # Barcha savollar sonini hisoblash
    total_questions_count = all_questions.count()

    # Agar berilgan savollar soni barcha mavjud savollar sonidan katta bo'lsa,
    # barcha savollarni olib beramiz
    if num_questions >= total_questions_count:
        return all_questions.order_by('?')

    # Barcha savollar ID larini olish
    all_question_ids = list(all_questions.values_list('id', flat=True))

    # Boshlang'ich ro'yxatdan tasodifiy tartibda num_questions ta savolni tanlash
    selected_question_ids = random.sample(all_question_ids, num_questions)

    # Tanlangan savollar ro'yxatini olish
    selected_questions = all_questions.filter(id__in=selected_question_ids)

    return selected_questions.order_by('?')

#######

def student_home(request):

    if request.method == "POST":
        data = request.POST

        grade_id = int(data['grade_id'])
        group_id = int(data['group_id'])
        student_id = int(data['student_id'])

        try:
            grade = Grade.objects.get(id=grade_id)
            group = Group.objects.get(id=group_id)
            student = Student.objects.get(id=student_id)

            if group.grade == grade and student.group == group:
                print(True)
                request.session['grade_id'] = grade_id
                request.session['group_id'] = group_id
                request.session['student_id'] = student_id

                return redirect('quiz_room')
            else:
                messages.error(request, "Ma'lumot kiritishda xatolik!")
        except:
            messages.error(request, "Ma'lumot kiritishda xatolik!")

    grades = Grade.objects.all()
    groups = Group.objects.all()
    students = Student.objects.all()

    ctx = {
        'grades': grades,
        'groups': groups,
        'students': students,
    }
    return render(request, 'student/home.html', ctx)


def quiz_room(request):
    grade_id = request.session.get('grade_id')
    group_id = request.session.get('group_id')
    student_id = request.session.get('student_id')

    student_data = []

    if grade_id and group_id and student_id:
        try:
            group = Group.objects.get(id=group_id)
            grade = Grade.objects.get(id=grade_id)
            student = Student.objects.get(id=student_id)

            current_time = timezone.now()
            student_quizes = Quiz.objects.filter(groups=group, status=True, end_time__gt=current_time)

            for q in student_quizes:
                if q.start_time <= current_time and q.end_time >= current_time:
                    results = Result.objects.filter(quiz=q, student=student)
                    print(results)
                    if len(results) == 0:
                        student_data.append({
                            'quiz': q,
                            'status': 'start'
                        })
                    elif len(results) == q.maximum_attempts:
                        old_result = results.first()
                        if old_result.status == False:
                            student_data.append({
                                'quiz': q,
                                'status': 'davom_ettir',
                                'old_result': old_result
                            })
                        else:
                            student_data.append({
                                'quiz': q,
                                'status': 'urinish_tugadi',
                                'old_result': old_result
                            })
                    elif len(results) < q.maximum_attempts:
                        old_result = results.first()
                        if old_result.status == False:
                            student_data.append({
                                'quiz': q,
                                'status': 'davom_ettir',
                                'old_result': old_result
                            })
                        else:
                            student_data.append({
                                'quiz': q,
                                'status': 'qayta_boshla',
                                'old_result': old_result
                            })

            ctx = {
                'student_quizes': student_quizes,

                'grade': grade,
                'group': group,
                'student': student,

                'now': timezone.now(),
                'student_data': student_data,
            }

            return render(request, 'student/test_room.html', ctx)
        except:
            print(True)
            return redirect('student_home')
    else:
        return redirect('student_home')


def quiz_start(request, quiz_id):
    grade_id = request.session.get('grade_id')
    group_id = request.session.get('group_id')
    student_id = request.session.get('student_id')

    if grade_id and group_id and student_id:
        # try:
        student = Student.objects.get(id=student_id)
        quiz = get_object_or_404(Quiz, pk=quiz_id)

        current_time = timezone.now()

        if student in quiz.no_permission_students.all():
            messages.error(request, "Xatolik! Sizga ruhsat berilmagan!")
            return redirect('quiz_room')
        else:
            if quiz.start_time <= current_time and quiz.end_time >= current_time:
                results = Result.objects.filter(quiz=quiz, student=student)
                if len(results) == 0:
                    random_quizes = get_random_questions(quiz, quiz.max_questions)
                    result = Result.objects.create(
                        quiz=quiz,
                        student=student,
                        score=0,
                    )

                    user_answers = []
                    for i in random_quizes:
                        user_answer = UserAskedAnswer.objects.create(
                            quiz=quiz,
                            user=student,
                            question=i
                        )
                        user_answers.append(user_answer)

                    result.random_quizes.set(random_quizes)
                    result.answers.set(user_answers)

                    ctx = {
                        'result': result
                    }

                    return render(request, 'student/quizes.html', ctx)
                elif len(results) == quiz.maximum_attempts:
                    old_result = results.first()
                    if old_result.status == False:
                        ctx = {
                            'result': old_result
                        }

                        return render(request, 'student/quizes.html', ctx)
                    else:
                        ctx = {
                            'result': old_result
                        }

                        return render(request, 'student/quizes.html', ctx)
                elif len(results) < quiz.maximum_attempts:
                    print('Asliddin +++++++++++++++++++')
                    old_result = results.first()

                    if old_result.status == False:
                        ctx = {
                            'result': old_result
                        }

                        return render(request, 'student/quizes.html', ctx)
                    else:
                        random_quizes = get_random_questions(quiz, quiz.max_questions)
                        result = Result.objects.create(
                            quiz=quiz,
                            student=student,
                            score=0,
                        )

                        user_answers = []
                        for i in random_quizes:
                            user_answer = UserAskedAnswer.objects.create(
                                quiz=quiz,
                                user=student,
                                question=i
                            )
                            user_answers.append(user_answer)

                        result.random_quizes.set(random_quizes)
                        result.answers.set(user_answers)
                        ctx = {
                            'result': result
                        }

                        return render(request, 'student/quizes.html', ctx)
                else:
                    old_result = results.first()

                    if old_result.status == False:
                        old_result.status = True
                        old_result.save()
                        messages.error(request, "Sizning urinishlaringiz tugadi!")
                        return redirect('quiz_room')
            else:
                messages.error(request, "Xatolik! Test vaqti tugagan!")
                return redirect('quiz_room')

        # except:
        #     messages.error(request, "Xatolik! Ma'lumotlar mos kelmadi!")
        #     return redirect('quiz_room')
    else:
        messages.error(request, "Noma'lum talaba!")
        return redirect('student_home')

def quiz_end(request, quiz_id):
    grade_id = request.session.get('grade_id')
    group_id = request.session.get('group_id')
    student_id = request.session.get('student_id')

    if grade_id and group_id and student_id:
        student = Student.objects.get(id=student_id)
        quiz = get_object_or_404(Quiz, pk=quiz_id)

        current_time = timezone.now()

        if quiz.start_time <= current_time and quiz.end_time >= current_time:
            results = Result.objects.filter(quiz=quiz, student=student)

            old_result = results.first()
            if old_result.status == False:
                max_ball = 100 / old_result.quiz.max_questions
                print(max_ball)
                k = 0
                for i in old_result.answers.all():
                    print(i)
                    if i.chosen_answer:
                        if i.chosen_answer.is_correct:
                            k += max_ball
                old_result.score = k

                old_result.end_time = timezone.now()
                old_result.status = True
                old_result.save()
                messages.success(request, f"Sizning natijangiz: {k} ball!")

            return redirect('quiz_room')
        else:
            messages.error(request, "Xatolik! Test vaqti tugagan!")
            return redirect('quiz_room')
    else:
        messages.error(request, "Noma'lum talaba!")
        return redirect('student_home')

def quizes(request, quiz_id):
    grade_id = request.session.get('grade_id')
    group_id = request.session.get('group_id')
    student_id = request.session.get('student_id')

    student_data = []

    if grade_id and group_id and student_id:
        try:
            group = Group.objects.get(id=group_id)
            grade = Grade.objects.get(id=grade_id)
            student = Student.objects.get(id=student_id)

            current_time = timezone.now()
            q = get_object_or_404(Quiz, pk=quiz_id)

            if q.start_time <= current_time and q.end_time >= current_time:
                results = Result.objects.filter(quiz=q, student=student)
                if len(results) == 0:
                    print(1)
                if len(results) == q.maximum_attempts:
                    old_result = results.first()
                    if old_result.status == False:
                        student_data.append({
                            'quiz': q,
                            'status': 'davom_ettir'
                        })
                    else:
                        student_data.append({
                            'quiz': q,
                            'status': 'urinish_tugadi'
                        })
                elif len(results) < q.maximum_attempts:
                    old_result = results.first()
                    if old_result.status == False:
                        student_data.append({
                            'quiz': q,
                            'status': 'davom_ettir'
                        })
                    else:
                        student_data.append({
                            'quiz': q,
                            'status': 'qayta_boshla'
                        })

            ctx = {
                'grade': grade,
                'group': group,
                'student': student,

                'now': timezone.now(),
                'student_data': student_data,
                'result': old_result,
            }

            return render(request, 'student/quizes.html', ctx)
        except:
            return redirect('student_home')
    else:
        return redirect('student_home')


def student_results(request):
    grade_id = request.session.get('grade_id')
    group_id = request.session.get('group_id')
    student_id = request.session.get('student_id')

    if grade_id and group_id and student_id:
        try:
            group = Group.objects.get(id=group_id)
            grade = Grade.objects.get(id=grade_id)
            student = Student.objects.get(id=student_id)

            # results = Result.objects.filter(student=student)
            results = []
            quiz_all = Quiz.objects.all()
            for quiz in quiz_all:
                quiz_results = Result.objects.filter(quiz=quiz, student=student)
                if len(quiz_results) > 0:
                    results.append(quiz_results.first())
            print(results)

            ctx = {
                'grade': grade,
                'group': group,
                'student': student,

                'results': results,
            }

            return render(request, 'student/student_results.html', ctx)
        except:
            return redirect('student_home')
    else:
        return redirect('student_home')
# Responses ++++++++++++
def get_groups(request, grade_id):
    # Retrieve groups based on the selected grade
    groups = Group.objects.filter(grade_id=grade_id).values('id', 'group_name')

    # Convert queryset to list of dictionaries
    groups_list = list(groups)

    # Return JSON response
    return JsonResponse(groups_list, safe=False)

def get_students(request, group_id):
    students = Student.objects.filter(group_id=group_id).values('id', 'name')
    students_list = list(students)
    return JsonResponse(students_list, safe=False)

# ========================== ++++ ============================
def question_check_by_id(request, question_id, answer_id):
    instance = get_object_or_404(UserAskedAnswer, pk=int(question_id))
    chosen_answer = get_object_or_404(Answer, pk=int(answer_id))

    print(instance)
    print(chosen_answer)

    instance.chosen_answer = chosen_answer
    instance.save()

    return JsonResponse({'status': True})