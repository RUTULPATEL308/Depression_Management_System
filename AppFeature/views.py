import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import joblib
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
from rest_framework.decorators import api_view
from django.contrib import messages
from .forms import EmailOrUsernameLoginForm
from django.utils.timezone import is_naive, make_aware, get_current_timezone

from .forms import RegistrationForm,AppointmentForm, MentalHealthAssessmentForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .models import BookAppointment, MentalHealthAssessment
from .ai_model import get_ai_recommendation  # Import AI function


@login_required(login_url='login')
def appointments(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user  # Assign logged-in user
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
            Sappointment.patient_id = request.user
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
    # mood_history = MentalHealthAssessment.objects.all()
    mood_history = MentalHealthAssessment.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'mood_history': mood_history})

@login_required(login_url='login')
def assessment(request):
    return render(request, 'assessment.html')


def registration(request):
    if request.method == "POST":
        try:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Registration successful. You can now log in.")  # Success message
                return redirect('login')  # Change to your login page name
            else:
                messages.error(request, "Please correct the errors below.")
        except Exception as e:
            return render(request, 'registration.html', {'error': f'An error occurred: {str(e)}'})  # Error message for invalid form
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect after login

    if request.method == "POST":
        form = EmailOrUsernameLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username/email or password.")
    else:
        form = EmailOrUsernameLoginForm()

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')  # Change to your login page name


@login_required(login_url='login')
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.id  # ✅ Assign logged-in user ID

            # Timezone-aware fix
            if appointment.appointment_date and is_naive(appointment.appointment_date):
                appointment.appointment_date = make_aware(
                    appointment.appointment_date, timezone=get_current_timezone()
                )
            appointment.save()
            print("Appointment saved for:", appointment.patient)
            return redirect('dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'appointments.html', {'form': form})


@login_required(login_url='login')
def viewAppointment(request):
        # Assuming you have an Appointment model to list appointments
    # Vappointments = Appointment.objects.filter(user=request.user)
    return render(request, 'viewAppointment.html')



@api_view(["POST"])
def ai_recommendation(request):
    """
    API endpoint to get AI-generated mental health recommendations.
    """
    try:
        user_data = request.data  # Get user input from request
        recommendation = get_ai_recommendation(user_data)
        return JsonResponse({"recommendation": recommendation}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

from django.shortcuts import render
from .forms import MentalHealthAssessmentForm
from .models import MentalHealthAssessment
from .ai_model import get_ai_recommendation  # Import AI function
# Load the trained model and encoders

@login_required(login_url='login')
def mental_health_assessment(request):
    if request.method == "POST":
        form = MentalHealthAssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.user = request.user  # Assign the logged-in user

            # Prepare user data for AI model
            user_data = {
                "mood_level": assessment.mood_level,
                "sleep_hours": assessment.sleep_hours,
                "sleep_quality": assessment.sleep_quality,
                "interest_in_activities": assessment.interest_in_activities,
                "suicidal_thoughts": assessment.suicidal_thoughts,
                "emotional_state": assessment.emotional_state,
                "appetite_changes": assessment.appetite_changes,
                "energy_levels": assessment.energy_levels,
                "social_engagement": assessment.social_engagement,
            }

            # Get AI-generated recommendations
            recommendations = get_ai_recommendation(user_data)
            
            if isinstance(recommendations, list):
                recommendations = " ".join(recommendations)  # Convert list to a single string
                recommendations = recommendations.strip()
            
            # Book recommendations based on emotional state
            book_recommendations = {
                "Sad": ("The Happiness Project", "https://pdfcoffee.com/the-happiness-project-gretchen-rubin-pdf-free.html"),
                "Anxious": ("The Anxiety and Phobia Workbook", "https://www.aspirecounselingsolutions.com/storage/app/media/Resources/Self-Talk.pdf"),
                "Stressed": ("Burnout: The Secret to Unlocking the Stress Cycle", "https://irp.cdn-website.com/54bb561b/files/uploaded/Burnout%20The%20Secret%20to%20Unlocking%20the%20Stress%20Cycle.pdf"),
                "Calm": ("The Power of Now", "https://ia601000.us.archive.org/33/items/ThePowerOfNowEckhartTolle_201806/The%20Power%20Of%20Now%20-%20Eckhart%20Tolle.pdf"),
                "Depressed": ("Feeling Good: The New Mood Therapy", "https://feelinggood.com/wp-content/uploads/2021/12/AAA-Exploring-the-Daily-Mood-Log.pdf"),
                "Happy": ("The Book of Joy", "https://drnishikantjha.com/papersCollection/The%20Book%20of%20Joy,%20.pdf"),
            }

            book_title, book_link = book_recommendations.get(user_data["emotional_state"], ("Mindfulness in Plain English", "https://www.amazon.com/dp/0861719069"))
            
            # Store recommendations in the assessment model
            assessment.recommendation = recommendations
            assessment.book_title = book_title
            assessment.book_link = book_link
            assessment.save()

            return render(request, "mental_health_result.html", {
                "assessment": assessment,
                "recommendations": recommendations.get('AI_Recommendation', 'No recommendation available'),
                "book_title": book_title,
                "book_link": book_link
            })
    else:
        form = MentalHealthAssessmentForm()

    return render(request, "mental_health_assessment.html", {"form": form})

@login_required(login_url='login')
def view_appointments(request):
    """
    View to display the most recent booked appointment for the logged-in user.
    """
    if request.user.is_authenticated:
        last_appointment = BookAppointment.objects.filter(patient_id=request.user).order_by('-id').first()
        return render(request, 'viewAppointment.html', {'appointment': last_appointment})
    else:
        return redirect('login')  # Redirect to login if user is not authenticated

def books(request):
    return render(request, 'books.html')