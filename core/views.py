from django.shortcuts import render
from django.http import JsonResponse
from .models import Subject

# Create your views here.

def test_view(request):
    return JsonResponse({"message":"View is working"})

def subject_list(request):
    if request.method == "GET":
        subject_qs = Subject.objects.all().values("id", "name", "description")
        subjects = list(subject_qs)
        return JsonResponse(subjects, safe=False)
    return JsonResponse({"Error":" Method not allowed."})

def subject(request, numri):
    if request.method == "GET":
        subject = Subject.objects.get(id=numri)
        
        subject_dict = {
            "id": subject.id,
            "name": subject.name,
            "description": subject.discription
        }
        return JsonResponse(subjects, safe=False)
    return JsonResponse({"Error":" Method not allowed."})
