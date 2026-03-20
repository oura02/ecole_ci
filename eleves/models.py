# eleves/models.py
from django.db import models


class Classe(models.Model):
    NIVEAU_CHOICES = [
        ('CP1', 'CP1'), ('CP2', 'CP2'),
        ('CE1', 'CE1'), ('CE2', 'CE2'),
        ('CM1', 'CM1'), ('CM2', 'CM2'),
        ('6eme', '6ème'), ('5eme', '5ème'),
        ('4eme', '4ème'), ('3eme', '3ème'),
        ('2nde', '2nde'), ('1ere', '1ère'),
        ('Tle', 'Terminale'),
    ]

    nom = models.CharField(max_length=50)
    niveau = models.CharField(max_length=10, choices=NIVEAU_CHOICES)
    annee_scolaire = models.CharField(max_length=10, default='2025-2026')
    effectif_max = models.IntegerField(default=45)

    def __str__(self):
        return f"{self.nom} - {self.niveau} ({self.annee_scolaire})"

    class Meta:
        ordering = ['niveau', 'nom']
        verbose_name = 'Classe'
        verbose_name_plural = 'Classes'


class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    coefficient = models.IntegerField(default=1)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nom} (coef. {self.coefficient})"

    class Meta:
        ordering = ['nom']
        verbose_name = 'Matière'
        verbose_name_plural = 'Matières'


class Professeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    matieres = models.ManyToManyField(Matiere, related_name='professeurs')
    date_recrutement = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        ordering = ['nom']
        verbose_name = 'Professeur'
        verbose_name_plural = 'Professeurs'


class Eleve(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100, blank=True)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL,
                               null=True, related_name='eleves')
    nom_parent = models.CharField(max_length=200, blank=True)
    telephone_parent = models.CharField(max_length=20, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.matricule} - {self.prenom} {self.nom}"

    class Meta:
        ordering = ['nom', 'prenom']
        verbose_name = 'Élève'
        verbose_name_plural = 'Élèves'