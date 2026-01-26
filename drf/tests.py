from django.test import TestCase
from rest_framework.test import APITestCase
from core.models import Subject
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

        self.assertEqual(response.data[0]["id"], 1)
        self.assertEqual(response.data[0]["description"], "Test Description")

    def test_all_subjects_post(self):
        payload = {"name":"Success", "description": "Success"}

        url = reverse("all-subjects")
        response = self.client.post(url, payload)

        new_subject = Subject.objects.get(name="Success")
        self.assertIsNotNone(new_subject)
        self.assertEqual(new_subject.description, payload["description"])