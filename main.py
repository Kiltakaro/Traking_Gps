import logging
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaConsumer
import json
from typing import List
import mysql.connector
import threading


# Configuration de base du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Configuration CORS
# OBLIGé SINON ça fonctionne pas
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500",
    "null"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
####

# Initialiser le consommateur Kafka
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "test_topic"


# Connexion à la base de données MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpassword",
    database="Kafka_db"
)

cursor = db_connection.cursor()

@app.get("/")
async def root():
    return {"message": "Hello world"}

#commenter sur la variable
def consume_messages(consumer_group):
    """
    Consomme les messages de Kafka et les stocke dans la bdd mysql.
    """
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=consumer_group,  # ajout de variable pour lire IP1 ou IP2 avec les thread
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    for message in consumer:
        logging.info(f"Message reçu : {message.value}")

        try:
            sql = "INSERT INTO Coordinates (IP, latitude, longitude, messageDate) VALUES (%s, %s, %s, NOW())"
            val = (message.value['IP'], message.value['latitude'], message.value['longitude'])
            cursor.execute(sql, val)
            db_connection.commit()
            logging.info(f"{cursor.rowcount} record inserted")
        except mysql.connector.Error as err:
            logging.error(f"Erreur MySQL: {err}")
        except Exception as e:
            logging.error(f"Erreur: {e}")

# DEPRECIATED a refaire mais pour ce qu'onn fait ça suffira
# Peut etre dupliquer le thread pour consumer 2 
@app.on_event("startup")
async def startup_event():
    """
    Démarre la consommation des messages Kafka au démarrage de l'application.
    """
    consumer_thread = threading.Thread(target=consume_messages, args=('fastapi_consumer_group',), daemon=True)
    consumer_thread.start()
    # consumer_thread1 = threading.Thread(target=consume_messages, args=('fastapi_consumer_group_1',), daemon=True)
    # consumer_thread1.start()

    # consumer_thread2 = threading.Thread(target=consume_messages, args=('fastapi_consumer_group_2',), daemon=True)
    # consumer_thread2.start()


# A FAIRE SI NECESSAIRE
@app.get("/messages")
async def get_messages():
    """
    Récupère tous les messages consommés.
    """
    pass



# A dedoubler sur 2 threads pour faire IP1 et IP2 en meme temps ? 
@app.get("/messages/IP1/last")
async def get_last_message_IP1():
    """
    Récupère le dernier message d'IP1 consommé.
    """
    cursor.execute("SELECT * FROM Coordinates ORDER BY messageDate DESC LIMIT 1")
    last_msg = cursor.fetchone()

    if not last_msg:
        logging.info("Aucun message disponible.")
        return {"message": "Aucun message disponible."}
    
    # logging.info(f"Dernier message : {last_msg}")
    # return {last_msg}
    return {
        "id": last_msg[0],
        "IP": last_msg[1],
        "latitude": last_msg[2],
        "longitude": last_msg[3],
        "messageDate": last_msg[4].isoformat()  # Convertir datetime en string
    }


@app.get("/messages/IP2/last")
async def get_last_message_IP2():
    """
    Récupère le dernier message d'IP2 consommé.
    """
    ip = 2
    cursor.execute("SELECT * FROM Coordinates WHERE IP = %s ORDER BY messageDate DESC LIMIT 1", (ip,))
    last_msg = cursor.fetchone()

    if not last_msg:
        logging.info("Aucun message disponible.")
        return {"message": "Aucun message disponible."}
    
    # logging.info(f"Dernier message : {last_msg}")
    return {
        "id": last_msg[0],
        "IP": last_msg[1],
        "latitude": last_msg[2],
        "longitude": last_msg[3],
        "messageDate": last_msg[4].isoformat()  # Convertir datetime en string
    }


# https://fastapi.tiangolo.com/advanced/websockets/#in-production

