from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from plagiarism_webapp.config import Config


db = SQLAlchemy()  # creiamo l'istanza del db
bcrypt = Bcrypt()  # inizializzo bcrypt
login_manager = LoginManager()  # creo il login manager basato sull'app
login_manager.login_view = 'users.login'  # specifichiamo la route di login, per farci reindirizzare in caso di bisogno
login_manager.login_message_category = 'info'  # ci permette di aggiungere le categorie bootstrap
mail = Mail()  # creiamo l'istanza mail


def create_app(config_class=Config):   # funzione di creazione dell'applicazione
    app = Flask(__name__)  # creating the variable app = class flask / --name-- > name of module
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from plagiarism_webapp.users.routes import users  # users è il nome della variabile nel route users
    from plagiarism_webapp.sentences.routes import sentences
    from plagiarism_webapp.main.routes import main
    from plagiarism_webapp.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(sentences)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app
