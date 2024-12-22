
PAS 

################ Lancer kafka
# LE DOCKER COMPOSE LE FAIT TOUT SEUL
# mais sinon la théorie c'est ça 

# configuration
kafka_2.13-3.9.0/bin/kafka-storage.sh format \
    --config kafka_2.13-3.9.0/config/kraft/server.properties \
    --cluster-id $(kafka_2.13-3.9.0/bin/kafka-storage.sh random-uuid)

# lancement
kafka_2.13-3.9.0/bin/kafka-server-start.sh kafka_2.13-3.9.0/config/kraft/server.properties


# voir les topics existant, vu que la premier commande cree un nouveau kafka, ça sera vide
kafka_2.13-3.9.0/bin/kafka-topics.sh --list --bootstrap-server localhost:9092


################ Backend 
# les commandes étaient en local donc python3 sert plus vu qu'on est passé au docker
# voici comment on lançait le back + front si kafka déjà allumé

source .venv/bin/activate

#lancer des msg dans le kafka
python3 producer1.py

# lancer serveur
fastapi dev main.py
OU 
uvicorn main:app --reload

# pour visualiser : 
localhost:8000

# fini
##################

##### Bonus
python3 kafkconsumer.py
# sert a débug mais normalement est inutile 
# MAIS ça sera bcp plus simple de voir si ce truc consume plutot que le main


######### Tips SQL ###############""
# identifiants
root rootpassword

# rappels mysql
mysql -u root -p
source
SHOW databases;
USE Kafka_db;
DESCRIBE Coordiantes;
SELECT * FROM Coordinates;

# rappels POSTGRESQL
# user par defaut c'est postgres
# feed le fichier sql
# dans la db kafka_db
psql -h localhost -U postgres -f db/create_db_postgresql.sql
psql -U postgres -f db/create_db_postgresql.sql
psql -U postgres -d kafka_db -f db/create_table_postgresql.sql
psql -U postgres -W
# Show
\l
# Use 
\c kafka_db
# Describe
\d Coordinates
SELECT * FROM Coordinates;
################

# pip install mysql-connector-python fastapi uvicorn kafka-python pymysql sqlalchemy psycopg2 
#pip install psycopg2-binary
# binary car psycopg2 seul ne marche pas

docker-compose down && docker-compose build --no-cache && docker-compose up --force-recreate
