# notes/admin.py
from django.contrib import admin
from .models import Note, Bulletin


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['eleve', 'matiere', 'note', 'trimestre',
                    'type_note', 'date_saisie']
    list_filter = ['trimestre', 'type_note', 'matiere']
    search_fields = ['eleve__nom', 'eleve__matricule']


@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ['eleve', 'classe', 'trimestre',
                    'moyenne_generale', 'rang', 'annee_scolaire']
    list_filter = ['trimestre', 'annee_scolaire']
    search_fields = ['eleve__nom', 'eleve__matricule']