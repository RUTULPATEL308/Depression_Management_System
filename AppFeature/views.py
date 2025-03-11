from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from AppFeature.models import SymptomLog, WearableData, AIRecommendation
from AppFeature.serializers import WearableDataSerializer
from AppFeature.serializers import SymptomLogSerializer
from AppFeature.serializers import AIRecommendationSerializer

from django.core.files.storage import default_storage

# Create your views here.

@csrf_exempt
def SymptomLogApi(request, id=0):
    if request.method == 'GET':
        symptom_logs = SymptomLog.objects.all()
        symptom_log_serializer = SymptomLogSerializer(symptom_logs, many=True)
        return JsonResponse(symptom_log_serializer.data, safe=False)
    elif request.method == 'POST':
        symptom_log_data = JSONParser().parse(request)
        symptom_log_serializer = SymptomLogSerializer(data=symptom_log_data)
        if symptom_log_serializer.is_valid():
            symptom_log_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        symptom_log_data = JSONParser().parse(request)
        symptom_log = SymptomLog.objects.get(id=symptom_log_data['id'])
        symptom_log_serializer = SymptomLogSerializer(symptom_log, data=symptom_log_data)
        if symptom_log_serializer.is_valid():
            symptom_log_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        symptom_log = SymptomLog.objects.get(id=id)
        symptom_log.delete()
        return JsonResponse("Deleted Successfully", safe=False)

@csrf_exempt
def WearableDataApi(request, id=0):
    if request.method == 'GET':
        wearable_data = WearableData.objects.all()
        wearable_data_serializer = WearableDataSerializer(wearable_data, many=True)
        return JsonResponse(wearable_data_serializer.data, safe=False)
    elif request.method == 'POST':
        wearable_data = JSONParser().parse(request)
        wearable_data_serializer = WearableDataSerializer(data=wearable_data)
        if wearable_data_serializer.is_valid():
            wearable_data_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        wearable_data = JSONParser().parse(request)
        wearable = WearableData.objects.get(id=wearable_data['id'])
        wearable_data_serializer = WearableDataSerializer(wearable, data=wearable_data)
        if wearable_data_serializer.is_valid():
            wearable_data_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        wearable = WearableData.objects.get(id=id)
        wearable.delete()
        return JsonResponse("Deleted Successfully", safe=False)

@csrf_exempt
def AIRecommendationApi(request, id=0):
    if request.method == 'GET':
        recommendations = AIRecommendation.objects.all()
        recommendation_serializer = AIRecommendationSerializer(recommendations, many=True)
        return JsonResponse(recommendation_serializer.data, safe=False)
    elif request.method == 'POST':
        recommendation_data = JSONParser().parse(request)
        recommendation_serializer = AIRecommendationSerializer(data=recommendation_data)
        if recommendation_serializer.is_valid():
            recommendation_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        recommendation_data = JSONParser().parse(request)
        recommendation = AIRecommendation.objects.get(id=recommendation_data['id'])
        recommendation_serializer = AIRecommendationSerializer(recommendation, data=recommendation_data)
        if recommendation_serializer.is_valid():
            recommendation_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        recommendation = AIRecommendation.objects.get(id=id)
        recommendation.delete()
        return JsonResponse("Deleted Successfully", safe=False)
