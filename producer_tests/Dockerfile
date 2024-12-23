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
EXPOSE 6001

# Commande pour démarrer l'application
CMD ["python", "producer1.py"]