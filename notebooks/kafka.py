from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers="nav-prod-kafka-nav-prod.aivencloud.com:26484", security_protocol='SSL')
