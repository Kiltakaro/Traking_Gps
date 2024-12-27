import asyncio
import logging
from fastapi import FastAPI, WebSocket, Request # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from kafka import KafkaConsumer # type: ignore
import json
import threading
import psycopg2 # type: ignore
import time 


# Attend que le broker soit allumé
time.sleep(6)

# Configuration de base du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

##### Configuration CORS
# Obligé SINON ça fonctionne pas
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
#####

##### Initialiser le consommateur Kafka
KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "coordinates_topic"

##### Connexion à postgresql db
db_connection = psycopg2.connect(
    host="database",
    user="user",
    password="password",
    dbname="gpsDb"
)

cursor = db_connection.cursor()

app = FastAPI()

# Monter le répertoire de fichiers statiques pour avoir le front
app.mount("/static", StaticFiles(directory="Front"), name="static")
templates = Jinja2Templates(directory="Front")


@app.get('/')
def index(request: Request):
    """
    Page principale de l'appli de tracking gps
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/hello")
async def root():
    """
    Pour tester l'appli si erreur sur la page root
    """
    return {"message": "Hello world ça marche"}

def consume_messages(consumer_group):
    """
    Consomme les messages de Kafka et les stocke dans la bdd mysql.
     Parameters:
    - consumer_groupe: group_ip pour le broker kafka
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

        except psycopg2.Error as err:
            logging.error(f"Erreur SQL: {err}")
        except Exception as e:
            logging.error(f"Erreur: {e}")


#### Setup thread consommer broker 
consumer_thread = threading.Thread(target=consume_messages, args=('fastapi_consumer_group',), daemon=True)
consumer_thread.start()


@app.get("/messages")
async def get_messages():
    """
    Récupère tous les messages consommés.
    """
    cursor.execute("SELECT * FROM Coordinates ORDER BY messageDate DESC")
    messages = cursor.fetchall()

    if not messages:
        return {"message": "Aucun message disponible."}

    return [
        {
            "id": msg[0],
            "IP": msg[1],
            "latitude": msg[2],
            "longitude": msg[3],
            "messageDate": msg[4].isoformat()
        }
        for msg in messages
    ]
    # pass


@app.get("/messages/IP1")
async def get_messages_IP1():
    """
    Récupère tous les messages consommés d'IP1.
    """

    ip = 1
    cursor.execute("SELECT * FROM Coordinates WHERE IP = %s ORDER BY messageDate DESC", (ip,))
    messages = cursor.fetchall()


    if not messages:
        return {"message": "Aucun message disponible."}

    return [
        {
            "id": msg[0],
            "IP": msg[1],
            "latitude": msg[2],
            "longitude": msg[3],
            "messageDate": msg[4].isoformat()
        }
        for msg in messages
    ]


@app.get("/messages/IP2")
async def get_messages_IP2():
    """
    Récupère tous les messages consommés d'IP2.
    """
    
    ip = 2
    cursor.execute("SELECT * FROM Coordinates WHERE IP = %s ORDER BY messageDate DESC", (ip,))
    messages = cursor.fetchall()


    if not messages:
        return {"message": "Aucun message disponible."}

    return [
        {
            "id": msg[0],
            "IP": msg[1],
            "latitude": msg[2],
            "longitude": msg[3],
            "messageDate": msg[4].isoformat()
        }
        for msg in messages
    ]


@app.get("/messages/IP1/last")
async def get_last_message_IP1():
    """
    Récupère le dernier message d'IP1 consommé.
    """
    cursor.execute("SELECT * FROM Coordinates ORDER BY messageDate DESC LIMIT 1")
    last_msg = cursor.fetchone()

    if not last_msg:
        return {"message": "Aucun message disponible."}
    
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
        return {"message": "Aucun message disponible."}
    
    return {
        "id": last_msg[0],
        "IP": last_msg[1],
        "latitude": last_msg[2],
        "longitude": last_msg[3],
        "messageDate": last_msg[4].isoformat()  # Convertir datetime en string
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Ouvre un websocket avec le frontend pour lui donner les dernières coordonnées GPS
    """
    
    await websocket.accept()
    while True:

        ip = 1
        cursor.execute("SELECT * FROM Coordinates WHERE IP = %s ORDER BY messageDate DESC LIMIT 1", (ip,))
        last_msg1 = cursor.fetchone()

        ip = 2
        cursor.execute("SELECT * FROM Coordinates WHERE IP = %s ORDER BY messageDate DESC LIMIT 1", (ip,))
        last_msg2 = cursor.fetchone()

        try:
            # CASE IP1 + IP2 ont des msg
            if last_msg1 and last_msg2:
                message = {
                    "IP1": last_msg1[1],
                    "latitudeIP1": last_msg1[2],
                    "longitudeIP1": last_msg1[3],
                    "messageDateIP1": last_msg1[4].isoformat(),
                    "IP2": last_msg2[1],
                    "latitudeIP2": last_msg2[2],
                    "longitudeIP2": last_msg2[3],
                    "messageDateIP2": last_msg2[4].isoformat()
                }
                print("Les 2 msg sont la")
                await websocket.send_json(message) # A FACTORISER

            # CASE IP1 A DES MSG MAIS PAS IP2 
            elif last_msg1 and not last_msg2:
                message = {
                    "IP1": last_msg1[1],
                    "latitudeIP1": last_msg1[2],
                    "longitudeIP1": last_msg1[3],
                    "messageDateIP1": last_msg1[4].isoformat(),
                    "IP2": None,
                    "latitudeIP2": None,
                    "longitudeIP2": None,
                    "messageDateIP2": None
                }
                print("Seul IP1 msg sont la")
                await websocket.send_json(message) # A FACTORISER

            # CASE IP1 A 0 MSG MAIS IP2 SI
            elif not last_msg1 and last_msg2:
                message = {
                    "IP1": None,
                    "latitudeIP1": None,
                    "longitudeIP1": None,
                    "messageDateIP1": None,
                    "IP2": last_msg2[1],
                    "latitudeIP2": last_msg2[2],
                    "longitudeIP2": last_msg2[3],
                    "messageDateIP2": last_msg2[4].isoformat()
                }
                print("Seul IP2 msg sont la")
                await websocket.send_json(message) # A FACTORISER

            else : 
                print("pas de msg")
        
        except psycopg2.Error as err:
            logging.error(f"Erreur SQL: {err}")

        except Exception as e:
            logging.error(f"Erreur: {e}")

        await asyncio.sleep(4)  # Verifier s'il y a du nouveau toutes les 4 secondes