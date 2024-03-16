from jwcrypto import jwk, jwe, jws
from jwcrypto.common import json_encode, json_decode
import codecs
import json, os
import datetime

path = "Certs/"
def decrypt(data):
    try:
        enc = json.dumps(data)

        appName = os.environ.get("PEER_NAME", "ARQUITECTURA")
        llave = appName+".crt"

        pub_pem = open(path + llave, "rb").read()
        priv_pem = open(path + "keyPrivate.key", "rb").read()

        private_key = jwk.JWK()
        private_key.import_from_pem(priv_pem)

        public_key = jwk.JWK()
        public_key.import_from_pem(pub_pem)

        ### DECRYPTING USING PRIVATE KEY PEM
        print("\nDesencriptando con llave privada..." )
        
        jwetoken = jwe.JWE()
        jwetoken.deserialize(enc)
        jwetoken.decrypt(private_key)
        payload = jwetoken.payload

        ### CHECKING SIGNATURE
        print("Validando firma con llave publica..." )
        jwstoken = jws.JWS()
        jwstoken.deserialize(payload)
        jwstoken.verify(public_key)
        payload = jwstoken.payload
        print(datetime.datetime.now())
        print("Validacion terminada con exito\n>-----" )

        return json.loads(payload)
    except FileNotFoundError as ex:
        print('ERROR:',ex)
        return {'error': 'File Not Found', 'args': ex.args[1]}
    except jwe.InvalidJWEData as ex:
        print('ERROR:',ex)
        return {'error': 'Invalid Encrypted Data', 'args': str(ex)}
    except jws.InvalidJWSSignature as ex:
        print('ERROR:',ex)
        return {'error': 'Invalid Signature', 'args:': str(ex)}
    except jws.InvalidJWSObject as ex:
        print('ERROR:',ex)
        return {'error': 'Invalid Signature Object', 'args': str(ex)}
    except Exception as ex:
        print('ERROR:',ex)
        return {'error': 'Exception', 'args': ex.args[0]}