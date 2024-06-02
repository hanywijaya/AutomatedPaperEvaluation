from random import randint
from flask import Flask

app = Flask(__name__)


def generate_token():
    token = randint(100000, 999999)
    return token

    
number = generate_token()
print(number)