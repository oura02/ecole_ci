# ecole_ci
Système de gestion scolaire pour la Côte d'Ivoire — élèves, notes, bulletins — Django REST API

## Technologies
- Python 3.12 / Django 6.0
- Django REST Framework
- JWT Authentication
- SQLite

## Fonctionnalités
- Gestion des élèves et classes
- Gestion des matières et professeurs
- Saisie des notes par trimestre
- Calcul automatique des moyennes pondérées
- Génération des bulletins
- API REST complète avec filtrage et recherche

## Installation
git clone https://github.com/oura02/ecole_ci.git
cd ecole_ci
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## Endpoints API
- GET/POST /api/eleves/eleves/
- GET/POST /api/eleves/classes/
- GET/POST /api/eleves/matieres/
- GET/POST /api/notes/notes/
- GET /api/notes/notes/moyenne_eleve/?eleve_id=1
- GET /api/notes/notes/stats_classe/?classe_id=1
- POST /api/token/

## Auteur
KONAN ROMEO OURA
Développeur Django Freelance — Abidjan, Côte d'Ivoire
Volontaire DjangoCon Europe 2026 — Athènes, Grèce
