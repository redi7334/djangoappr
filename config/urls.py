from core.views import test_view, subject_list, subject

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test_view),
    path('subject-list/', subject_list),
    path('Subject/<int:numri>/', subject)

]
