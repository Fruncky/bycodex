# Formation IA

Site de démonstration pour proposer et vendre des formations en intelligence artificielle destinées aux entreprises.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # renseignez vos identifiants email
python app.py
```

## Déploiement

L'application peut être déployée sur une plateforme comme Heroku. Assurez-vous de définir les variables d'environnement indiquées dans `.env.example`.
