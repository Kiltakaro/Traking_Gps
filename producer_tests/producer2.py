from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import time
import random


# Initialiser le producer Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # transforme en JSON
)

try:
    for i in range(30): 
        message = {'IP': 2, 'latitude': 48.8576 + (i * random.randint(1, 10)/1000), 'longitude': 2.3542 + (i * random.randint(1, 10)/1000)}
        producer.send('test_topic', message)
        producer.flush()  # S'assurer que le message est bien envoyé
        print(f"Message envoyé avec succès : {message}")
        time.sleep(8)
except KafkaError as e:
    print(f"Une erreur est survenue : {e}")
finally:
    producer.close()  # Toujours fermer le producer après utilisation