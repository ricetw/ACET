import json
import secrets

from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from configs import AES_KEY

def gen_aes_data(data_payload):
    key = AES_KEY.encode("utf-8")
    iv = secrets.token_bytes(8).hex().encode("utf-8")
    data = json.dumps(data_payload).encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    Crypto_data = cipher.encrypt(pad(data, AES.block_size))
    output = str(iv.decode("utf-8")) + str(b64encode(Crypto_data).decode("utf-8"))
    return output
    
