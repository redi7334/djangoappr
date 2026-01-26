from django.test import TestCase
from core.models import Subject, StudySession
from django.test import Client
import json

class SubjectTests(TestCase):
    def setUp(self):
        self.subject1 = Subject.objects.create(
            name="Test Name",
            description="Test Description"
        )
        self.subject2 = Subject.objects.create(
            name="Test 2",
            description="Test 2"
        )

    def test_get_subject(self):
        c = Client()
        subject_id = self.subject1.id
        response = c.get(f"/subject/{subject_id}/")
        self.assertEqual(response.json()["name"], "Test Name")

    def test_patch_subject(self):
        c = Client()
        subject_id = self.subject1.id

        response = c.patch(f"/subject/{subject_id}/", json.dumps({"name":"New Name",
                                                       "description":"New description"}))
        self.assertEqual(response.json()["message"], "Object Updated succesfully")

        updated_subject = Subject.objects.get(id=subject_id)
        self.assertEqual(updated_subject.name, "New Name")

    def test_delete_subject(self):
        c = Client()
        old_subject = self.subject1
        response = c.delete(f"/subject/{old_subject.id}/")
        self.assertEqual(response.json(), {"message": "Deleted succesfully"})

class StudySessionTests(TestCase):
    def setUp(self):
        self.subject1 = Subject.objects.create(
            name="Test Name",
            description="Test Description"
        )
        self.ss1 = StudySession.objects.create(
            subject=self.subject1,
            datetime="2025-12-12",
            duration_minutes=60,
            notes="Test Description"
        )

    def test_search_date_invalid_year(self):
        c = Client()
        response = c.get(f"/search-by-date/3000-12-12/")
        self.assertEqual(response.json(), {"Error":"Invalid year"})

    def test_ss_not_found(self):
        c = Client()
        response = c.get(f"/search-by-date/2024-12-12/")
        self.assertEqual(response.json(), {"Error":"StudySession not found"})

    def test_total_time_subject_not_found(self):
        c = Client()
        response = c.get(f"/total-time/999/")
        self.assertEqual(response.json(), {"Error":"Subject not found"})