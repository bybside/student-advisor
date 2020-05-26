from flask import Flask
from models.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from routes import *

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000) # to listen on all public IP addresses
    app.run(port=8080)
