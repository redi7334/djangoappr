from django.test import TestCase
from rest_framework.test import APITestCase
from core.models import Subject,StudySession
from django.urls import reverse

# Create your tests here.

class SubjectTests(APITestCase):
    def setUp(self):
        self.subject1 = Subject.objects.create(
            name="Test Name",
            description="Test Description"
        )
        self.subject2 = Subject.objects.create(
            name="Test 2",
            description="Test 2"
        )

    def test_all_subjects(self):
        url = reverse("all-subjects")
        response = self.client.get(url)

        self.assertEqual(response.data[0]["id"], self.subject1.id)
        self.assertEqual(response.data[0]["description"], self.subject1.description)        

    def test_all_subjects_post(self):
        payload = {"name":"Success", "description": "Success"}

        url = reverse("all-subjects")
        response = self.client.post(url, payload)

        new_subject = Subject.objects.get(name="Success")
        self.assertIsNotNone(new_subject)
        self.assertEqual(new_subject.description, payload["description"])


class StudySessionTests(APITestCase):
    def setUp(self):
        self.subject=Subject.objects.create(name="Test1",description="Test test")
        self.study_session1 = StudySession.objects.create(
            subject = self.subject,
            datetime = "2026-01-22",
            duration_minutes = 60,
            notes="test test"
        )

    def test_get_session(self):
        ss_id = self.study_session1.id
        url = reverse(f"study-session",kwargs={"numri":ss_id})
        response = self.client.get(url)

        self.assertEqual(response.data["id"],self.study_session1.id)
        #self.assertEqual(response.data["datetime"],self.study_session1.datetime)
        self.assertEqual(response.data["duration_minutes"],self.study_session1.duration_minutes)


    def test_total_time_all_subjects(self):
           # Create second session for the same subject
        StudySession.objects.create(
            subject=self.subject,
            datetime="2026-01-23",
            duration_minutes=45,
            notes="bonus test"
        )
        
        url = reverse("total-time-all-subjects")
        response = self.client.get(url)

        
        # Total should be 60 (from setUp) + 45 = 105
        expected_total = 105
        
        # Find the dictionary for our subject
        subject_data = next(item for item in response.data if item["id"] == self.subject.id)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(subject_data["Total Time"], expected_total)