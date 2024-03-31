import bcrypt
import json
import os

def set_master_password(input_password):
    if not os.path.exists('master_password.json'):
        hashed = bcrypt.hashpw(input_password.encode(), bcrypt.gensalt())
        with open('master_password.json', 'w') as file:
            file.write(json.dumps({'master_password': hashed.decode()}))
        return True
    else:
        return False

def verify_master_password(input_password):
    if not os.path.exists('master_password.json'):
        return False
    with open('master_password.json', 'r') as file:
        stored_hash = json.load(file)['master_password'].encode()
    return bcrypt.checkpw(input_password.encode(), stored_hash)

