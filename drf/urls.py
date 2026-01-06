from django.urls import path
from .views import test2, all_subjects, subject, study_session

urlpatterns = [
    path("test2/", test2),
    path("all-subjects/", all_subjects),
    path("subject/<int:numri>", subject),
    path("study-session/<int:numri>", study_session)
]