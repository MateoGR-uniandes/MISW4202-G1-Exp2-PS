from flask import Flask, jsonify, abort
import pika, os, random, json
from flask_restful import Resource
from flask import request
from subscriber import decrypter

class subscriber(Resource):
    def post(self):
        print("Comenzando a escuchar")
        LeerCola()

def LeerCola():
    url = os.environ.get("CLOUDAMQP_URL", "amqp://guest:guest@localhost:5672/%2f")

    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue="arqsub")

    def callback(ch, method, properties, body):
        print('mensaje recibido -> ', body)
        a =  decrypter.decrypt(json.loads(body))
        print('mensaje desencriptado ->', a)

    channel.basic_consume("arqsub", callback, auto_ack=True)

    try:
        channel.start_consuming()
    except pika.exceptions.ConnectionClosedByBroker as ex:
        print("Processed until connection closed")
        # exit(0)

    connection.close()
    # print(messageDecrypted)
