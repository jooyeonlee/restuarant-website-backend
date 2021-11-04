from flask import Flask
from config import Config
from flask_cors import CORS

from .api.routes import api
from .payment.routes import payment

#import db
from .models import db
from flask_migrate import Migrate

# defining our app as an instance of the Flask object
app = Flask(__name__)
cors = CORS(app, origins=['*']) # allow public '*'

#register blueprints
app.register_blueprint(api)
app.register_blueprint(payment)

# configure that app using our Config class
app.config.from_object(Config)

# configure db
db.init_app(app)
migrate = Migrate(app, db)

from .import models
from .import routes