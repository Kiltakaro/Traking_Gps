from kafka import KafkaConsumer
import json

# Inutile mtn

# Initialiser le consommateur Kafka
consumer = KafkaConsumer(
    'test_topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # Lire les messages depuis le début
    enable_auto_commit=True,  # Valider automatiquement les offsets
    group_id='my_consumer_group',  # Définir le groupe du consommateur
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # transformer les données en JSON
)

# Consommer les messages
for message in consumer:
    print(f"Message reçu : {message.value}")
