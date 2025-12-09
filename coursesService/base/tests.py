from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from base.models import Course
from unittest.mock import patch
from django.test import override_settings

@override_settings(DISCUSSIONS_API_BASE_URL="http://testserver/api/discussions/")
class CourseAPITestCase(TestCase):
    """
    Unit tests for the Course API endpoints.
    Each test follows best practices: explicit precondition, test, and postcondition assertions.
    """

    def setUp(self):
        self.client = APIClient()
        self.student_headers = {'HTTP_AUTHORIZATION': 'bearer student'}
        self.staff_headers = {'HTTP_AUTHORIZATION': 'bearer staff'}
        self.admin_headers = {'HTTP_AUTHORIZATION': 'bearer admin'}
        # Patch authentication to simulate user roles
        self.patcher = patch('coursesService.authentication.ExternalJWTAuthentication.authenticate', side_effect=self.fake_auth)
        self.patcher.start()
        # Prepopulate with two courses
        self.course1 = Course.objects.create(
            courseID=1,
            courseSubject="COMPSCI", title="Intro to CS", instructor="Smith",
            credits=3, schedule="MWF 10:00-10:50", room="CS101",
            requirements="", description="Basics", instruction_mode="In Person"
        )
        self.course2 = Course.objects.create(
            courseID=2,
            courseSubject="BIOLOGY", title="Genetics", instructor="Jones",
            credits=4, schedule="TTh 11:00-12:15", room="BIO201",
            requirements="", description="Genes", instruction_mode="Online"
        )
        self.course1.refresh_from_db()
        self.course2.refresh_from_db()

    def tearDown(self):
        self.patcher.stop()

    def fake_auth(self, request):
        # Simulate user roles based on Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token = auth_header.split()[-1].lower() if auth_header else ''
        roles = {
            'student': {'id': 1, 'role': 'STUDENT', 'is_authenticated': True},
            'staff': {'id': 2, 'role': 'STAFF', 'is_authenticated': True},
            'admin': {'id': 3, 'role': 'ADMIN', 'is_authenticated': True},
        }
        user_info = roles.get(token, {'id': 0, 'role': 'STUDENT', 'is_authenticated': True})
        class DummyUser:
            def __init__(self, info):
                self.id = info['id']
                self.role = info['role']
                self.is_authenticated = info['is_authenticated']
        return (DummyUser(user_info), {})

    def test_api_overview(self):
        """
        Test the /api/ endpoint.
        """
        # Precondition assertion
        self.assertEqual(Course.objects.count(), 2, "Precondition: 2 courses exist.")
        # Testing assertion
        response = self.client.get('/api/', **self.student_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Testing: Should return 200 OK.")
        self.assertIn('getCourses', response.data, "Testing: 'getCourses' endpoint should be listed.")
        # Postcondition assertion
        self.assertEqual(Course.objects.count(), 2, "Postcondition: No courses should be changed.")

    def test_list_courses(self):
        """
        Test listing all courses.
        """
        # Precondition assertion
        self.assertEqual(Course.objects.count(), 2, "Precondition: 2 courses exist.")
        # Testing assertion
        response = self.client.get('/api/courses/', **self.student_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Testing: Should return 200 OK.")
        self.assertEqual(len(response.data), 2, "Testing: Should return 2 courses.")
        subjects = [course['courseSubject'] for course in response.data]
        self.assertEqual(subjects, sorted(subjects), "Testing: Courses should be sorted.")
        # Postcondition assertion
        self.assertEqual(Course.objects.count(), 2, "Postcondition: No courses should be changed.")

    def test_filter_by_subject(self):
        """
        Test filtering by subject.
        """
        # Precondition assertion
        self.assertEqual(Course.objects.count(), 2, "Precondition: 2 courses exist.")
        # Testing assertion
        response = self.client.get('/api/courses/?courseSubject=COMPSCI', **self.student_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Testing: Should return 200 OK.")
        self.assertEqual(len(response.data), 1, "Testing: Should return 1 course.")
        self.assertEqual(response.data[0]['courseSubject'], 'COMPSCI', "Testing: Subject should be COMPSCI.")
        # Postcondition assertion
        self.assertEqual(Course.objects.count(), 2, "Postcondition: No courses should be changed.")

    def test_filter_by_instructor(self):
        """
        Test filtering by instructor.
        """
        # Precondition assertion
        self.assertEqual(Course.objects.count(), 2, "Precondition: 2 courses exist.")
        # Testing assertion
        response = self.client.get('/api/courses/?instructor=Jones', **self.student_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Testing: Should return 200 OK.")
        self.assertEqual(len(response.data), 1, "Testing: Should return 1 course.")
        self.assertEqual(response.data[0]['instructor'], 'Jones', "Testing: Instructor should be Jones.")
        # Postcondition assertion
        self.assertEqual(Course.objects.count(), 2, "Postcondition: No courses should be changed.")

    def test_filter_by_title_partial(self):
        """
        Test filtering by partial title.
        """
        # Precondition assertion
        self.assertEqual(Course.objects.count(), 2, "Precondition: 2 courses exist.")
        # Testing assertion
        response = self.client.get('/api/courses/?title=Gen', **self.student_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Testing: Should return 200 OK.")
        self.assertEqual(len(response.data), 1, "Testing: Should return 1 course.")
        self.assertIn('Gen', response.data[0]['title'], "Testing: Title should contain 'Gen'.")
        # Postcondition assertion
        self.assertEqual(Course.objects.count(), 2, "Postcondition: No courses should be changed.")

    def test_no_results(self):
        """
        Test filtering with no results.
        """
        # Precondition assertion
        self.assertEqual(Course.objects.count(), 2, "Precondition: 2 courses exist.")
        # Testing assertion
        response = self.client.get('/api/courses/?courseSubject=PHYSICS', **self.student_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Testing: Should return 200 OK.")
        self.assertEqual(len(response.data), 0, "Testing: Should return 0 courses.")
        # Postcondition assertion
        self.assertEqual(Course.objects.count(), 2, "Postcondition: No courses should be changed.")

    @patch('api.views.requests.post')
    def test_create_course(self, mock_post):
        """
        Test creating a course (STAFF only).
        """
        # Precondition assertion
        self.assertEqual(Course.objects.count(), 2, "Precondition: 2 courses exist.")
        new_course = {
            "courseID": 999,
            "courseSubject": "MATH",
            "title": "Calculus",
            "instructor": "Taylor",
            "credits": 4,
            "schedule": "MWF 9:00-9:50",
            "room": "MATH101",
            "requirements": "None",
            "description": "Intro to Calculus",
            "instruction_mode": "In Person"
        }
        response = self.client.post('/api/courses/create/', new_course, format='json', **self.staff_headers)
        # Testing assertion
        if response.status_code != status.HTTP_201_CREATED:
            print('Create course response:', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Testing: Should return 201 Created.")
        self.assertEqual(Course.objects.count(), 3, "Testing: Should have 3 courses after creation.")
        # Postcondition assertion
        created = Course.objects.get(title="Calculus")
        self.assertEqual(created.instructor, "Taylor", "Postcondition: Instructor should be Taylor.")
        mock_post.assert_called()

    @patch('api.views.requests.delete')
    def test_delete_course(self, mock_delete):
        """
        Test deleting a course (STAFF only).
        """
        # Precondition assertion
        self.assertEqual(Course.objects.count(), 2, "Precondition: 2 courses exist.")
        # Testing assertion
        url = f'/api/courses/{self.course1.courseSubject}/{self.course1.courseID}/delete/'
        response = self.client.delete(url, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, "Testing: Should return 204 No Content.")
        self.assertEqual(Course.objects.count(), 1, "Testing: Should have 1 course after deletion.")
        # Postcondition assertion
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(courseID=self.course1.courseID)
        mock_delete.assert_called()

    def test_api_routing(self):
        """
        Test the /api/test-routing/ endpoint to verify API routing.
        """
        response = self.client.get('/api/test-routing/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'API routing works')