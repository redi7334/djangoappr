from rest_framework import serializers
from core.models import Subject, StudySession

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class StudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySession
        fields = "__all__"