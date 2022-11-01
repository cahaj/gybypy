from flask import Flask
from threading import Thread
import random

app = Flask('')

@app.route('/')
def home():
    return "Bot online."

def run():
  app.run(host='0.0.0.0',port=random.randint(1000, 10000))

def keep_alive():  
    t = Thread(target=run)
    t.start()