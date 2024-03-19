from django.urls import path

from .views import *

urlpatterns = [
    # Home
    path('', dashboard_home, name='dashboard_home'),

    # Auth
    path('auth/login/', login_page, name='login_page'),
    path('auth/logout/', logout_page, name='logout_page'),
    path('auth/change-password/', change_password, name='change_password'),


    # Student grades
    path('student/grades/', grade_list, name='grade_list'),
    path('student/grades/create/', grade_create, name='grade_create'),
    path('student/grades/<int:pk>/edit/', grade_edit, name='grade_edit'),
    path('student/grades/<int:pk>/delete/', grade_delete, name='grade_delete'),
    path('student/grades/checked/delete/', grade_checked_delete, name='grade_checked_delete'),

    # Student groups
    path('student/groups/', group_list, name='group_list'),
    path('student/grade-groups/<int:pk>/', group_list_by_grade_id, name='group_list_by_grade_id'),
    path('student/groups/create/', group_create, name='group_create'),
    path('student/groups/<int:pk>/edit/', group_edit, name='group_edit'),
    path('student/groups/<int:pk>/delete/', group_delete, name='group_delete'),
    path('student/groups/checked/delete/', group_checked_delete, name='group_checked_delete'),

    # Student students
    path('student/students/', student_list, name='student_list'),
    path('student/group-students/<int:pk>/', student_list_by_group_id, name='student_list_by_group_id'), # new
    path('student/group-type-students/<int:pk>/', student_list_by_group_type, name='student_list_by_group_type'), # new
    path('student/students/create/', student_create, name='student_create'),
    path('student/students/create-excel/', student_excel_create, name='student_excel_create'),
    path('student/students/<int:pk>/edit/', student_edit, name='student_edit'),
    path('student/students/<int:pk>/delete/', student_delete, name='student_delete'),
    path('student/students/checked/delete/', student_checked_delete, name='student_checked_delete'),

    # Quiz =======================
    # Subject
    path('quiz/subjects/', subject_list, name='subject_list'),
    path('quiz/grade-subjects/<int:pk>/', subject_list_by_grade_id, name='subject_list_by_grade_id'),
    path('quiz/subjects/create/', subject_create, name='subject_create'),
    path('quiz/subjects/<int:pk>/edit/', subject_edit, name='subject_edit'),
    path('quiz/subjects/<int:pk>/delete/', subject_delete, name='subject_delete'),
    path('quiz/subjects/checked/delete/', subject_checked_delete, name='subject_checked_delete'),
    path('quiz/subjects/<int:subject_id>/add-questions/', subject_add_question, name='subject_add_question'),
    path('quiz/subjects/edit-question/<int:question_id>/', subject_question_answer_is_active, name='subject_question_answer_is_active'),
    path('quiz/subjects/question/edit/<int:question_id>/', subject_question_detail, name='subject_question_detail'),

    # Quiz types
    path('quiz/quiz-types/', quiz_type_list, name='quiz_type_list'),
    path('quiz/quiz-types/create/', quiz_type_create, name='quiz_type_create'),
    path('quiz/quiz-types/<int:pk>/edit/', quiz_type_edit, name='quiz_type_edit'),
    path('quiz/quiz-types/<int:pk>/delete/', quiz_type_delete, name='quiz_type_delete'),
    path('quiz/quiz-types/checked/delete/', quiz_type_checked_delete, name='quiz_type_checked_delete'),

    # Quiz ++++++
    path('quiz/quiz/', quiz_list, name='quiz_list'),
    path('quiz/quiz/create/', quiz_create, name='quiz_create'),
    path('quiz/quiz/<int:pk>/edit/', quiz_edit, name='quiz_edit'),
    path('quiz/quiz/<int:pk>/delete/', quiz_delete, name='quiz_delete'),
    path('quiz/quiz/checked/delete/', quiz_checked_delete, name='quiz_checked_delete'),
    path('quiz/quiz/<int:quiz_id>/quiz-active/', quiz_is_active, name='quiz_is_active'),

    # Result ++++++
    path('quiz/result/', result_list, name='result_list'),
    path('quiz/result-quiz/<int:pk>/', result_list_by_quiz_id, name='result_list_by_quiz_id'),
    path('quiz/result/create/', result_create, name='result_create'),
    path('quiz/result/<int:pk>/edit/', result_edit, name='result_edit'),
    path('quiz/result/<int:pk>/delete/', result_delete, name='result_delete'),
    path('quiz/result/checked/delete/', result_checked_delete, name='result_checked_delete'),

    path('quiz/result/excel-create/<int:pk>/', excel_create_results_by_quiz_id, name='excel_create_results_by_quiz_id'),
]