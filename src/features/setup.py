import uuid
from dotenv import load_dotenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


# generate uuid using the target's mac address
def generate_uuid():
    return str(uuid.getnode())
