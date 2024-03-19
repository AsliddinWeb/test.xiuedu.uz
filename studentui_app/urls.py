from django.urls import path

from .views import (student_home, get_groups, get_students, quiz_room, quiz_start, quizes,
                    question_check_by_id, quiz_end, student_results
                    )

urlpatterns = [
    path('', student_home, name='student_home'),
    path('room/', quiz_room, name='quiz_room'),
    path('room/<int:quiz_id>/start/', quiz_start, name='quiz_start'),
    path('room/<int:quiz_id>/end/', quiz_end, name='quiz_end'),
    path('room/<int:quiz_id>/', quizes, name='quizes'),

    path('room/my-results/', student_results, name='student_results'),

    # Responses
    path('get/groups/<int:grade_id>/', get_groups, name='get_groups'),
    path('get/students/<int:group_id>/', get_students, name='get_students'),
    path('answer/<int:question_id>/<int:answer_id>/', question_check_by_id, name='question_check_by_id')

]