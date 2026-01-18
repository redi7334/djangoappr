from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import viewsets

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
        subject_id = request.GET.get("subject_id", None)
        # do bejm check nese ekziston subject_id
        if subject_id:
          
        #do kerkojm db per studySession me ate subject_ID
            qs = StudySession.objects.filter(subject__id=subject_id)
         #serialize the data
            serializer = StudySessionSerializer(qs, many=True)
        #return
            return Response(serializer.data)
        
    duration_minutes = request.GET.get("duration_minutes", None)
    if duration_minutes:
           qs = StudySession.objects.filter(duration_minutes__lte=duration_minutes)
           serializer = StudySessionSerializer(qs, many=True)
           return Response(serializer.data)
        
        #start_date do ta maresh si query parameter YYYY-MM--DD
        #do besh check nese ekzistojne
        #start = datetime.fromisoformat(start_date)
        #end = datetime.fromisoformat(start_date)
        #lte dhe gte per te gjetur range
        #do beni return qs
        
        
class SubjectViewset(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
    
    """
    GET drf/subjects/
    POST drf/subjects/
    
    GET drf/subjects/(id)/
    PUT drf/subjects/(id)/
    PATCH drf/subjects/(id)/
    DELEte drf/subjects/(id)/
    """
    
class StudySessionViewset(viewsets.ModelViewSet):
    queryset = StudySession.objects.all()
    serializer_class = StudySessionSerializer