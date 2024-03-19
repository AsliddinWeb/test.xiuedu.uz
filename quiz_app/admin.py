from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field

from django.contrib import admin

from .models import *

admin.site.register(Subject)

class AnswerInline(admin.TabularInline):
    model = Answer
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('text', 'subject')
admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
admin.site.register(Answer, AnswerAdmin)

admin.site.register(QuizType)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'deadline', 'max_questions', 'subject',
                    'maximum_attempts', 'status')
    filter_vertical = ('groups', 'no_permission_students')
admin.site.register(Quiz, QuizAdmin)

class UserAskedAnswerAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'question', 'chosen_answer')
admin.site.register(UserAskedAnswer, UserAskedAnswerAdmin)

class ResultResource(resources.ModelResource):
    student_name = Field(attribute='student__name', column_name='Talaba')
    quiz_title = Field(attribute='quiz__title', column_name='Imtihon')
    score = Field(attribute='score', column_name='Ball')
    end_time = Field(attribute='end_time', column_name='Tugatgan vaqti')

    class Meta:
        model = Result
        fields = ('student_name', 'quiz_title', 'score', 'end_time')
        export_order = ('student_name', 'quiz_title', 'score', 'end_time')


class ResultAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'start_time', 'end_time')
    list_filter = ['quiz']
    resource_class = ResultResource

admin.site.register(Result, ResultAdmin)
