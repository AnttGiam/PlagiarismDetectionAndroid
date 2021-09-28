from flask import render_template, Blueprint, redirect, url_for, current_app

from plagiarism_webapp.main.utils import *
from plagiarism_webapp.main.forms import UploadSongsForm

from flask import request
from flask import jsonify

main = Blueprint('main', __name__)


@main.route('/')  # route decorator -> add functionality to existing function -> root page of website
@main.route('/home')
def home():
    """
    Route per la homepage
    :return:
    """
    return render_template('homepage.html')


@main.route('/about')  # about decorator
def about():
    """
    Route per la pagina About
    :return:
    """
    return render_template('about.html', title='About')  # usually we'd return html, this is a test


@main.route("/upload_songs", methods=['GET', 'POST'])  # #################
def upload_songs():
    """
    Route per il primo passo di CHECK PLAGIARISM, il caricamento delle due canzoni, tramite un piccolo form che accetta
    soltanto files .xml
    :return:
    """
    upload_songs_form = UploadSongsForm()
    if upload_songs_form.validate_on_submit():  # se raggiungo questa route dal submit (ovvero ho caricato due file xml)
        song1 = upload_songs_form.song_file1.data
        song2 = upload_songs_form.song_file2.data
        save_songs_in_legacy_and_static(song1, song2)

        song1_name, _ = os.path.splitext(song1.filename)  # prendiamo nome, ignorando l'estensione
        song2_name, _ = os.path.splitext(song2.filename)
        return redirect(url_for('main.uploaded_songs', song1=song1_name, song2=song2_name))  # altra route dove mostreremo i nomi delle canzoni caricate
    return render_template('upload_songs.html', title='Upload Songs', form=upload_songs_form)


@main.route("/upload_songsMobile", methods=['GET', 'POST'])  #Carichiamo due XML e confrontiamo
def upload_songsMobile():
    """
    Route per il primo passo di CHECK PLAGIARISM, il caricamento delle due canzoni, tramite un piccolo form che accetta
    soltanto files .xml
    :return:
    """
    print("upload mobile")
    print (request)
    if request.method == 'POST':
        song1 = request.files['song1']
        song2 = request.files['song2']
        save_songs_in_legacy_and_static(song1, song2)
        dictionary, labels, values, val_clustering, val_threshold, avg, result_of_confrontation, file_name1, file_name2\
        = calculate_results_and_informations()
        write_result_values_in_static_temp(dictionary, avg, result_of_confrontation, file_name1, file_name2)
        lines = []  # empty list
        file_path = os.path.join(current_app.root_path, 'static/last_check_temp_files/result_values.txt')
        try:
            with open(file_path) as data_file:  # apro il file result_values.txt in lettura
                for row in data_file:  # per ogni riga
                    lines.append(row.strip('\n'))  # salvo nella nostra lista e tolgo i newline
        except OSError as error:  # errore
            print(error)
            lines = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']   # finti risultati
        print(lines)
    print("post")
    dataResult = {
    "file_not_found" : False , 
    "cosine" : lines[3] , 
    "soresen_dice" : lines[4] , 
    "overlap" : lines[5] , 
    "clustering" : lines[6] , 
    "clusteringValue" : lines[7] , 
    "percentuage" : lines[8], 
    "threshold" : lines[9]
    }
    if lines[7] == '0' :
        plagiarism = False
    else :
        plagiarism = True
    return jsonify({"plagiarism": plagiarism , "dataResult": dataResult}) #Ritorno JSON Risultati

@main.route("/uploaded_songs/<string:song1>/<string:song2>")
def uploaded_songs(song1, song2):
    """
    Route per il secondo passo di CHECK PLAGIARISM, una volta caricate le canzoni verranno mostrati i loro nomi
    e gli spartiti associati, tramite iframe che richiamano il player di alphatab nel template
    Da qui si potrà effettuare il calcolo dei risultati
    :param song1:
    :param song2:
    :return:
    """
    return render_template('uploaded_songs.html', title='Loaded Songs', song1=song1, song2=song2)


@main.route('/results')
def results():
    """
    Route per il terzo passo di CHECK PLAGIARISM, il calcolo dei risultati, qui calcoliamo tutte le informazioni e le
    salviamo in result_values.txt in last_check_temp_files;
    una volta calcolati i risultati all'interno dell'iframe del template results.html, viene calcolato anche l'lcs con
    i relativi files salvati in last_check_temp_files
    :return:
    """
    dictionary, labels, values, val_clustering, val_threshold, avg, result_of_confrontation, file_name1, file_name2\
        = calculate_results_and_informations()
    write_result_values_in_static_temp(dictionary, avg, result_of_confrontation, file_name1, file_name2)
    # faccio calcolare tutto dentro utils e mi faccio dare dizionario e valori già smontati, poi scrivo il file results
    return render_template('results.html', title='Results', chValues=values, chLabels=labels,
                           clust=val_clustering, thres=val_threshold, avg=avg, resultKind=result_of_confrontation)


@main.route('/player/<string:song_name>')  # route per chiamare alphatab_player.html
def player(song_name):
    """
    Route per il player di alphatab (richiamato in iframe) ,
    a partire dal nome della canzone, genera il path necessario al template per
    la visualizzazione dello spartito
    :param song_name:
    :return:
    """
    file_path = 'last_check_temp_files/' + song_name + ".xml"
    return render_template('alphatab_player.html', file_path=file_path)


@main.route('/viewlcs')  # route per calcolare e visualizzare lcs
def viewlcs():
    """
    Route per la visualizzazione dell'lcs (richiamato in iframe) ,
    a partire dai files salvati in last_check_temp_files nelle sottocartelle per lcs genera i path e calcola il numero
    di files da visualizzare, per poi passare queste informazioni al template viewlcs.html
    :return:
    """
    fn1, fn2 = clean_and_generate_lcs_and_get_file_names()

    img_count_lcs1 = 0  # contiamo i file nella cartella last_check_temp_files/color_parts_lcs1
    for file in os.listdir(os.path.join(current_app.root_path, 'static/last_check_temp_files/color_parts_lcs1')):
        img_count_lcs1 += 1
    img_count_lcs2 = 0  # contiamo i file nella cartella last_check_temp_files/color_parts_lcs2
    for file in os.listdir(os.path.join(current_app.root_path, 'static/last_check_temp_files/color_parts_lcs2')):
        img_count_lcs2 += 1

    path_str1 = 'last_check_temp_files/color_parts_lcs1/' + 'PROCESS1' + fn1
    path_str2 = 'last_check_temp_files/color_parts_lcs2/' + 'PROCESS2' + fn2

    return render_template('viewlcs.html', img_count_lcs1=img_count_lcs1, img_count_lcs2=img_count_lcs2,
                           path_str1=path_str1, path_str2=path_str2, fn1=fn1, fn2=fn2)
