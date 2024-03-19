from django.db import models

class Grade(models.Model):
    grade = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.grade}"
    class Meta:
        ordering = ['-id']

class TypeGroup(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type}"

class Group(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='groups')
    type_group = models.ForeignKey(TypeGroup, on_delete=models.CASCADE, related_name='groups')
    group_name = models.CharField(max_length=455)

    def __str__(self):
        return self.group_name
    class Meta:
        ordering = ['-id']

class Student(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=455)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-id']
