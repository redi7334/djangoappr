from rest_framework.decorators import api_view
from adrf.decorators import api_view as async_api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import viewsets
from django.db.models import Sum
import pandas as pd
from core.models import Subject, StudySession
from .serializers import SubjectSerializer, StudySessionSerializer

from .pagination import StudySessionPagination
from adrf.views import APIView

import requests

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
        # Do bejm check nese ekziston subject_id
        if subject_id:
            # Do kerkojm db per studySession me ate subject_id
            qs = StudySession.objects.filter(subject__id=subject_id)
            # Serialize the data
            serializer = StudySessionSerializer(qs, many=True)
            # return
            return Response(serializer.data)
        duration_minutes = request.GET.get("duration_minutes", None)
        if duration_minutes:
            qs = StudySession.objects.filter(duration_minutes__lte=duration_minutes)
            serializer = StudySessionSerializer(qs, many=True)
            return Response(serializer.data)
        # start_date, end_date do ta marresh si query parameter YYYY-MM-DD
        # do besh check nese ekzistojne
        # start = datetime.fromisoformat(start_date) 
        # end = datetime.fromisoformat(start_date) 
        # lte dhe gte per te gjetur range 
        # Do beni return qs

        # DSH Shtojini pagination
        # DSH 
        # Implementoni ordering (sipas dates) acending edhe descending
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
        # EXTRA:
        # Perpiquni ta beni me nje query parameter, maybe nje string=-YYYY-MM-DD
        # .startswith("-") string slicing

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

class SubjectViewSet(viewsets.ModelViewSet):
     queryset = Subject.objects.all()
     serializer_class = SubjectSerializer

     """
     GET drf/subjects/
     POST drf/subjects/

     GET drf/subjects/{id}/
     PUT drf/subjects/{id}/
     PATCH drf/subjects/{id}/
     DELETE drf/subjects/{id}/
     """

class TotalTimeAllSubjectsAsync(APIView):
    async def get(self, request):
        if request.method == "GET":
            subject_qs = Subject.objects.all()
            list1=[]
            async for subject in subject_qs:
                study_sessions = StudySession.objects.filter(subject=subject)
                total_time = 0
                async for session in study_sessions:
                    total_time += session.duration_minutes
                dict1 = {"id":subject.id,"Total Time":total_time}
                list1.append(dict1)
            return Response(list1)

@api_view(["GET"])
def total_time_all_subjects(request):
    ...

@api_view(["POST"])
def third_party_api(request):
    if request.method == "POST":
        name = request.data.get("name")
        
        response = requests.get(
            "https://api.agify.io/",
            params={"name":name},
            timeout=10)

        # {"count":50651,"name":"matt","age":54}
        description = f'count: {response.json()["count"]}, age: {response.json()["age"]}'
        subject = Subject.objects.create(name=name, description=description)

        serializer = SubjectSerializer(subject, many=False)
        return Response(serializer.data)
    
    """
    New view qe ben return:
    {
        "total_sessions":0,
        "total_minutes":0,
        "average_session_minutes":0,
        "sessions_per_day":{
            "2026-01-01":0,
            "2026-02-01":0
        }
    }
    """

@api_view(["GET"])
def ss_analytics(request):

    qs = StudySession.objects.all().values(
            "id",
            "datetime",
            "duration_minutes",
        )

    if not qs.exists():
        return Response("No Study Sessions Found")
    
    # Convert queryset → DataFrame
    df = pd.DataFrame.from_records(qs)

    """
    id      datetime     duration_minutes 
    1       2023-01-12      60  
    3       2028-02-12      50           
    """
    total_sessions = len(df)
    total_minutes = df["duration_minutes"].sum()
    average_session_minutes = df["duration_minutes"].mean()
    breakpoint()
    df["day"] = str(pd.to_datetime(df["datetime"]).dt.date)
    sessions_per_day = (
        df.groupby("day").size().astype(int).to_dict()
    )
    #.size().astype(int).to_dict()
    return Response(
        {
        "total_sessions":total_sessions,
        "total_minutes":total_minutes,
        "average_session_minutes":average_session_minutes,
        "sessions_per_day":sessions_per_day
    }
    )