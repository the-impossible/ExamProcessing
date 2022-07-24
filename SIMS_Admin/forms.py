from django import forms

# My App imports
from SIMS_Admin.models import (
    Student,
    StudentRoles,
    StudentClass,
    Subjects,
    SubjectCombination,
    StudentClass,
    StaffRoles,
    Staff,
    StaffClassCombination,
    StudentGrades,
    Admins,
)
from SIMS_Authentication.models import Accounts

class StudentForm(forms.ModelForm):
    select_gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    student_class = forms.ModelChoiceField(queryset=StudentClass.objects.all(), initial=1, required=True, widget=forms.Select(
        attrs={
            'class':'form-select'
        }
    ))

    student_role = forms.ModelChoiceField(queryset=StudentRoles.objects.all(), initial=3, required=False, widget=forms.Select(
        attrs={
            'class':'form-select'
        }
    ))
    student_gender = forms.ChoiceField(choices=select_gender, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    student_date_of_birth = forms.DateTimeField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'date'
        }
    ))


    class Meta:
        model = Student
        fields = ('student_class', 'student_role', 'student_gender', 'student_date_of_birth')

class SubjectForm(forms.ModelForm):
    subject_title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    subject_code = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))


    class Meta:
        model = Subjects
        fields = ('subject_title', 'subject_code')

class SubjectCombinationForm(forms.ModelForm):
    select_class = forms.ModelChoiceField(queryset=StudentClass.objects.all(), initial=3, required=False, widget=forms.Select(
        attrs={
            'class':'form-select'
        }
    ))

    select_subject = forms.ModelChoiceField(queryset=Subjects.objects.all(), initial=3, required=False, widget=forms.Select(
        attrs={
            'class':'form-select'
        }
    ))

    class Meta:
        model = SubjectCombination
        fields = ('select_class', 'select_subject')

class StaffClassCombinationForm(forms.ModelForm):
    student_class = forms.ModelChoiceField(queryset=StudentClass.objects.all(), required=False, widget=forms.Select(
        attrs={
            'class':'form-select'
        }
    ))

    staff = forms.ModelChoiceField(queryset=Staff.objects.all(), required=False, widget=forms.Select(
        attrs={
            'class':'form-select'
        }
    ))

    class Meta:
        model = StaffClassCombination
        fields = ('student_class', 'staff')

class StudentGradesForm(forms.ModelForm):
    student_ca1 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    student_ca2 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    student_ca3 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    student_exam = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    select_subject = forms.ModelChoiceField(queryset=SubjectCombination.objects.all(), required=False, widget=forms.Select(
        attrs={
            'class':'form-select'
        }
    ))

    def clean_student_ca1(self):
        student_ca1 = self.cleaned_data.get('student_ca1')
        if int(student_ca1) > 10:
            raise forms.ValidationError('Score should be over 10')
        return student_ca1

    def clean_student_ca2(self):
        student_ca2 = self.cleaned_data.get('student_ca2')
        if int(student_ca2) > 10:
            raise forms.ValidationError('Score should be over 10')
        return student_ca2

    def clean_student_ca3(self):
        student_ca3 = self.cleaned_data.get('student_ca3')
        if int(student_ca3) > 10:
            raise forms.ValidationError('Score should be over 10')
        return student_ca3

    def clean_student_exam(self):
        student_exam = self.cleaned_data.get('student_exam')
        if int(student_exam) > 70:
            raise forms.ValidationError('Score should be over 70')
        return student_exam

    class Meta:
        model = StudentGrades
        fields = ('student_ca1', 'student_ca2', 'student_ca3', 'student_exam', 'select_subject')

class ClassForm(forms.ModelForm):
    class_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    section = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    class Meta:
        model = StudentClass
        fields = ('class_name', 'section')

class AccountEditForm(forms.ModelForm):
    firstname = forms.CharField(required=True, help_text='Please enter your firstname',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    lastname = forms.CharField(required=True, help_text='Please enter your lastname', widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    othername = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    email = forms.EmailField(required=False, help_text='Enter a valid email address', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'email',
            'readonly':'readonly'
        }
    ))

    schNo = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'readonly':'readonly'
        }
    ))


    class Meta:
        model = Accounts
        fields = ('firstname', 'lastname', 'othername', 'email', 'schNo')

class AccountPictureForm(forms.ModelForm):
    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'image/png, image/jpeg'
        }
    ))


    class Meta:
        model = Accounts
        fields = ('picture',)

class StudentEditForm(forms.ModelForm):
    select_gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    student_class = forms.ModelChoiceField(queryset=StudentClass.objects.all(), required=False, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    student_role = forms.ModelChoiceField(queryset=StudentRoles.objects.all(), required=False, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))
    student_gender = forms.ChoiceField(choices=select_gender, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    student_date_of_birth = forms.DateTimeField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'date'
        }
    ))

    class Meta:
        model = Student
        fields = ('student_gender', 'student_date_of_birth')

class StudentEditAdminForm(forms.ModelForm):
    select_gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    student_class = forms.ModelChoiceField(queryset=StudentClass.objects.all(), required=False, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    student_role = forms.ModelChoiceField(queryset=StudentRoles.objects.all(), required=False, widget=forms.Select(
        attrs={
            'class':'form-select',
        }   
    ))
    student_gender = forms.ChoiceField(choices=select_gender, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    student_date_of_birth = forms.DateTimeField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'date'
        }
    ))

    class Meta:
        model = Student
        fields = ('student_gender', 'student_date_of_birth', 'student_class', 'student_role')

class StaffForm(forms.ModelForm):
    select_gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    staff_phone = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))
    staff_gender = forms.ChoiceField(choices=select_gender, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))
    staff_class = forms.ModelChoiceField(queryset=StudentClass.objects.all(), initial=1, required=True, widget=forms.Select(
        attrs={
            'class':'form-select'
        }
    ))

    staff_role = forms.ModelChoiceField(queryset=StaffRoles.objects.all(), initial=3, required=False, widget=forms.Select(
        attrs={
            'class':'form-select'
        }
    ))

    staff_date_of_birth = forms.DateTimeField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'date'
        }
    ))

    class Meta:
        model = Staff
        fields = ('staff_phone', 'staff_class', 'staff_role', 'staff_gender', 'staff_date_of_birth')

class StaffEditForm(forms.ModelForm):
    select_gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    staff_phone = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))
    staff_gender = forms.ChoiceField(choices=select_gender, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    staff_date_of_birth = forms.DateTimeField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'date'
        }
    ))

    class Meta:
        model = Staff
        fields = ('staff_phone', 'staff_gender', 'staff_date_of_birth')

class StaffEditAdminForm(forms.ModelForm):
    select_gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    staff_phone = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))
    staff_gender = forms.ChoiceField(choices=select_gender, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))
    staff_class = forms.ModelChoiceField(queryset=StudentClass.objects.all(), initial=1, required=False, widget=forms.Select(
        attrs={
            'class':'form-select'
        }
    ))
    staff_role = forms.ModelChoiceField(queryset=StaffRoles.objects.all(), initial=3, required=False, widget=forms.Select(
        attrs={
            'class':'form-select'
        }
    ))

    staff_date_of_birth = forms.DateTimeField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'date'
        }
    ))

    class Meta:
        model = Staff
        fields = ('staff_phone', 'staff_class', 'staff_role', 'staff_gender', 'staff_date_of_birth')


class AdminForm(forms.ModelForm):
    select_gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    admin_phone = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))
    admin_gender = forms.ChoiceField(choices=select_gender, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    admin_date_of_birth = forms.DateTimeField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'date'
        }
    ))

    class Meta:
        model = Admins
        fields = ('admin_phone', 'admin_gender', 'admin_date_of_birth')
