
from rest_framework import serializers
from AppFeature.models import SymptomLog, WearableData, AIRecommendation

class SymptomLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomLog
        fields = '__all__'

class WearableDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WearableData
        fields = '__all__'

class AIRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRecommendation
        fields = '__all__'