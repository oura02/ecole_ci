# eleves/admin.py
from django.contrib import admin
from .models import Classe, Matiere, Professeur, Eleve


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ['nom', 'niveau', 'annee_scolaire', 'effectif_max']
    list_filter = ['niveau', 'annee_scolaire']
    search_fields = ['nom']


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'coefficient']
    search_fields = ['nom', 'code']


@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'email', 'telephone']
    search_fields = ['nom', 'prenom', 'email']
    filter_horizontal = ['matieres']


@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ['matricule', 'nom', 'prenom', 'sexe', 'classe', 'actif']
    list_filter = ['sexe', 'classe', 'actif']
    search_fields = ['matricule', 'nom', 'prenom']
    list_editable = ['actif']