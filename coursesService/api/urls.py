from django.urls import path
from . import views
urlpatterns = [
    path('', views.apiOverview, name='apiOverview'),
    path('courses/', views.getCourses, name='getCourses'),
    path('courses/create/', views.createCourse, name='createCourse'),
    path('courses/<str:courseSubject>/<int:courseID>/delete/', views.deleteCourse, name='deleteCourse'),
    path('test-routing/', views.test_routing, name='testRouting'),
]