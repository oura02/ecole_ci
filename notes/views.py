# notes/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from .models import Note, Bulletin
from .serializers import NoteSerializer, BulletinSerializer
from eleves.models import Eleve, Matiere


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.select_related('eleve', 'matiere', 'professeur')
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['trimestre', 'type_note', 'matiere', 'eleve']
    search_fields = ['eleve__nom', 'eleve__matricule', 'matiere__nom']
    ordering_fields = ['date_saisie', 'note']
    ordering = ['-date_saisie']

    # ─── Moyenne d'un élève par trimestre ──────────────────────
    @action(detail=False, methods=['get'])
    def moyenne_eleve(self, request):
        eleve_id = request.query_params.get('eleve_id')
        trimestre = request.query_params.get('trimestre')

        if not eleve_id:
            return Response(
                {"error": "Paramètre eleve_id requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        notes = Note.objects.filter(eleve_id=eleve_id)
        if trimestre:
            notes = notes.filter(trimestre=trimestre)

        resultat = notes.values('matiere__nom', 'matiere__coefficient').annotate(
            moyenne=Avg('note'),
            nombre_notes=Count('id')
        )

        # Calcul moyenne générale pondérée
        total_points = sum(
            float(r['moyenne']) * r['matiere__coefficient']
            for r in resultat if r['moyenne']
        )
        total_coefs = sum(
            r['matiere__coefficient']
            for r in resultat if r['moyenne']
        )
        moyenne_generale = round(total_points / total_coefs, 2) if total_coefs > 0 else 0

        return Response({
            "eleve_id": eleve_id,
            "trimestre": trimestre or "Tous",
            "moyennes_par_matiere": list(resultat),
            "moyenne_generale": moyenne_generale
        })

    # ─── Statistiques d'une classe ─────────────────────────────
    @action(detail=False, methods=['get'])
    def stats_classe(self, request):
        classe_id = request.query_params.get('classe_id')
        trimestre = request.query_params.get('trimestre', 1)

        if not classe_id:
            return Response(
                {"error": "Paramètre classe_id requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        notes = Note.objects.filter(
            eleve__classe_id=classe_id,
            trimestre=trimestre
        )

        stats = notes.values('matiere__nom').annotate(
            moyenne_classe=Avg('note'),
            nombre_eleves=Count('eleve', distinct=True)
        )

        return Response({
            "classe_id": classe_id,
            "trimestre": trimestre,
            "statistiques": list(stats)
        })


class BulletinViewSet(viewsets.ModelViewSet):
    queryset = Bulletin.objects.select_related('eleve', 'classe')
    serializer_class = BulletinSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['trimestre', 'annee_scolaire', 'classe']
    search_fields = ['eleve__nom', 'eleve__matricule']