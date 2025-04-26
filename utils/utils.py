import hashlib
import datetime

def random_from_datetime():
    now = datetime.datetime.now().isoformat()
    hash_object = hashlib.sha256(now.encode())
    hash_digest = hash_object.hexdigest()
    # Convert a portion of the hash to an integer
    random_number = int(hash_digest[:10], 16)
    return random_number


import random
import time

def generate_transaction_id():
    timestamp = int(time.time())  # nombre de secondes depuis 1970
    random_number = random.randint(1000, 9999)  # 4 chiffres aléatoires
    return f"{timestamp}{random_number}"