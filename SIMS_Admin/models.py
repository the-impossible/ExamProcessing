
from django.db import models

# My app imports
from SIMS_Authentication.models import Accounts

# Create your models here.
class StudentClass(models.Model):
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10, help_text='Eg- A,B,C etc')
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Student Class'
        db_table = 'Student Class'

    def __str__(self):
        return f'{self.class_name} {self.section}'

class StudentRoles(models.Model):
    role = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Student Roles'
        db_table = 'Student Roles'

    def __str__(self):
        return self.role

class StaffRoles(models.Model):
    role = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Staff Roles'
        db_table = 'Staff Roles'

    def __str__(self):
        return self.role

class Student(models.Model):
    select_gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    student_acct = models.OneToOneField(to=Accounts, on_delete=models.CASCADE, blank=True, null=True, related_name="student_acct")
    student_class = models.ForeignKey(to=StudentClass, on_delete=models.CASCADE, blank=True, null=True)
    student_role = models.ForeignKey(to=StudentRoles, on_delete=models.CASCADE, blank=True, null=True)
    student_gender = models.CharField(max_length=8, choices=select_gender, blank=True, null=True)
    student_date_of_birth = models.DateField(blank=True, null=True)

    class Meta():
        verbose_name_plural = 'Students'

    def __str__(self):
        return f'{self.student_acct}'

class Staff(models.Model):
    select_gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    staff_acct = models.OneToOneField(to=Accounts, on_delete=models.CASCADE, blank=True, null=True)
    staff_phone = models.CharField(max_length=14, unique=True, db_index=True)
    staff_gender = models.CharField(max_length=8, choices=select_gender, blank=True, null=True)
    staff_class = models.ForeignKey(to=StudentClass, on_delete=models.CASCADE, null=True)
    staff_role = models.ForeignKey(to=StaffRoles, on_delete=models.CASCADE, blank=True, null=True)
    staff_date_of_birth = models.DateField(blank=True, null=True)

    class Meta():
        verbose_name_plural = 'Staffs'

    def __str__(self):
        return f'{self.staff_acct}'

class Admins(models.Model):
    select_gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    admin_acct = models.OneToOneField(to=Accounts, on_delete=models.CASCADE, blank=True, null=True)
    admin_phone = models.CharField(max_length=14, unique=True, db_index=True)
    admin_gender = models.CharField(max_length=8, choices=select_gender, blank=True, null=True)
    admin_date_of_birth = models.DateField(blank=True, null=True)

    class Meta():
        verbose_name_plural = 'Admins'

    def __str__(self):
        return f'{self.admin_acct}'

class Subjects(models.Model):
    subject_title = models.CharField(max_length=30, unique=True, db_index=True)
    subject_code = models.CharField(max_length=14, unique=True, db_index=True)
    subject_creation_date = models.DateTimeField(auto_now_add=True)

    class Meta():
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.subject_title

class SubjectCombination(models.Model):
    select_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    select_subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    combination_desc = models.CharField(max_length=100, unique=True, blank=True, null=True)

    class Meta():
        verbose_name_plural = 'Subject Combination'

    def __str__(self):
        return f'{self.select_class} {self.select_subject}'

class StudentGrades(models.Model):
    student_ca1 = models.IntegerField()
    student_ca2 = models.IntegerField()
    student_ca3 = models.IntegerField()
    student_exam = models.IntegerField()
    student_total = models.IntegerField()
    select_student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    select_subject = models.ForeignKey(SubjectCombination, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.CharField(max_length=100, unique=True, blank=True, null=True)

    class Meta():
        verbose_name_plural = 'Student Grades'

    def __str__(self):
        return f'{self.select_student} Scored  {self.student_total} in {self.select_subject}'

class StaffClassCombination(models.Model):
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, blank=True, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True, null=True)
    combination_desc = models.CharField(max_length=100, unique=True, blank=True, null=True)

    class Meta():
        verbose_name_plural = 'Staff Assigned Class'

    def __str__(self):
        return f'{self.staff} is assigned to: {self.student_class}'
