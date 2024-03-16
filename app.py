from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from certificates import GetCertificate
from publisher import publisher
from subscriber import subscriber
import os
def create_flask_app():
    app = Flask(__name__)

    app_context = app.app_context()
    app_context.push()
    add_urls(app)
    CORS(app)

    appName = os.environ.get("APP_NAME", "ARQUITECTURA")
    print("iniciando aplicacion -> ", appName)
    GetCertificate.getCertificate(appName)
    print("inicializacion completa")
    return app

def add_urls(app):
    api = Api(app)
    api.add_resource(publisher.publisher, '/enviar_mensaje')
    api.add_resource(subscriber.subscriber, '/escuchar')
    api.add_resource(GetCertificate.Certificate, '/registrar_servicio', '/enviar_certificado')

app = create_flask_app()

if __name__ == "__main__":
    app.run()

