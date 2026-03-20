# eleves/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClasseViewSet, MatiereViewSet, ProfesseurViewSet, EleveViewSet

router = DefaultRouter()
router.register(r'classes', ClasseViewSet, basename='classe')
router.register(r'matieres', MatiereViewSet, basename='matiere')
router.register(r'professeurs', ProfesseurViewSet, basename='professeur')
router.register(r'eleves', EleveViewSet, basename='eleve')

urlpatterns = [
    path('', include(router.urls)),
]