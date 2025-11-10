from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import models
from base.models import Course
from .serializers import CourseSerializer

@api_view(['GET'])
def apiOverview(request):
    """
    Returns a dictionary of available API endpoints for the courses service.
    """
    endpoints = {
        'getCourses': '/api/courses/',
        # Add other endpoints as needed
    }
    return Response(endpoints)

@api_view(['GET'])
def getCourses(request):
    """
    Retrieve a list of courses, optionally filtered by query parameters.
    Supported filters: courseSubject, courseID, title, instructor.
    Results are always ordered by courseSubject and courseID.
    """
    # Get all courses
    courses = Course.objects.all()

    # Extract filter parameters from request
    courseSubject = request.GET.get('courseSubject', '')
    courseID = request.GET.get('courseID', '')
    title = request.GET.get('title', '')
    instructor = request.GET.get('instructor', '')

    # Apply filters if provided
    if courseSubject:
        courses = courses.filter(courseSubject__icontains=courseSubject)
    if courseID:
        courses = courses.filter(courseID=courseID)
    if title:
        courses = courses.filter(title__icontains=title)
    if instructor:
        courses = courses.filter(instructor__icontains=instructor)

    # Always order results by courseSubject and courseID
    courses = courses.order_by('courseSubject', 'courseID')

    # Serialize and return the course data
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

