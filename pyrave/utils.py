import string
import random
import uuid


def generate_id(gen_for):
    chars = string.ascii_uppercase + string.digits
    if gen_for == "device_fingerprint":
        return str(uuid.uuid4())
    txref = "{0}_".format(gen_for)
    rand = ''.join(random.choice(chars) for _ in range(20)).lower()
    return txref + rand
