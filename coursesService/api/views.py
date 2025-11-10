from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import models
from base.models import Course
from .serializers import CourseSerializer

@api_view(['GET'])
def apiOverview(request):
    endpoints = {
        'getCourses': '/api/courses/',
        # Add other endpoints as needed
    }
    return Response(endpoints)

@api_view(['GET'])
def getCourses(request):
    courses = Course.objects.all()
    courseSubject = request.GET.get('courseSubject', '')
    courseID = request.GET.get('courseID', '')
    title = request.GET.get('title', '')
    instructor = request.GET.get('instructor', '')

    if courseSubject:
        courses = courses.filter(courseSubject__icontains=courseSubject)
    if courseID:
        courses = courses.filter(courseID=courseID)
    if title:
        courses = courses.filter(title__icontains=title)
    if instructor:
        courses = courses.filter(instructor__icontains=instructor)

    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

