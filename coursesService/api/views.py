from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
import requests
from django.db import models
from django.conf import settings
from base.models import Course
from .serializers import CourseSerializer
from .permissions import IsStudent, IsStaff, IsAdmin

@api_view(['GET'])
def test_routing(request):
    return Response({'message': 'API routing works'})

@api_view(['GET'])
@permission_classes([IsStudent])
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
@permission_classes([IsStudent])
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

@api_view(['POST'])
@permission_classes([IsStaff])
def createCourse(request):
    """
    Create a new course and its associated discussion.
    """
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        course = serializer.save(creator_id=request.user.id)
        # Use correct base URL for discussions service
        discussion_service_url = f"{settings.DISCUSSIONS_API_BASE_URL}course-discussions/"
        discussion_data = {
            "course_id": str(course.courseID),
            "course_subject": course.courseSubject,
            "title": f"Discussion for {course.title}",
            "body": f"This is the general discussion thread for {course.courseSubject} {course.courseID}: {course.title}.",
            "author": "System"
        }
        try:
            requests.post(discussion_service_url, json=discussion_data)
        except requests.exceptions.RequestException as e:
            print(f"Failed to create discussion: {e}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsStaff])
def deleteCourse(request, courseSubject, courseID):
    """
    Delete a course and its associated discussion.
    """
    qs = Course.objects.filter(courseSubject__iexact=courseSubject, courseID=courseID)
    try:
        course = qs.get()
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    # Use correct base URL for discussions service
    discussion_service_url = f"{settings.DISCUSSIONS_API_BASE_URL}course-discussions/"
    url = f"{discussion_service_url}{course.courseSubject}/{course.courseID}/"
    try:
        requests.delete(url)
    except requests.exceptions.RequestException as e:
        print(f"Failed to delete discussion: {e}")
    course.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

