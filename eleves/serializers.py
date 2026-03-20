# eleves/serializers.py
from rest_framework import serializers
from .models import Classe, Matiere, Professeur, Eleve


class ClasseSerializer(serializers.ModelSerializer):
    nombre_eleves = serializers.SerializerMethodField()

    class Meta:
        model = Classe
        fields = ['id', 'nom', 'niveau', 'annee_scolaire',
                  'effectif_max', 'nombre_eleves']

    def get_nombre_eleves(self, obj):
        return obj.eleves.filter(actif=True).count()


class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = ['id', 'nom', 'code', 'coefficient', 'description']


class ProfesseurSerializer(serializers.ModelSerializer):
    matieres_detail = MatiereSerializer(source='matieres',
                                        many=True, read_only=True)

    class Meta:
        model = Professeur
        fields = ['id', 'nom', 'prenom', 'email', 'telephone',
                  'matieres', 'matieres_detail', 'date_recrutement']
        extra_kwargs = {'matieres': {'write_only': True}}


class EleveSerializer(serializers.ModelSerializer):
    classe_detail = ClasseSerializer(source='classe', read_only=True)
    classe = serializers.PrimaryKeyRelatedField(
        queryset=Classe.objects.all(), write_only=True,
        allow_null=True, required=False
    )
    age = serializers.SerializerMethodField()

    class Meta:
        model = Eleve
        fields = ['id', 'matricule', 'nom', 'prenom', 'sexe',
                  'date_naissance', 'age', 'lieu_naissance',
                  'classe', 'classe_detail', 'nom_parent',
                  'telephone_parent', 'date_inscription', 'actif']
        read_only_fields = ['date_inscription']

    def get_age(self, obj):
        from datetime import date
        today = date.today()
        age = today.year - obj.date_naissance.year
        if (today.month, today.day) < (obj.date_naissance.month,
                                        obj.date_naissance.day):
            age -= 1
        return age


class EleveListSerializer(serializers.ModelSerializer):
    classe_nom = serializers.CharField(source='classe.__str__',
                                       read_only=True)

    class Meta:
        model = Eleve
        fields = ['id', 'matricule', 'nom', 'prenom',
                  'sexe', 'classe_nom', 'actif']