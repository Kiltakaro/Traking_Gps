FROM confluentinc/cp-kafka:7.0.1

WORKDIR /kafka

ENV KAFKA_BROKER_ID=1
ENV KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
ENV KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
ENV KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT
ENV KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093
ENV KAFKA_PROCESS_ROLES=broker,controller
ENV KAFKA_NODE_ID=1
ENV KAFKA_LOG_DIRS=/var/lib/kafka/data
ENV KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
ENV KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1
ENV KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1
ENV KAFKA_LOG_RETENTION_HOURS=168
ENV KAFKA_LOG_SEGMENT_BYTES=1073741824
ENV KAFKA_LOG_RETENTION_CHECK_INTERVAL_MS=300000
ENV KAFKA_AUTO_CREATE_TOPICS_ENABLE=true


COPY . .

VOLUME /var/lib/kafka/data

# ajout des permissions pour les logs
USER root
RUN mkdir -p /kafka/logs && chmod -R 777 /kafka/logs


RUN bin/kafka-storage.sh format --config config/kraft/server.properties --cluster-id $(bin/kafka-storage.sh random-uuid)

# Pour debug si besoin 
# CMD ["sh", "-c", "ls -a /kafka/config/kraft"]
# CMD ["sh", "-c", "ls -a /kafka && ls -a /kafka/config && ls -a /etc/kafka"]


# RUN bin/kafka-topics.sh --create --topic test_topic --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1
# RUN bin/kafka-topics.sh --list --bootstrap-server kafka:9092

# Pour lancer le broker au lancement
CMD ["sh", "-c", "bin/kafka-server-start.sh /kafka/config/kraft/server.properties"]

