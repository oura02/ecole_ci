# notes/models.py
from django.db import models
from eleves.models import Eleve, Matiere, Classe, Professeur


class Note(models.Model):
    TRIMESTRE_CHOICES = [
        (1, 'Premier trimestre'),
        (2, 'Deuxième trimestre'),
        (3, 'Troisième trimestre'),
    ]

    TYPE_CHOICES = [
        ('devoir', 'Devoir'),
        ('composition', 'Composition'),
        ('interrogation', 'Interrogation'),
    ]

    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE,
                              related_name='notes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE,
                                related_name='notes')
    professeur = models.ForeignKey(Professeur, on_delete=models.SET_NULL,
                                   null=True, related_name='notes')
    note = models.DecimalField(max_digits=4, decimal_places=2)
    trimestre = models.IntegerField(choices=TRIMESTRE_CHOICES)
    type_note = models.CharField(max_length=15, choices=TYPE_CHOICES,
                                 default='devoir')
    commentaire = models.TextField(blank=True)
    date_saisie = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.eleve} - {self.matiere} - {self.note}/20"

    class Meta:
        ordering = ['-date_saisie']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'


class Bulletin(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE,
                              related_name='bulletins')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    trimestre = models.IntegerField(choices=Note.TRIMESTRE_CHOICES)
    annee_scolaire = models.CharField(max_length=10, default='2025-2026')
    moyenne_generale = models.DecimalField(max_digits=4, decimal_places=2,
                                           null=True, blank=True)
    rang = models.IntegerField(null=True, blank=True)
    appreciation = models.TextField(blank=True)
    date_generation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bulletin {self.eleve} - T{self.trimestre} {self.annee_scolaire}"

    class Meta:
        ordering = ['-date_generation']
        unique_together = ['eleve', 'trimestre', 'annee_scolaire']
        verbose_name = 'Bulletin'
        verbose_name_plural = 'Bulletins'