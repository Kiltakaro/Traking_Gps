from kafka import KafkaProducer # type: ignore
from kafka.errors import KafkaError, KafkaTimeoutError # type: ignore
import json
import time
import os
import random

# Initialiser le producer Kafka
# laisse le temps au broker de se setup
print(f"Attend 12 secondes...")
time.sleep(12)

kafka_broker_ip = os.getenv('KAFKA_BROKER_IP', 'localhost')
try:
    producer = KafkaProducer(
        bootstrap_servers=f'{kafka_broker_ip}:9092',
        # bootstrap_servers=f'Kafka:9092', for local dev
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks='all'
    )
    print("Connexion PRODUCER réussie.")

except KafkaTimeoutError as e:
    print(f"Erreur de connexion à Kafka : {e}")
    while True:
        print("En attente de Kafka...")
        time.sleep(10)  #

try:
    lattitude = 48.8566
    longitude = 2.3522
    while True: 
        i = random.randint(0, 4)
        j = random.randint(0, 4)
        if random.random() < 0.5:
            i = -i
        if random.random() < 0.5:
            j = -j
        lattitude = lattitude + (i * 0.001)
        longitude = longitude + (j * 0.001)
        message = {'IP': 2, 'latitude': lattitude, 'longitude': longitude}
        future = producer.send('coordinates_topic', value=message)
        result = future.get(timeout=25)  # Attendre que le message soit envoyé
        print(f"Message envoyé avec succès : {message}")
        time.sleep(4)

except KafkaError as e:
    print(f"Une erreur est survenue : {e}")
finally:
    producer.close()  # Toujours fermer le producer après utilisation
