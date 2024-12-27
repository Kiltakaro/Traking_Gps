FROM python:3.11-slim

COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

