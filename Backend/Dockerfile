FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copy le fichier requirements.txt dans le workdir
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# faudra peut etre RAJOTUER DE QUOI COPIER LE FRONT 
COPY . /app

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 8000

# Commande pour démarrer l'application
# a tester sinon "fastapi dev main.py"
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["python", "kafkconsumer.py"]