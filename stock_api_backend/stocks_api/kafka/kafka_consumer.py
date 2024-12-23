# from confluent_kafka import Consumer
#
# consumer_config={
#     'bootstrap.servers': 'localhost:9092',
#     'group.id': 'market_data_group',
#     'auto.offset.reset': 'earliest',
# }
#
# consumer=Consumer(consumer_config)
# consumer.subscribe(['market_data'])
#
# def listen_for_messages():
#     while True:
#         msg=consumer.poll(1.0)
#         if msg is None:
#             continue
#         if msg.error():
#             print(f'Consumer error: {msg.error()}')
#             continue
#         print(f"Received message: {msg.value().decode('utf-8}')}")
#
# if __name__ == '__main__':
#     listen_for_messages()