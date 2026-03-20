# eleves/views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Classe, Matiere, Professeur, Eleve
from .serializers import (ClasseSerializer, MatiereSerializer,
                           ProfesseurSerializer, EleveSerializer,
                           EleveListSerializer)


class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['niveau', 'annee_scolaire']
    search_fields = ['nom', 'niveau']


class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'code']


class ProfesseurViewSet(viewsets.ModelViewSet):
    queryset = Professeur.objects.all()
    serializer_class = ProfesseurSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'prenom', 'email']


class EleveViewSet(viewsets.ModelViewSet):
    queryset = Eleve.objects.select_related('classe')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['sexe', 'classe', 'actif']
    search_fields = ['nom', 'prenom', 'matricule']
    ordering_fields = ['nom', 'prenom', 'date_inscription']
    ordering = ['nom']

    def get_serializer_class(self):
        if self.action == 'list':
            return EleveListSerializer
        return EleveSerializer