from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from plagiarism_webapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader  # decoratore per far capire che è questa la funzione da usare per trovarlo
def load_user(user_id):
    return User.query.get(int(user_id))  # castato a integer giusto per sicurezza


class User(db.Model, UserMixin):  # con user mixin gestisce tutto per i login
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)  #
    last_name = db.Column(db.String(20), nullable=False)   #
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    expertise = db.Column(db.String(120), nullable=False)  #
    sentences = db.relationship('Sentence', backref='author', lazy=True)  # cambiato
    # sentences ha una relazione col modello sentence/ backref significa che da sentence si prende author

    def get_reset_token(self, expires_sec=1800):  # 1800->30 minuti
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')  # passiamo l'id dell'utente

    @staticmethod  # non userà self, in quanto è statico
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):  # praticamente un tostring
        return f"User('{self.username}, {self.first_name}, {self.last_name}, {self.email}, {self.image_file}')"  #


class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    first_song = db.Column(db.String(25), nullable=False)  #
    second_song = db.Column(db.String(25), nullable=False)  #
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # utcnow e non utcnow() altrimenti prende il valore di oggi e non la funzione
    is_plagiarism = db.Column(db.Boolean, default=False)   # booleano nullable
    has_trial = db.Column(db.Boolean, default=False)       # booleano nullable
    has_verdict = db.Column(db.Boolean, default=False)     # booleano nullable # todo controllare se tutto è ben collegato
    info = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # foreignkey dice che c'è una relazione con l'oggetto user ( tabell e colonna )

    def __repr__(self):  # praticamente un tostring
        return f"Sentence('{self.title}, {self.first_song}, {self.second_song}, {self.date_posted}')"

