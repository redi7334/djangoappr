from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class StudySession(models.Model):
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    duration_minutes = models.IntegerField()
    notes = models.TextField(blank=True)