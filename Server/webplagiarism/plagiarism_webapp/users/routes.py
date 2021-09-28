from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from plagiarism_webapp import db, bcrypt
from plagiarism_webapp.models import User, Sentence
from plagiarism_webapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                           RequestResetForm, ResetPasswordForm)
from plagiarism_webapp.users.utils import save_picture, send_reset_email
from flask import jsonify
users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])  # specifichiamo i metodi accettati
def register():
    """
    Route per la registrazione di un utente, permette di accedere al form e di effettuare la registrazione in caso
    di submit del suddetto form
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  # se siamo già loggati, redirect a home
    form = RegistrationForm()
    if form.validate_on_submit():  # prima di fare il rendering, controllo se il form ha validato quando è stato submit
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, password=hashed_password, expertise=form.expertise.data)  #
        db.session.add(user)  # aggiungo
        db.session.commit()   # commit
        flash('Your account has been created! You are now able to login', 'success')
        return redirect(url_for('users.login'))  # name of the function
    return render_template('register.html', title='Register', form=form)  # con form rendiamo accessibile il form

@users.route("/loginMobile", methods=['GET', 'POST'])
def loginMobile():
    """
    Route per il login di un utente, permette di accedere al form e di effettuare il login in caso
    di submit del suddetto form
    :return:
    """

    mail = request.args.get('mail', None)
    password = request.args.get('pw',None)
    user = User.query.filter_by(email=mail).first()
    if user and bcrypt.check_password_hash(user.password, password):  # if user exists and pass matches
        return "1"  # LOGIN OK -> REDIRECT AL MENU
    else:
        return "0"  # NO LOGIN -> ERRORE

@users.route("/accountMobile", methods=['GET', 'POST'])
def accountMobile():
    """
    Route per visualizzare i dati di un account
    :return:
    """

    mail = request.args.get('mail', None)
    user = User.query.filter_by(email=mail).first()
    return createJsonUser(user)

def createJsonUser(user):
    id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    image_file = user.image_file
    password = user.password
    expertise = user.expertise

    userData = {
        "id": id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "image_file": image_file,
        "password": password,
        "expertise": expertise
    }

    return  jsonify(userData)



@users.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route per il login di un utente, permette di accedere al form e di effettuare il login in caso
    di submit del suddetto form
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('sentences.all_sentences'))  # se siamo già loggati, redirect a home
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # if user exists and pass matches
            login_user(user, remember=form.remember.data)  # passiamo user e checkremember
            next_page = request.args.get('next')
            return redirect(next_page)if next_page else redirect(url_for('sentences.all_sentences'))  # redirect a home
        else:
            flash('Login Unsuccessful. Please check email and password!', 'danger')  # danger class -> red color
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    """
    Route per il logout dell'utente corrente
    :return:
    """
    logout_user()
    return redirect(url_for('main.home'))  # redirect a home


@users.route('/account', methods=['GET', 'POST'])
@login_required  # dobbiamo essere loggati per accedere alla route, vuole
def account():
    """
    Route per l'aggiornamento di un account, permette di accedere al form (precompilato con le vecchie informazioni)
    per poter cambiare le informazioni o caricare (o cambiare) una immagine utente
    di submit del suddetto form
    :return:
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():  # se stiamo inviando il form...
        if form.picture.data:  # se ha inserito anche un file immagine
            picture_file = save_picture(form.picture.data)  # funzione a parte per salvare sul file system
            current_user.image_file = picture_file  # settiamo il nome dell'immagine al return della funzione
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.expertise = form.expertise.data   #
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':  # Se c'è una richiesta GET
        form.username.data = current_user.username  # riempi i campi
        form.email.data = current_user.email
        form.expertise.data = current_user.expertise  #
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route("/accountUpdateMobile", methods=['GET', 'POST'])
def accountUpdateMobile():
    """
    Route per visualizzare i dati di un account
    :return:
    """

    if request.method == 'POST':
        mail = request.form.get("mail")
        user = User.query.filter_by(email=mail).first() #Cerco utente corrispondente
        if request.form.get("username") is not None: #Se ha inserito un username
            username = request.form.get("username")
            user.username = username #Aggiorno Username
        if request.form.get("expertise") is not None: #Se ha inserito delle expertise
            expertise = request.form.get("expertise")
            user.expertise = expertise #Aggiorno Expertise
        db.session.commit() #Aggiorno Utente in DB
        if request.files.get("image") is not None:
            print(request.files.get("image"))
            picture_file = save_picture(request.files.get("image"))  # funzione a parte per salvare sul file system
            user.image_file = picture_file  # settiamo il nome dell'immagine al return della funzione
        db.session.commit()
        return "OK"
    return "NO"

@users.route('/user/<string:username>')
def user_sentences(username):
    """
    Route per la visualizzazione di tutti i casi associati all'utente USERNAME
    :param username:
    :return:
    """
    page = request.args.get('page', 1, type=int)  # prendiamo il parametro page, se non c'è è 1, tipo int
    user = User.query.filter_by(username=username).first_or_404()
    sentences = Sentence.query.filter_by(author=user)\
        .order_by(Sentence.date_posted.desc())\
        .paginate(page=page, per_page=5)  #
    return render_template('user_sentences.html', sentences=sentences, user=user)  #


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
    Route per la richiesta di cambio password, si dà l'accesso al form e si invia l'email di reset in caso di submit
    Nota: l'email inviata (vedere in users/utils.py) contiene un token dalla durata di 30 minuti per cambiare la psw.
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  # se siamo già loggati, redirect a home
    form = RequestResetForm()
    if form.validate_on_submit():  # se è stato submittato il form
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_passwordMobile", methods=['GET', 'POST'])
def reset_requestMobile():
    """
    Route per la richiesta di cambio password, si dà l'accesso al form e si invia l'email di reset in caso di submit
    Nota: l'email inviata (vedere in users/utils.py) contiene un token dalla durata di 30 minuti per cambiare la psw.
    :return:
    """
    mail = request.args.get('mail', None)
    user = User.query.filter_by(email=mail).first()
    send_reset_email(user)
    return 1


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """
    Route per il cambio password, a partire dal link ricevuto nella mail, controlla se il token è valido e nel caso
    permette di accedere al form di cambiamento password.
    :param token:
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  # se siamo già loggati, redirect a home
    user = User.verify_reset_token(token)  # metodo static di user per verificare il token
    if user is None:
        flash('That is an invalid or expired token!', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()   # commit
        flash('Your password has been updated! You are now able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

