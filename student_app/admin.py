from django.contrib import admin

from .models import *

admin.site.register(Grade)

admin.site.register(TypeGroup)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'grade')
admin.site.register(Group, GroupAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
admin.site.register(Student, StudentAdmin)