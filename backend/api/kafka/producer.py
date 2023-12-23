from kafka import KafkaProducer
import json
# This is still a work in progress...
class KafkaLoggingProducer:
    def __init__(self, servers, topic):
        self.producer = KafkaProducer(bootstrap_servers=servers,
                                      value_serializer=lambda m: json.dumps(m).encode('ascii'))
        self.topic = topic

    def log(self, message):
        self.producer.send(self.topic, message)
        self.producer.flush()
