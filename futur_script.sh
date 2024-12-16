
# pip install mysql-connector-python fastapi uvicorn kafka-python pymysql sqlalchemy psycopg2 

# identifiants
root rootpassword

# rappels bdd
mysql -u root -p
SHOW databases;
USE Kafka_db;
DESCRIBE Coordiantes;
SELECT * FROM Coordinates;

kafka_2.13-3.9.0/bin/kafka-storage.sh format \
    --config kafka_2.13-3.9.0/config/kraft/server.properties \
    --cluster-id $(kafka_2.13-3.9.0/bin/kafka-storage.sh random-uuid)

kafka_2.13-3.9.0/bin/kafka-server-start.sh kafka_2.13-3.9.0/config/kraft/server.properties

kafka_2.13-3.9.0/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# sert a débug mais normalement est inutile mtn
# python3 kafkconsumer.py

source .venv/bin/activate

python3 kafkproduccer1.py

uvicorn main:app --reload