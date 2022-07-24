from django.urls import path

# My app imports
from SIMS_Admin.views import (
    DashboardView,
    ProfileView,
    AddStudentView,
    AddStaffView,
    AddSubjectView,
    AssingSubjectView,
    CreateEditDeleteClassView,
    ListStudentClassView,
    StudentListView,
    ListStaffsView,
    AssignClassView,
    AssignedClassView,
    MyStudentView,
    AddGradeOrViewResult,
    EditGradeView,
    DeleteGradeView,
    ResultToPDFView,
    AddAdminView,
    AdminListView,
    EditAdminView,
    DeleteAdminView,
    ListSubjectsView,
    EditSubjectsView,
    ListSubjectsComboView,
    EditSubjectComboView,
    DeleteStudentView,
    DeleteStaffView
)

app_name = 'sims_admin'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('profile/<int:user_id>', ProfileView.as_view(), name='profile'),
    path('add_student', AddStudentView.as_view(), name='add_student'),
    path('add_staff', AddStaffView.as_view(), name='add_staff'),
    path('assign_subject', AssingSubjectView.as_view(), name='assign_subject'),
    path('assign_class', AssignClassView.as_view(), name='assign_class'),
    path('create_class/<str:mode>/<int:class_id>', CreateEditDeleteClassView.as_view(), name='create_class'),
    path('list_student_class/<str:mode>', ListStudentClassView.as_view(), name='list_student_class'),
    path('student_list/<str:class_name>/<str:class_section>/', StudentListView.as_view(), name='student_list'),
    path('list_staffs', ListStaffsView.as_view(), name='list_staffs'),

    # subjects
    path('add_subject', AddSubjectView.as_view(), name='add_subject'),
    path('list_subjects/<int:subject_id>/<str:mode>', ListSubjectsView.as_view(), name='list_subjects'),
    path('list_subjects_combo/<int:combo_id>/<str:mode>', ListSubjectsComboView.as_view(), name='list_subjects_combo'),
    path('edit_subject/<int:subject_id>/', EditSubjectsView.as_view(), name='edit_subject'),
    path('edit_subject_combo/<int:combo_id>/', EditSubjectComboView.as_view(), name='edit_subject_combo'),

    #upload staff
    path('assigned_class/<str:mode>', AssignedClassView.as_view(), name='assigned_class'),
    path('my_student/<str:class_name>/<str:mode>', MyStudentView.as_view(), name='my_student'),
    path('add_grades/<int:user_id>/<str:mode>', AddGradeOrViewResult.as_view(), name='add_grades'),
    # Edit result
    path('edit_grades/<str:subject>/<int:user_id>/', EditGradeView.as_view(), name='edit_grades'),
    path('delete_grades/<str:subject>/<int:user_id>/', DeleteGradeView.as_view(), name='delete_grades'),
    path('result_pdf/<int:user_id>/', ResultToPDFView.as_view(), name='result_pdf'),
    #Add Admin
    path('add_admin', AddAdminView.as_view(), name='add_admin'),
    path('admin_list', AdminListView.as_view(), name='admin_list'),
    path('edit_admin/<int:user_id>/', EditAdminView.as_view(), name='edit_admin'),
    path('delete_admin/<int:user_id>/', DeleteAdminView.as_view(), name='delete_admin'),
    path('delete_student/<int:user_id>/', DeleteStudentView.as_view(), name='delete_student'),
    path('delete_staff/<int:user_id>/', DeleteStaffView.as_view(), name='delete_staff'),
]
