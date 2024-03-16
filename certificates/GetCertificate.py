import requests
from flask_restful import Resource
from flask import request
import json 
import base64
import time
import os

class Certificate(Resource):
    def post(self):
        print("Recibiendo registros de servicio")
        certificate = request.json

        fh = open("./Certs/"+certificate["api"]+".crt", "wb")
        fh.write(base64.b64decode(certificate["public_cert"]))
        fh.close()

        print("Servicio" + certificate["api"] + "registrado")

    def put(self):
        print("Registrando servicio con receptor")
        SendCertificate()        

def getCertificate(name):
    url = 'https://misw4202-g1-exp2-ec-5cf63e1ac9b4.herokuapp.com/crearcertificado'
    myobj = {'api': name}

    json_object = requests.post(url, json = myobj)
    objCert = json_object.json()

    keyPublic = objCert['public_cert']
    keyPrivate = objCert['private_key']

    fh = open("./Certs/keyPublic.crt", "wb")
    fh.write(base64.b64decode(keyPublic))
    fh.close()

    fh = open("./Certs/keyPrivate.key", "wb")
    fh.write(base64.b64decode(keyPrivate))
    fh.close()
    print("Llaves recibidas correctamente")

def SendCertificate():
    print('enviando certificado')
    auxUrl = os.environ.get("PEER_SERVICE", "")

    url = auxUrl+'/registrar_servicio'
    print("Destino: ", url)
    cert = open("./Certs/keyPublic.crt", "rb").read()

    b64 = base64.b64encode(cert)
    key = b64.decode('ascii')
    appName = os.environ.get("APP_NAME", "ARQUITECTURA")
    myobj = {'api': appName, 'public_cert': key}

    json_object = requests.post(url, json = myobj)

    print(json_object)
    print('servicio '+ appName +' registrado')