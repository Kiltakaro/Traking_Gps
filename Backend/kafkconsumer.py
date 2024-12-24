from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import time

# inutile mtn

print("Test print")
print("Init consommateur Kafka")

# Initialiser le consommateur Kafka
try:
    time.sleep(8)
    consumer = KafkaConsumer(
        'test_topic',
        bootstrap_servers=['kafka:9092'],  # Utiliser le nom du service Kafka défini dans docker-compose
        auto_offset_reset='earliest',  # Lire les messages depuis le début
        # auto_offset_reset='latest',  # Lire les nouveaux msg
        enable_auto_commit=True,  # Valider automatiquement les offsets
        group_id='my_consumer_group',  # Définir le groupe du consommateur
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # transformer les données en JSON
    )
    print("Connexion CONSUMER réussie.")
except KafkaError as e:
    print(f"Erreur de connexion à Kafka : {e}")
    while True:
        print("En attente de Kafka...")
        time.sleep(10)

# Consommer les messages
print("Début de la consommation")
for message in consumer:
    print(f"Message reçu : {message.value}")