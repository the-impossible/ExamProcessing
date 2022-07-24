from django.http.response import FileResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

# My app imports
from SIMS_Authentication.forms import AccountRegistrationForm
from SIMS_Admin.forms import StudentForm, SubjectForm, SubjectCombinationForm, ClassForm, AccountEditForm, StudentEditForm, AccountPictureForm, StaffForm, StaffClassCombinationForm, StudentGradesForm, AdminForm, StaffEditForm, StudentEditAdminForm, StaffEditAdminForm
from SIMS_Authentication.views import generate_schno
from SIMS_Admin.models import StudentClass, Student, Staff, StaffClassCombination, SubjectCombination, Subjects, StudentGrades, StudentRoles, Admins
from SIMS_Authentication.models import Accounts
from SIMS_Admin.decorator import is_admin, is_staff

# PDF
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.conf import settings
import os

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            students = Student.objects.all().order_by('-id').count()
            staffs = Accounts.objects.filter(is_staff=True, is_superuser=False).order_by('-id').count()
            subjects = Subjects.objects.all().order_by('-id').count()
            classes = StudentClass.objects.all().order_by('-id').count()
            grades = StudentGrades.objects.all().order_by('-id').count()
            roles = StudentRoles.objects.all().order_by('-id').count()
            assigned_classes = StaffClassCombination.objects.all().order_by('-id').count()
            context = {
                'students':students,
                'staffs':staffs,
                'subjects':subjects,
                'classes':classes,
                'grades':grades,
                'roles':roles,
                'assigned_classes':assigned_classes,
            }
        elif not request.user.is_superuser and request.user.is_staff:
            students = Student.objects.all().order_by('-id').count()
            subjects = Subjects.objects.all().order_by('-id').count()
            classes = StudentClass.objects.all().order_by('-id').count()
            staff_assigned_classes = StaffClassCombination.objects.filter(staff_id=request.user.staff.id).order_by('-id').count()
            roles = StudentRoles.objects.all().order_by('-id').count()
            context = {
                'students':students,
                'subjects':subjects,
                'classes':classes,
                'roles':roles,
                'staff_assigned_classes':staff_assigned_classes,
            }
        else:
            students = Student.objects.all().order_by('-id').count()
            cmate = Student.objects.filter(student_class=request.user.student_acct.student_class).order_by('-id').count()
            subjects = Subjects.objects.all().order_by('-id').count()
            roles = StudentRoles.objects.all().order_by('-id').count()
            roles = StudentRoles.objects.all().order_by('-id').count()
            context = {
                'subjects':subjects,
                'students':students,
                'roles':roles,
                'cmate':cmate,
            }
        return render(request, 'admin/dashboard.html', context)

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        try:
            user_acct = Accounts.objects.get(id=user_id)
            if user_acct.is_staff and user_acct.is_superuser:
                admin = Admins.objects.get(admin_acct=user_acct.id)
                context = {
                    'user':user_acct,
                    'form':AccountEditForm(instance=user_acct),
                    'form2':AccountPictureForm(instance=user_acct),
                    'form1':AdminForm(instance=admin),
                    'mode':'admin',
                    'admin':admin,
                }
            elif user_acct.is_staff:
                staff = Staff.objects.get(staff_acct =user_acct.id)
                context = {
                    'user':user_acct,
                    'form':AccountEditForm(instance=user_acct),
                    'form2':AccountPictureForm(instance=user_acct),
                    'form1':StaffEditAdminForm(initial={'staff_role':staff.staff_role, 'staff_class':staff.staff_class},instance=staff),
                    'mode':'staff',
                    'staff':staff,
                }
            else:
                student = Student.objects.get(student_acct_id=user_acct.id)
                context = {
                    'user':user_acct,
                    'form':AccountEditForm(instance=user_acct),
                    'form2':AccountPictureForm(instance=user_acct),
                    'form1':StudentEditAdminForm(initial={'student_class':student.student_class, 'student_role':student.student_role}, instance=student),
                    'mode':'student',
                    'student':student,
                }
        except ObjectDoesNotExist:
            messages.error(request, ('User account not found'))
            return redirect('sims_admin:dashboard')
        else:
            return render(request, 'admin/profile.html', context)

    def post(self, request, user_id):
        if 'picture' in request.POST:
            user_acct = Accounts.objects.get(id=user_id)
            form = AccountPictureForm(request.POST, request.FILES, instance=user_acct)
            if form.is_valid():
                form.save()
                messages.success(request, ('Profile Picture Updated successful'))
            else:
                messages.error(request, ('Error Processing Profile Upload!'))

        if 'info' in request.POST:
            user_acct = Accounts.objects.get(id=user_id)
            if user_acct.is_staff and user_acct.is_superuser:
                admin = Admins.objects.get(admin_acct=user_acct.id)
                form = AccountEditForm(data=request.POST, instance=user_acct)
                form1 = AdminForm(data=request.POST, instance=admin)

                if form.is_valid() and form1.is_valid():
                    form.save()
                    form1.save()
                    messages.success(request, ('Profile Info Updated successfully'))
                else:
                    messages.error(request, ('Error processing profile information!'))
                    form2 = AccountPictureForm(instance=user_acct),
                    return render(request, 'admin/profile.html', {'form':form, 'form1':form1, 'form2':form2, 'mode':'admin', 'admin': admin})
            elif user_acct.is_staff:
                staff = Staff.objects.get(staff_acct=user_acct.id)
                form = AccountEditForm(data=request.POST, instance=user_acct)
                if not request.user.is_superuser:
                    form1 = StaffEditForm(data=request.POST, instance=staff)
                else:
                    form1 = StaffEditAdminForm(initial={'staff_role':staff.staff_role, 'staff_class':staff.staff_class}, data=request.POST, instance=staff)

                if form.is_valid() and form1.is_valid():
                    form.save()
                    form1.save()
                    messages.success(request, ('Profile Info Updated successfully'))
                else:
                    messages.error(request, ('Error processing profile information!'))
                    form2 = AccountPictureForm(instance=user_acct),
                    return render(request, 'admin/profile.html', {'form':form, 'form1':form1, 'form2':form2, 'mode':'staff', 'staff': staff})
            else:
                student = Student.objects.get(student_acct_id=user_acct.id)
                form = AccountEditForm(data=request.POST, instance=user_acct)
                if not request.user.is_superuser:
                    form1 = StudentEditForm(data=request.POST, instance=student, initial={'student_class':student.student_class, 'student_role':student.student_role},)
                else:
                    form1 = StudentEditAdminForm(data=request.POST, instance=student, initial={'student_class':student.student_class, 'student_role':student.student_role},)

                if form.is_valid() and form1.is_valid():
                    form.save()
                    if not request.user.is_superuser:
                        stud = form1.save(commit=False)
                        stud.student_role = student.student_role
                        stud.student_class = student.student_class
                        stud.save()
                    form1.save()
                    messages.success(request, ('Profile Info Updated successful'))
                else:
                    messages.error(request, ('Error processing profile information!'))
                    form2 = AccountPictureForm(instance=user_acct),
                    return render(request, 'admin/profile.html', {'form':form, 'form1':form1, 'form2':form2, 'mode':'student', 'student':student})
        return redirect('sims_admin:profile', user_id)

class AddStudentView(LoginRequiredMixin, View):
    @method_decorator(is_admin)
    def get(self, request):
        context = {
            'form':AccountRegistrationForm(),
            'form1':StudentForm()
        }
        return render(request, 'admin/add_student.html', context)

    @method_decorator(is_admin)
    def post(self, request):
        form = AccountRegistrationForm(request.POST)
        form1 = StudentForm(request.POST)
        if form.is_valid() and form1.is_valid():
            user = form.save(commit=False)
            user_profile = form1.save(commit=False)

            user.schNo = str(generate_schno())
            user.set_password(user.password)
            user_profile.student_acct = user

            user.save()
            user_profile.save()
            messages.success(request, ('Account creation successful'))
            return redirect('sims_admin:add_student')

        return render(request, 'admin/add_student.html', {'form':form, 'form1':form1})

class AddSubjectView(LoginRequiredMixin, View):
    @method_decorator(is_admin)
    def get(self, request):
        context = {'form':SubjectForm()}
        return render(request, 'admin/add_subject.html', context)

    @method_decorator(is_admin)
    def post(self, request):
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.subject_code = str(subject.subject_code).upper()
            subject.save()
            messages.success(request, (f'Subject {subject.subject_title} has been created'))
            return redirect('sims_admin:add_subject')

        return render(request, 'admin/add_subject.html', {'form':form})

class AssingSubjectView(LoginRequiredMixin, View):
    @method_decorator(is_admin)
    def get(self, request):
        context = {'form':SubjectCombinationForm()}
        return render(request, 'admin/subject_class.html', context)

    @method_decorator(is_admin)
    def post(self, request):
        form = SubjectCombinationForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.combination_desc = f'{info.select_subject} {info.select_class}'
            try:
                info.save()
                messages.success(request, (f'Subject: {info.select_subject} has been linked with Class: {info.select_class}'))
                return redirect('sims_admin:assign_subject')
            except IntegrityError:
                messages.error(request, (f'Subject has already been linked with class'))
        return render(request, 'admin/subject_class.html', {'form':form})

class AssignClassView(LoginRequiredMixin, View):
    @method_decorator(is_admin)
    def get(self, request):
        context = {'form':StaffClassCombinationForm()}
        return render(request, 'admin/staff_class.html', context)

    @method_decorator(is_admin)
    def post(self, request):
        form = StaffClassCombinationForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            try:
                StaffClassCombination.objects.get(combination_desc__endswith=f'{info.student_class}')
            except ObjectDoesNotExist:
                info.combination_desc = f'{info.staff} {info.student_class}'
                info.save()
                messages.success(request, (f'Staff: {info.staff} has been linked with Class: {info.student_class}'))
                return redirect('sims_admin:assign_class')
            else:
                messages.error(request, (f'Another Staff is linked with the class'))
        return render(request, 'admin/staff_class.html', {'form':form})

class CreateEditDeleteClassView(LoginRequiredMixin, View):
    @method_decorator(is_admin)
    def get(self, request, mode, class_id):
        if mode == 'create':
            context = {'form':ClassForm(), 'mode':'Create'}
        elif mode == 'edit':
            to_edit = StudentClass.objects.get(id=class_id)
            context = {'form':ClassForm(instance=to_edit), 'mode':'Edit'}
        else:
            to_delete = StudentClass.objects.get(id=class_id)
            context = {'form':ClassForm(instance=to_delete)}
        return render(request, 'admin/add_class.html', context)

    @method_decorator(is_admin)
    def post(self, request, mode, class_id):
        if mode == 'create':
            form = ClassForm(request.POST)
            if form.is_valid():
                info = form.save(commit=False)
                info.save()
                messages.success(request, (f'Class: {info.class_name} {info.section} has been created!'))
                return redirect('sims_admin:create_class','create', 0)
            return render(request, 'admin/add_class.html', {'form':form})

        elif mode == 'edit':
            edit = StudentClass.objects.get(id=class_id)
            form = ClassForm(request.POST, instance=edit)
            if form.is_valid():
                info = form.save(commit=False)
                info.save()
                messages.success(request, (f'Class: {info.class_name} {info.section} has been updated!'))

                student_class = StudentClass.objects.all().order_by('-id')
                context = {
                    'classes':student_class,
                    'mode':'Classes',
                }
                return render(request, 'admin/student_class_list.html', context)
            else:
                messages.error(request, (f'Error processing class update'))

            return render(request, 'admin/add_class.html', {'form':form})
        else:
            try:
                delete = StudentClass.objects.get(id=class_id)
                delete.delete()
                messages.success(request, (f'{delete} has been deleted!'))
            except StudentClass.DoesNotExist:
                messages.error(request, (f'Error deleting class!'))
            finally:
                student_class = StudentClass.objects.all().order_by('-id')
                context = {
                    'classes':student_class,
                    'mode':'Classes',
                }
                return render(request, 'admin/student_class_list.html', context)

class AddStaffView(LoginRequiredMixin, View):
    @method_decorator(is_admin)
    def get(self, request):
        context = {
            'form':AccountRegistrationForm(),
            'form1':StaffForm()
        }
        return render(request, 'admin/add_staff.html', context)

    @method_decorator(is_admin)
    def post(self, request):
        form = AccountRegistrationForm(request.POST)
        form1 = StaffForm(request.POST)
        if form.is_valid() and form1.is_valid():
            user = form.save(commit=False)
            user_profile = form1.save(commit=False)

            user.schNo = str(generate_schno('staff'))
            user.is_staff = True
            user.set_password(user.password)
            user_profile.staff_acct = user

            user.save()
            user_profile.save()
            messages.success(request, ('Staff Account creation successful'))
            return redirect('sims_admin:add_staff')
        context = {
            'form':form,
            'form1':form1
        }
        return render(request, 'admin/add_staff.html', context)

class AddAdminView(View):
    @method_decorator(is_admin)
    def get(self, request):
        context = {
            'form':AccountRegistrationForm(),
            'form1':AdminForm()
        }
        return render(request, 'admin/add_admin.html', context)

    @method_decorator(is_admin)
    def post(self, request):
        form = AccountRegistrationForm(request.POST)
        form1 = AdminForm(request.POST)
        if form.is_valid() and form1.is_valid():
            user = form.save(commit=False)
            user_profile = form1.save(commit=False)

            user.schNo = str(generate_schno('staff'))
            user.is_staff = True
            user.is_superuser = True
            user.set_password(user.password)
            user_profile.admin_acct = user

            user.save()
            user_profile.save()
            messages.success(request, ('Admin Account creation successful'))
            return redirect('sims_admin:add_admin')
        context = {
            'form':form,
            'form1':form1
        }
        return render(request, 'admin/add_admin.html', context)

class EditAdminView(View):
    @method_decorator(is_admin)
    def get(self, request, user_id):
        admin = Admins.objects.get(id=user_id)
        acct = Accounts.objects.get(id=admin.admin_acct.id)
        context = {
            'form':AccountEditForm(instance=acct),
            'form1':AdminForm(instance=admin)
        }
        return render(request, 'admin/edit_admin.html', context)

    @method_decorator(is_admin)
    def post(self, request, user_id):
        admin = Admins.objects.get(id=user_id)
        acct = Accounts.objects.get(id=admin.admin_acct.id)

        form = AccountEditForm(request.POST, instance=acct)
        form1 = AdminForm(request.POST, instance=admin)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            messages.success(request, ('Admin Account Updated successfully'))
            return redirect('sims_admin:admin_list')
        context = {
            'form':form,
            'form1':form1
        }
        return render(request, 'admin/edit_admin.html', context)

class DeleteAdminView(View):
    @method_decorator(is_admin)
    def post(self, request, user_id):
        try:
            admin = Admins.objects.get(id=user_id)
            admin.delete()
            messages.success(request, ('Admin Account Deleted successfully'))
            return redirect('sims_admin:admin_list')
        except:
            messages.error(request, ('Error deleting admin'))
            return redirect('sims_admin:admin_list')

class DeleteStudentView(View):
    @method_decorator(is_admin)
    def post(self, request, user_id):
        try:
            student = Student.objects.get(id=user_id)
            student.delete()
            messages.success(request, ('Student Account Deleted successfully'))
            return redirect('sims_admin:student_list', student.student_class.class_name, student.student_class.section)
        except:
            messages.error(request, ('Error deleting student'))
            return redirect('sims_admin:list_student_class', 'manage')

class DeleteStaffView(View):
    @method_decorator(is_admin)
    def post(self, request, user_id):
        try:
            staff = Staff.objects.get(id=user_id)
            staff.delete()
            messages.success(request, ('Staff Account Deleted successfully'))
            return redirect('sims_admin:list_staffs')
        except:
            messages.error(request, ('Error deleting staff'))
            return redirect('sims_admin:list_staffs')

class ListSubjectsView(LoginRequiredMixin, View):
    @method_decorator(is_admin)
    def get(self, request, subject_id, mode='view'):
        if mode == 'delete':
            subject = Subjects.objects.get(id=subject_id)
            subject.delete()
            messages.success(request, ('Subject deleted!'))
            return redirect('sims_admin:list_subjects', 0, 'view')
        elif mode == 'edit':
            subject = Subjects.objects.get(id=subject_id)
            context = {'form':SubjectForm(instance=subject)}
            return render(request, 'admin/edit_subject.html', context)
        else:
            subjects = Subjects.objects.all().order_by('-id')
            context = {
                'subjects':subjects,
            }
            return render(request, 'admin/list_subject.html', context)

class EditSubjectsView(LoginRequiredMixin, View):
    @method_decorator(is_admin)
    def get(self, request, subject_id):
        subject = Subjects.objects.get(id=subject_id)
        context = {'form':SubjectForm(instance=subject)}
        return render(request, 'admin/edit_subject.html', context)

    @method_decorator(is_admin)
    def post(self, request, subject_id):
        subject = Subjects.objects.get(id=subject_id)
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, ('Subject Updated successfully'))
            return redirect('sims_admin:list_subjects', 0, 'view')
        context = {
            'form':form,
        }
        return render(request, 'admin/edit_admin.html', context)

class ListSubjectsComboView(LoginRequiredMixin, View):
    @method_decorator(is_admin)
    def get(self, request, combo_id, mode='view'):
        if mode == 'delete':
            subject = SubjectCombination.objects.get(id=combo_id)
            subject.delete()
            messages.success(request, ('Subject Combination deleted!'))
            return redirect('sims_admin:list_subjects_combo', 0, 'view')
        else:
            subjects = SubjectCombination.objects.all().order_by('-id')
            context = {
                'subjects':subjects,
            }
            return render(request, 'admin/list_subject_combo.html', context)

class EditSubjectComboView(LoginRequiredMixin, View):
    @method_decorator(is_admin)
    def get(self, request, combo_id):
        combo = SubjectCombination.objects.get(id=combo_id)
        context = {'form':SubjectCombinationForm(instance=combo)}
        return render(request, 'admin/edit_subject_combo.html', context)

    @method_decorator(is_admin)
    def post(self, request, combo_id):
        combo = SubjectCombination.objects.get(id=combo_id)
        form = SubjectCombinationForm(request.POST, instance=combo)
        if form.is_valid():
            info = form.save(commit=False)
            info.combination_desc = f'{info.select_subject} {info.select_class}'
            try:
                info.save()
                messages.success(request, (f'Subject: {info.select_subject} has been linked with Class: {info.select_class}'))
                return redirect('sims_admin:list_subjects_combo', 0, 'view')
            except IntegrityError:
                messages.error(request, (f'Subject has already been linked with class'))
        return render(request, 'admin/edit_subject_combo.html', {'form':form})

class ListStudentClassView(LoginRequiredMixin, View):
    def get(self, request, mode='manage'):
        try:
            student_class = StudentClass.objects.all().order_by('-id')
            if mode == 'class':
                context = {
                    'classes':student_class,
                    'mode':'Classes',
                }
            else:
                context = {
                'classes':student_class,
                'mode':'Students',
            }
            return render(request, 'admin/student_class_list.html', context)
        except:
            return render(request, 'admin/student_class_list.html')

class ListStaffsView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            all_Staffs = Staff.objects.all().order_by('-id')
            context = {
                'staffs':all_Staffs,
            }
            return render(request, 'admin/list_staff.html', context)
        except:
            return render(request, 'admin/list_staff.html')

class StudentListView(LoginRequiredMixin, View):
    def get(self, request, class_name, class_section):
        try:
            students_class = StudentClass.objects.get(class_name=class_name, section=class_section)
            students = Student.objects.filter(student_class_id=students_class.id).order_by('-id')
            context = {
                'students':students,
            }
            return render(request, 'admin/student_list.html', context)
        except:
            return render(request, 'admin/student_list.html')

class AdminListView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            admins = Admins.objects.all().order_by('-id')
            context = {
                'admins':admins,
            }
            return render(request, 'admin/admin_list.html', context)
        except:
            return render(request, 'admin/admin_list.html')

class AssignedClassView(LoginRequiredMixin, View):
    def get(self, request, mode):
        staff = Staff.objects.get(staff_acct_id=request.user.id)
        class_list = StaffClassCombination.objects.filter(staff_id=staff)

        # Display student in the class
        if mode == 'upload':
            context = {'class_list':class_list, 'mode':'upload'}
        else:
            context = {'class_list':class_list, 'mode':'view'}
        return render(request, 'admin/assigned_class.html', context)

class MyStudentView(LoginRequiredMixin, View):
    def get(self, request, class_name, mode):
        # String spliting
        prefix = class_name[:-2]
        suffix = class_name[-1]
        # Getting students
        class_id = StudentClass.objects.get(class_name=prefix, section=suffix)
        students = Student.objects.filter(student_class=class_id)
        # Display student in the class
        if mode == 'upload':
            context = {'students':students, 'mode':'upload'}
        else:
            context = {'students':students, 'mode':'view'}
        return render(request, 'admin/my_students.html', context)

class AddGradeOrViewResult(LoginRequiredMixin, View):
    @method_decorator(is_staff)
    def get(self, request, user_id, mode):
        if mode == 'upload':
            try:
                student = Student.objects.get(student_acct_id=user_id)
                form = StudentGradesForm()
                form.fields['select_subject'].queryset = SubjectCombination.objects.filter(select_class_id=student.student_class_id)
                context = {
                    'user':student,
                    'form':form,
                    'mode':'Upload'
                }
            except Student.DoesNotExist:
                context = {'form':StudentGradesForm()}
            return render(request, 'admin/add_grades.html', context)
        else:
            student = Student.objects.get(student_acct_id=user_id)
            grades = StudentGrades.objects.filter(select_student_id=student.id)
            average = StudentGrades.objects.filter(select_student_id=student.id)
            total = 0
            for subject in grades:
                total += subject.student_total
            try:
                average = f'{total/len(grades):.1f}'
            except ZeroDivisionError:
                average = ''
            context = {
                'user':student,
                'grades':grades,
                'average':average,
                'total':total,
            }
            return render(request, 'admin/student_result.html', context)
    @method_decorator(is_staff)
    def post(self, request, user_id, mode='upload'):
        user = Student.objects.get(student_acct_id=user_id)
        form = StudentGradesForm(data=request.POST)

        if form.is_valid():
            info = form.save(commit=False)
            slug = f'{user} {info.select_subject}'

            #Total score
            total = int(info.student_ca1) + int(info.student_ca2) + int(info.student_ca3) + int(info.student_exam)
            info.student_total = total
            info.slug = slug
            info.select_student = user

            try:
                info.save()
                messages.success(request, ('Grade Added successful!!'))
            except IntegrityError:
                messages.error(request, ('Student Grade has already been added for that subject'))
                form.fields['select_subject'].queryset = SubjectCombination.objects.filter(select_class_id=user.student_class_id)

                return render(request, 'admin/add_grades.html', {'form':form, 'user':user, 'mode':'Upload'})
        else:
            messages.error(request, ('Error processing Grades Try again!'))
            form.fields['select_subject'].queryset = SubjectCombination.objects.filter(select_class_id=user.student_class_id)
            return render(request, 'admin/add_grades.html', {'form':form, 'user':user, 'mode':'Upload'})
        return redirect('sims_admin:add_grades', user_id /'upload')

class EditGradeView(LoginRequiredMixin, View):
    @method_decorator(is_staff)
    def get(self, request, subject, user_id):
        try:
            student = Student.objects.get(student_acct_id=user_id)
            subject = StudentGrades.objects.get(id=subject)
            form = StudentGradesForm(instance=subject)
            form.fields['select_subject'].queryset = SubjectCombination.objects.filter(id=subject.select_subject_id)
            context = {
                'user':student,
                'form':form,
                'mode':'Edit'
            }
        except Student.DoesNotExist:
            context = {'form':StudentGradesForm()}
        return render(request, 'admin/add_grades.html', context)

    @method_decorator(is_staff)
    def post(self, request, subject, user_id):
        user = Student.objects.get(student_acct_id=user_id)
        subject = StudentGrades.objects.get(id=subject)
        form = StudentGradesForm(data=request.POST, instance=subject)

        if form.is_valid():
            info = form.save(commit=False)
            #Total score
            total = int(info.student_ca1) + int(info.student_ca2) + int(info.student_ca3) + int(info.student_exam)
            info.student_total = total
            info.save()
            messages.success(request, ('Grades has been Edited successfully!!'))
        else:
            messages.error(request, ('Error Editing Grades Try again!'))
            return render(request, 'admin/add_grades.html', {'form':form, 'user':user, 'mode':'Edit'})

        return redirect('sims_admin:add_grades', user_id, 'view')

class DeleteGradeView(LoginRequiredMixin, View):
    @method_decorator(is_staff)
    def get(self, request, subject, user_id):
        subject = StudentGrades.objects.get(select_subject_id=subject)
        subject.delete()
        messages.success(request, ('Grade deleted!'))
        return redirect('sims_admin:add_grades', user_id, 'view')

class ResultToPDFView(LoginRequiredMixin, View):
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]

        else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))

            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, user_id):
        # Logic
        student = Student.objects.get(student_acct_id=user_id)
        grades = StudentGrades.objects.filter(select_student_id=student.id)
        average = StudentGrades.objects.filter(select_student_id=student.id)
        total = 0
        for subject in grades:
            total += subject.student_total
        average = f'{total/len(grades):.1f}'

        template_path = 'admin/result_pdf.html'
        context = {
            'user':student,
            'grades':grades,
            'average':average,
            'total':total,
        }
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="result.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=self.link_callback)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response