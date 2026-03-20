# notes/serializers.py
from rest_framework import serializers
from .models import Note, Bulletin
from eleves.serializers import EleveListSerializer, MatiereSerializer


class NoteSerializer(serializers.ModelSerializer):
    eleve_detail = EleveListSerializer(source='eleve', read_only=True)
    matiere_detail = MatiereSerializer(source='matiere', read_only=True)
    eleve = serializers.PrimaryKeyRelatedField(
        queryset=__import__('eleves.models', fromlist=['Eleve']).Eleve.objects.all(),
        write_only=True
    )
    matiere = serializers.PrimaryKeyRelatedField(
        queryset=__import__('eleves.models', fromlist=['Matiere']).Matiere.objects.all(),
        write_only=True
    )
    professeur = serializers.PrimaryKeyRelatedField(
        queryset=__import__('eleves.models', fromlist=['Professeur']).Professeur.objects.all(),
        write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Note
        fields = ['id', 'eleve', 'eleve_detail', 'matiere',
                  'matiere_detail', 'professeur', 'note',
                  'trimestre', 'type_note', 'commentaire', 'date_saisie']
        read_only_fields = ['date_saisie']

    def validate_note(self, value):
        if value < 0 or value > 20:
            raise serializers.ValidationError(
                "La note doit être entre 0 et 20."
            )
        return value


class BulletinSerializer(serializers.ModelSerializer):
    eleve_detail = EleveListSerializer(source='eleve', read_only=True)

    class Meta:
        model = Bulletin
        fields = ['id', 'eleve', 'eleve_detail', 'classe',
                  'trimestre', 'annee_scolaire', 'moyenne_generale',
                  'rang', 'appreciation', 'date_generation']
        read_only_fields = ['date_generation']