from django.urls import path, include
from .views import (  
    TotalTimeAllSubjectsAsync, 
    test2, 
    subject, 
    study_session, 
    study_session_list,
    total_time_all_subjects,
    third_party_api,  
    ss_analytics,
    SubjectViewSet,
    SubjectListAsync,
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
    path("total-time-all-subjects/",total_time_all_subjects, name="total-time-all-subjects"),
    path("total-time-all-subjects-async", TotalTimeAllSubjectsAsync.as_view(), name="total-time-all-subjects-async"),
    path("third-party-api/", third_party_api, name="third-party-api"),
    path("ss-analytics/", ss_analytics, name="ss-analytics")
]