# Utiliser une image Python officielle légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier requirements et installer les dépendances (production only, tests excluded)
COPY requirements-prod.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-prod.txt

# Copier le code source (tests excluded via .dockerignore)
COPY ./src ./src

# Exposer le port de l'application
EXPOSE 8000

# Commande pour lancer l'application FastAPI avec Uvicorn
CMD ["uvicorn", "src.presentation.api.main_api:app", "--host", "0.0.0.0", "--port", "8000"]
