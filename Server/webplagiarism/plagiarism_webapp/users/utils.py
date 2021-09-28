import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from plagiarism_webapp import mail


def save_picture(form_picture):
    """
    Metodo di utilità, a partire dall'immagine presa dal form (nell'aggiornamento dell'account) dai un nome random all'
    immagine, rimpiccioliscila, salvala in static/profile_pics e restituiamo il filename aggiornato per usarlo al
    di fuori della funzione
    :param form_picture:
    :return: Stringa picture_fn , contenente il nome dell'immagine aggiornata
    """
    random_hex = secrets.token_hex(8)  # passiamo 8 bytes
    _, f_ext = os.path.splitext(form_picture.filename)  # prendiamo nome e estensione con il modulo os
    # nota usando l' '_' si segnala una variabile da buttare
    picture_fn = random_hex + f_ext  # costruiamo il nome
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)  # tupla
    i = Image.open(form_picture)
    i.thumbnail(output_size)  # resize
    i.save(picture_path)  # salviamo l'immagine nel file system

    return picture_fn  # restituiamo il filename aggiornato, così da poterlo usare fuori dalla funzione


def send_reset_email(user):
    """
    Metodo di utilità, dato l'oggetto User, generiamo un token (durata di 30min) e inviamo una mail all'utente con il
    token per effettuare il reset della password
    :param user:
    :return:
    """
    token = user.get_reset_token()  # metodo definito nel model , ha un default di 30 min
    msg = Message('Password Reset Request', sender='noreply@demo.com',
                  recipients=[user.email])  # lista di utenti cui inviare
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''  # nota external = true ci crea un link assoluto e non relativo.
    mail.send(msg)
