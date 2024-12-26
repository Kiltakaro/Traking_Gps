from kafka import KafkaProducer # type: ignore
from kafka.errors import KafkaError, KafkaTimeoutError # type: ignore
import json
import time
import os

# Initialiser le producer Kafka
print(f"test print")
time.sleep(12)

kafka_broker_ip = os.getenv('KAFKA_BROKER_IP', 'localhost')
try:
    producer = KafkaProducer(
        bootstrap_servers=f'{kafka_broker_ip}:9092',
        # bootstrap_servers=f'Kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks='all'
    )
    print("Connexion PRODUCER réussie.")
    # Envoyer des messages comme avant
except KafkaTimeoutError as e:
    print(f"Erreur de connexion à Kafka : {e}")
    while True:
        print("En attente de Kafka...")
        time.sleep(10)  #

try:
    for i in range(10): 
        message = {'IP': 2, 'latitude': 48.8566 + (i * 0.001), 'longitude': 2.3522 + (i * 0.001)}
        future = producer.send('coordinates_topic', value=message)
        result = future.get(timeout=25)  # Attendre que le message soit envoyé
        print(f"Message envoyé avec succès : {message}")
        time.sleep(10)

except KafkaError as e:
    print(f"Une erreur est survenue : {e}")
finally:
    producer.close()  # Toujours fermer le producer après utilisation
