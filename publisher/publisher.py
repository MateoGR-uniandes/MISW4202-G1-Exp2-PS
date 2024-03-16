import pika, os
import json
from flask_restful import Resource
from flask import request

from publisher import encrypter

class publisher(Resource):
    def post(self):
        messagesToSend = request.json
        print('lo que llego es: ', messagesToSend)
        
        # jsonMessage = json.loads(messagesToSend)
        # print('lo que salio es: ', jsonMessage)

        encryptMessage = encrypter.encrypt(messagesToSend)
        SendMessage(encryptMessage)


def SendMessage(encryptMessage):
    # URL of RabbitMQ
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    # We generate a random number of requests to make

    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='arqsub') # Declare a queue
        
    channel.basic_publish(exchange='',
                        routing_key='arqsub',
                        body=encryptMessage)

    connection.close()
    # print(encryptMessage)