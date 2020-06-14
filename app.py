from flask import Flask
from models.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from controllers.student import *
from controllers.course import *
from controllers.faculty import *
from controllers.field import *
from controllers.grade import *
from controllers.occupation import *
from controllers.semester import *

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000) # to listen on all public IP addresses
    app.run(port=8080)
