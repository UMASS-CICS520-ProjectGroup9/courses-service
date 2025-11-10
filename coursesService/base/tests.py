
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from base.models import Course

class CourseAPITestCase(TestCase):
    """
    Unit tests for the Course API endpoints.
    Precondition: The test database is empty before each test (Django TestCase).
    Postcondition: API returns correct data and status codes for each scenario.
    """

    def setUp(self):
        """
        Precondition: No courses exist in the test database.
        Postcondition: Two sample courses are created for API tests.
        """
        self.course1 = Course.objects.create(
            courseSubject="COMPSCI", title="Intro to CS", instructor="Smith",
            credits=3, schedule="MWF 10:00-10:50", room="CS101",
            requirements="", description="Basics", instruction_mode="In Person"
        )
        self.course2 = Course.objects.create(
            courseSubject="BIOLOGY", title="Genetics", instructor="Jones",
            credits=4, schedule="TTh 11:00-12:15", room="BIO201",
            requirements="", description="Genes", instruction_mode="Online"
        )
        self.client = APIClient()

    def test_list_courses(self):
        """
        Precondition: Two courses exist in the database.
        Postcondition: API returns both courses, sorted by courseSubject and courseID.
        """
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Check ordering by courseSubject
        subjects = [course['courseSubject'] for course in response.data]
        self.assertEqual(subjects, sorted(subjects))

    def test_filter_by_subject(self):
        """
        Precondition: Two courses exist in the database.
        Postcondition: API returns only the course matching the subject filter.
        """
        response = self.client.get('/api/courses/?courseSubject=COMPSCI')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['courseSubject'], 'COMPSCI')

    def test_filter_by_instructor(self):
        """
        Precondition: Two courses exist in the database.
        Postcondition: API returns only the course matching the instructor filter.
        """
        response = self.client.get('/api/courses/?instructor=Jones')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['instructor'], 'Jones')

    def test_filter_by_title_partial(self):
        """
        Precondition: Two courses exist in the database.
        Postcondition: API returns the course(s) whose title contains the search string.
        """
        response = self.client.get('/api/courses/?title=Gen')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('Gen', response.data[0]['title'])

    def test_no_results(self):
        """
        Precondition: Two courses exist in the database.
        Postcondition: API returns an empty list for unmatched filters.
        """
        response = self.client.get('/api/courses/?courseSubject=PHYSICS')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)