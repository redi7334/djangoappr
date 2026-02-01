from django.urls import path, include
from .views import (
    test2, SubjectListAsync, subject, study_session, 
    study_session_list, TotalTimeAllSubjectsAsync, SubjectViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"subjects", SubjectViewset, basename="subject")
 
urlpatterns = [
    path("test2/", test2),
    path("all-subjects/", SubjectListAsync.as_view(), name="all-subjects"), 
    path("subject/<int:numri>", subject),
    path("study-session/<int:numri>", study_session, name="study-session"),
    path("study-session-list/", study_session_list),
    path("total-time-all-subjects/", TotalTimeAllSubjectsAsync.as_view(), name="total-time-all-subjects"),
    path("", include(router.urls)),
    
]