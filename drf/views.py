from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Subject, StudySession
from .serializers import SubjectSerializer, StudySessionSerializer

from .pagination import StudySessionPagination

@api_view(["GET"])
def test2(request):
    return Response({"message":"test"})

@api_view(["GET", "POST"])
def all_subjects(request):
    if request.method == "GET":
        qs = Subject.objects.all()
        serializer = SubjectSerializer(qs, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
@api_view(["GET"])
def subject(request, numri):
        subject = Subject.objects.get(id=numri)
        serializer = SubjectSerializer(subject, many=False)
        return Response(serializer.data)

@api_view(["GET"])
def study_session(request, numri):
     study_session = StudySession.objects.get(id=numri)
     serializer = StudySessionSerializer(study_session)
     return Response(serializer.data)

@api_view(["GET"])
def study_session_list(request):
    if request.method == "GET":
        ss_qs = StudySession.objects.select_related('subject').all()        
        
        paginator = StudySessionPagination()
        page = paginator.paginate_queryset(ss_qs, request)

        serializer = StudySessionSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
    return Response({"Error":"Method not allowed."})