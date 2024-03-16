from jwcrypto import jwk, jwe, jws
from jwcrypto.common import json_encode, json_decode
import codecs
import json, os, datetime

path = "Certs/"
def encrypt(data):
    try:
        print('data: ', data)
        payload = json.dumps(data)
        appName = os.environ.get("PEER_NAME", "ARQUITECTURA")
        llave = appName+".crt"

        pub_pem = open(path + llave, "rb").read()
        priv_pem = open(path + "keyPrivate.key", "rb").read()
        
        public_key = jwk.JWK()
        public_key.import_from_pem(pub_pem)

        private_key = jwk.JWK()
        private_key.import_from_pem(priv_pem)

        print("Firmando con llave privada..." )
        ### SIGNING 
        jwstoken = jws.JWS(payload.encode('utf-8'))
        jwstoken.add_signature(private_key, None,
                               json_encode({"alg": "RS256"}),
                               json_encode({"kid": private_key.thumbprint()}))
        sig = jwstoken.serialize()
        sig_dict = json.loads(sig)
        sig_dict.pop('header')
        sig = json.dumps(sig_dict).encode()
        
        payload = sig
       
        ### ENCRYPTING USING PUBLIC KEY
        print("\nEncriptando con llave publica..." )
       
        protected_header = {
            "alg": "RSA-OAEP-256",
            "enc": "A256CBC-HS512",
            "typ": "JWE",
            "kid": public_key.thumbprint()
        }
       
        jwetoken = jwe.JWE(payload,
                           recipient=public_key,
                           protected=protected_header)
       
        enc = jwetoken.serialize()
       
        print("Mensaje encriptado: ", enc)
        print(datetime.datetime.now())
        print(">-----")
        return json.loads(enc)
    except FileNotFoundError as ex:
        print('ERROR:',ex)
        return {'error': 'File Not Found', 'args': ex.args[1]}
    except Exception as ex:
        print('ERROR:',ex)
        return {'error': 'Exception', 'args': ex.args[0]}