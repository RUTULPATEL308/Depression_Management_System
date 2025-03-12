from django.urls import re_path, include
from AppFeature import views, forms

urlpatterns = [
    re_path(r'^symptomsog$', views.SymptomLogApi),
    re_path(r'^symptomsog/([0-9]+)$', views.SymptomLogApi),
    re_path(r'^wearabledata$', views.WearableDataApi),
    re_path(r'^wearabledata/([0-9]+)$', views.WearableDataApi),
    re_path(r'^airecommendation$', views.AIRecommendationApi),
    re_path(r'^airecommendation/([0-9]+)$', views.AIRecommendationApi),
]
