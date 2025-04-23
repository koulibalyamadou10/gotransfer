import hashlib
import datetime

def random_from_datetime():
    now = datetime.datetime.now().isoformat()
    hash_object = hashlib.sha256(now.encode())
    hash_digest = hash_object.hexdigest()
    # Convert a portion of the hash to an integer
    random_number = int(hash_digest[:10], 16)
    return random_number

