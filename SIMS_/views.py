from django.shortcuts import render, redirect
from django.views import View

from SIMS_Admin.models import Student, Subjects

# Create your views here.
class HomeView(View):
    def get(self, request):
        subjects = Subjects.objects.all().order_by('-id').count()
        students = Student.objects.all().order_by('-id').count()
        context = {
            'subjects':subjects,
            'students':students
        }
        return render(request, 'sims/index.html', context)
