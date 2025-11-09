from django.urls import path
from . import views
urlpatterns = [
    path('', views.apiOverview, name='apiOverview'),
    path('courses/', views.getCourses, name='getCourses'),
   ]