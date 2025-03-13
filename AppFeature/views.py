from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth import logout

from AppFeature.models import SymptomLog, WearableData, AIRecommendation
from AppFeature.serializers import WearableDataSerializer
from AppFeature.serializers import SymptomLogSerializer
from AppFeature.serializers import AIRecommendationSerializer
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import default_storage
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

from .forms import RegistrationForm,AppointmentForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .models import BookAppointment

@login_required(login_url='login')
def appointments(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Assign logged-in user
            appointment.save()
            return redirect('/dashboard')
    else:
        form = AppointmentForm()
    #user_appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointments.html',{'form': form})

@login_required(login_url='login')
def submit_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            Sappointment = form.save(commit=False)
            Sappointment.user = request.user
            Sappointment.save()
            return redirect('/dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'appointments.html', {'form': form})

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



def home(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def assessment(request):
    return render(request, 'assessment.html')


def registration(request):
    if request.method == "POST":
        
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Change to your login page name
    else:
        form = RegistrationForm()  # Display empty form

    return render(request, 'registration.html', {'form': form})

def loginPage(request):
    if request.method == 'POST':
            # Authenticate and login the user
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect to home or any page after login
            
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')  # Change to your login page name

@login_required(login_url='login')
def book_appointment(request):
    if request.method == 'POST':
            # Assuming you have an AppointmentForm to handle appointment submissions
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments')  # Redirect to the appointments page
        else:
            form = AppointmentForm()  # Display empty form

        return render(request, 'book_appointment.html', {'form': form})

@login_required(login_url='login')
def viewAppointment(request):
        # Assuming you have an Appointment model to list appointments
    Vappointments = Appointment.objects.filter(user=request.user)
    return render(request, 'viewAppointment.html', {'appointments': Vappointments})
