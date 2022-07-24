from django.urls import path

# My app imports
from SIMS_.views import (
    HomeView,
)
app_name = 'sims'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
