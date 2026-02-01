from rest_framework.decorators import api_view
from adrf.decorators import api_view as async_api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import viewsets
from django.db.models import Sum

from core.models import Subject, StudySession
from .serializers import SubjectSerializer, StudySessionSerializer

from .pagination import StudySessionPagination

from adrf.views import APIView
from asgiref.sync import sync_to_async

@api_view(["GET"])
def test2(request):
    return Response({"message":"test"})

class SubjectListAsync(APIView):
    """
    Async Class-based view for Subject list and creation.
    """
    async def get(self, request):
        qs = Subject.objects.all()
        data = []
        async for subject in qs:
            data.append(SubjectSerializer(subject).data)
        return Response(data)        

    async def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            await sync_to_async(serializer.save)()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@async_api_view(["GET"])
async def subject(request, numri):
        subject = await Subject.objects.aget(id=numri)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

@async_api_view(["GET"])
async def study_session(request, numri):
     study_session = await StudySession.objects.aget(id=numri)
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
        #start_date, end_date do ta maresh si query parameter YYYY-MM--DD
        #do besh check nese ekzistojne
        #start = datetime.fromisoformat(start_date)
        #end = datetime.fromisoformat(start_date)
        #lte dhe gte per te gjetur range
        #do beni return qs
        
        # dsh shtojini pagination
        # implementoni ordering(sipas dates) acending edhe descending
        
    ordering = request.GET.get("ordering", None)
    if ordering:
        if ordering.startswith("-"):
            try:
                date_obj = datetime.fromisoformat(ordering[1:])
            except ValueError:
                return Response({"error":"Invalid string"})
            qs = StudySession.objects.all().filter(datetime__lte=date_obj).order_by("-datetime")
            serializer = StudySessionSerializer(qs, many=True)
            return Response(serializer.data)
        else:
            try:
                date_obj = datetime.fromisoformat(ordering)
            except ValueError:
                return Response({"error":"Invalid string"})
            qs = StudySession.objects.all().filter(datetime__gte=date_obj).order_by("datetime")
            serializer = StudySessionSerializer(qs, many=True)
            return Response(serializer.data)
        #EXTRA
        #Perpiquni ta beni me nje query parameter, maybe nje string=- YYYY-MM-DD
        #.startswith("-") string slicing
        
class TotalTimeAllSubjectsAsync(APIView):
    """
    Async Class-based view for calculating total time per subject.
    """
    async def get(self, request):
        # Annotate each subject with the total duration of its study sessions
        subject_qs = Subject.objects.annotate(
            total_time=Sum('studysession__duration_minutes')
        ).values('id', 'total_time')
        
        list1 = []
        async for subject in subject_qs:
            dict1 = {"id": subject["id"], "Total Time": subject["total_time"] or 0}
            list1.append(dict1)
            
        return Response(list1)

                
class SubjectViewset(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
    """
    
    GET drf/subjects/
    POST drf/subjects/
    
    GET drf/subjects/(id)/ PUT drf/subjects/(id)/
    PATCH drf/subjects/(id)/
    DELEte drf/subjects/(id)/

    """
