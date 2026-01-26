from django.urls import path, include
from .views import test2, all_subjects, subject, study_session, study_session_list,total_time_all_subjects

from rest_framework.routers import DefaultRouter
from .views import SubjectViewset

router = DefaultRouter()
router.register(r"subjects", SubjectViewset, basename="subject")
 
urlpatterns = [
    path("test2/", test2),
    path("all-subjects/", all_subjects, name="all_subjects"),    
    path("subject/<int:numri>", subject),
    path("study-session/<int:numri>", study_session,name="study-session"),
    path("study-session-list/", study_session_list),
    path("", include(router.urls)),
    path("total-time-all-subjects/",total_time_all_subjects,name="total-time-all-subjects")
]