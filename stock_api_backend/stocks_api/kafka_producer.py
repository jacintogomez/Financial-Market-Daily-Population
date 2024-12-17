from confluent_kafka import Producer

producer_config={
    'bootstrap.servers': 'localhost:9092',
}

producer=Producer(producer_config)

def send_message(topic,key,message):
    producer.produce(topic,key=key,value=message)
    producer.flush()

if __name__ == '__main__':
    send_message('market_data','population_complete','sample completion message')