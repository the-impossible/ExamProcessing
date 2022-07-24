from django.contrib import admin

# My App imports
from SIMS_Admin.models import (
    StudentClass,
    StudentRoles,
    StaffRoles,
    Student,
    Staff,
    Subjects,
    SubjectCombination,
    StaffClassCombination,
    StudentGrades,
    Admins
)

# Register your models here.
admin.site.register(StudentClass)
admin.site.register(StudentRoles)
admin.site.register(StaffRoles)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Subjects)
admin.site.register(SubjectCombination)
admin.site.register(StaffClassCombination)
admin.site.register(StudentGrades)
admin.site.register(Admins)