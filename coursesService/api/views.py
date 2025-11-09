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
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

