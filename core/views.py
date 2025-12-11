from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Subject
import json

def test_view(request):
    return JsonResponse({"message":"view is working."})

def subject_list(request):
    if request.method == "GET":
        subject_qs = Subject.objects.all().values("id", "name", "description")
        subjects = list(subject_qs)
        return JsonResponse(subjects, safe=False)
    return JsonResponse({"Error":"Method not allowed."})

@csrf_exempt
def subject(request, numri):
    if request.method == "GET":
        subject = Subject.objects.get(id=numri)

        subject_dict = {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description
        }

        return JsonResponse(subject_dict, safe=False)
    if request.method == "POST":
        # Duhen marre te dhenat nga requesti
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        name = data.get("name")
        description = data.get("description", "")

        # Duhet krijuar objekti ne db
        subject = Subject.objects.create(name=name, description=description)

        # Dergo mesazh suksesi
        return JsonResponse({"message":"Subject was created succesfully"})
    
    if request.method == "PATCH":
        ...
        # Marrim te dhenat nga requesti (id, name, description)

        # Duhet marr objekti nga db me id
        # Duhet ndryshuar name dhe description
        # Duhet ber save objekti ne db

        # return successful message, Old dhe new


    return JsonResponse({"Error":"Method not allowed."})