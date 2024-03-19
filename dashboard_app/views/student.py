from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

# Excel
import pandas as pd

from student_app.models import Grade, Group, Student, TypeGroup
from ..forms import GradeForm, GroupForm, StudentForm, StudentCreateExcelForm

# Grade
@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def grade_list(request):
    grades = Grade.objects.all()

    ctx = {

        # Main
        'grades': grades,
    }

    return render(request, 'dashboard/student/grade_list.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def grade_create(request):
    form = GradeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{form.cleaned_data['grade']}</b> muvaffaqqiyatli qo'shildi!")
            return redirect('grade_list')

    ctx = {

        # Main
        'form': form,
    }

    return render(request, 'dashboard/student/grade_create.html', ctx)


@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def grade_edit(request, pk):
    instance = get_object_or_404(Grade, pk=pk)
    form = GradeForm(instance=instance)

    if request.method == "POST":
        form = GradeForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{form.cleaned_data['grade']}</b> muvaffaqqiyatli o'zgartirildi!")
            return redirect('grade_list')

    ctx = {
        # Main
        'form': form,

        'instance': instance,
    }

    return render(request, 'dashboard/student/grade_edit.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)

def grade_delete(request, pk):
    instance = get_object_or_404(Grade, pk=pk)
    messages.success(request, f"<b>{instance.grade}</b> muvaffaqqiyatli o'chirildi!")
    instance.delete()

    return redirect('grade_list')

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def grade_checked_delete(request):
    if request.method == 'POST':
        grade_ids = request.POST.getlist('grade_ids')
        Grade.objects.filter(id__in=grade_ids).delete()

        messages.success(request, f"Tanlanganlar muvaffaqqiyatli o'chirildi!")
        return redirect('grade_list')

# Group
@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def group_list(request):
    groups = Group.objects.all()
    grades = Grade.objects.all().order_by('id')

    ctx = {

        # Main
        'groups': groups,
        'grades': grades,
        'grade_all': True,
    }

    return render(request, 'dashboard/student/group_list.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def group_list_by_grade_id(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    groups = grade.groups.all()
    grades = Grade.objects.all().order_by('id')

    ctx = {

        # Main
        'groups': groups,
        'grades': grades,
        'pk': pk,
        'grade_all': False,
    }

    return render(request, 'dashboard/student/group_list.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def group_create(request):
    form = GroupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{form.cleaned_data['group_name']}</b> muvaffaqqiyatli qo'shildi!")
            return redirect('group_list')

    ctx = {

        # Main
        'form': form,
    }

    return render(request, 'dashboard/student/group_create.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def group_edit(request, pk):
    instance = get_object_or_404(Group, pk=pk)
    form = GroupForm(instance=instance)

    if request.method == "POST":
        form = GroupForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{form.cleaned_data['group_name']}</b> muvaffaqqiyatli o'zgartirildi!")
            return redirect('group_list')

    ctx = {
        # Main
        'form': form,

        'instance': instance,
    }

    return render(request, 'dashboard/student/group_edit.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def group_delete(request, pk):
    instance = get_object_or_404(Group, pk=pk)
    messages.success(request, f"<b>{instance.group_name}</b> muvaffaqqiyatli o'chirildi!")
    instance.delete()

    return redirect('group_list')

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def group_checked_delete(request):
    if request.method == 'POST':
        group_ids = request.POST.getlist('group_ids')
        Group.objects.filter(id__in=group_ids).delete()

        messages.success(request, f"Tanlanganlar muvaffaqqiyatli o'chirildi!")
        return redirect('group_list')

# Student
@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def student_list(request):
    students = Student.objects.all()
    groups = Group.objects.all()
    group_types = TypeGroup.objects.all()

    ctx = {

        # Main
        'students': students,
        'groups': groups,
        'group_types': group_types,
        'h1_text': 'Barcha talabalar ro\'yhati',

        'group_all': True,
        'group_type_all': True
    }

    return render(request, 'dashboard/student/student_list.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def student_list_by_group_id(request, pk):
    group = get_object_or_404(Group, pk=pk)

    students = group.students.all()
    groups = Group.objects.all()
    group_types = TypeGroup.objects.all()

    ctx = {

        # Main
        'students': students,
        'groups': groups,
        'group_types': group_types,
        'pk': pk,
        'h1_text': f"<span class='text-info'>{group.group_name}</span> guruh talabalari",

        'group_all': False,
        'group_type_all': True
    }

    return render(request, 'dashboard/student/student_list.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def student_list_by_group_type(request, pk):
    group_type = get_object_or_404(TypeGroup, pk=pk)
    groups = group_type.groups.all()
    group_types = TypeGroup.objects.all()

    # Get all group IDs for the given group type
    group_ids = groups.values_list('id', flat=True)

    # Filter students based on the group IDs
    students = Student.objects.filter(group__id__in=group_ids)

    ctx = {

        # Main
        'students': students,
        'groups': groups,
        'group_types': group_types,
        'pk': pk,
        'h1_text': f"<span class='text-info'>{group_type.type}</span> talabalar",

        'group_all': True,
        'group_type_all': False
    }

    return render(request, 'dashboard/student/student_list.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def student_create(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{form.cleaned_data['name']}</b> muvaffaqqiyatli qo'shildi!")
            return redirect('student_list')

    ctx = {

        # Main
        'form': form,
    }

    return render(request, 'dashboard/student/student_create.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def student_edit(request, pk):
    instance = get_object_or_404(Student, pk=pk)
    form = StudentForm(instance=instance)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{form.cleaned_data['name']}</b> muvaffaqqiyatli o'zgartirildi!")
            return redirect('student_list')

    ctx = {
        # Main
        'form': form,

        'instance': instance,
    }

    return render(request, 'dashboard/student/student_edit.html', ctx)

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def student_delete(request, pk):
    instance = get_object_or_404(Student, pk=pk)
    messages.success(request, f"<b>{instance.name}</b> muvaffaqqiyatli o'chirildi!")
    instance.delete()

    return redirect('student_list')

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def student_checked_delete(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids')
        Student.objects.filter(id__in=student_ids).delete()

        messages.success(request, f"Tanlanganlar muvaffaqqiyatli o'chirildi!")
        return redirect('student_list')

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def student_excel_create(request):
    form = StudentCreateExcelForm()
    if request.method == "POST":
        form = StudentCreateExcelForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['excel']
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                k = 0
                for index, row in df.iterrows():
                    group_name = row["Guruh"]
                    student_name = row["To‘liq ismi"]
                    type_group = row["Ta’lim shakli"]
                    grade = row["Kurs"]

                    # Grade
                    grade_obj, created = Grade.objects.get_or_create(grade=grade)

                    # TypeGroup
                    type_group_obj, created = TypeGroup.objects.get_or_create(type=type_group)

                    # Group
                    group_obj, created = Group.objects.get_or_create(
                        grade=grade_obj,
                        type_group=type_group_obj,
                        group_name=group_name
                    )

                    # Student
                    if Student.objects.filter(name=student_name).exists():
                        print(student_name)
                    else:
                        student_obj = Student.objects.create(
                            group=group_obj,
                            name=student_name
                        )
                        k += 1
                messages.success(request, f"<b>{k} ta Talabalar</b> muvaffaqqiyatli qo'shildi!")
                return redirect('student_list')
            else:
                messages.error(request, "Fayl turi <b>.xlsx</b> bo'lishi zarur!")
        else:
            messages.error(request, "Xatolik!")

    ctx = {

        # Main
        'form': form,
    }

    return render(request, 'dashboard/student/student_add_excel.html', ctx)

