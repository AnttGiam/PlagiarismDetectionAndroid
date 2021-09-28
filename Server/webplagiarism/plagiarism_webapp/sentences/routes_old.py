from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required

from plagiarism_webapp.sentences.forms import SentenceForm, SentenceWithFilesForm, UpdateSentenceForm, SearchForm
from plagiarism_webapp.sentences.utils import *

sentences = Blueprint('sentences', __name__)


@sentences.route('/all_sentences')
def all_sentences():
    """
    Route per la visualizzazione di tutte le sentence contenute nel database (paginate)
    :return:
    """
    page = request.args.get('page', 1, type=int)  # prendiamo il parametro page, se non c'è è 1, tipo int
    sentences = Sentence.query.order_by(Sentence.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('all_sentences.html', sentences=sentences)


@sentences.route("/new_sentence_after_check/<cv>/<roc>", methods=['GET', 'POST'])  #nota. var non hanno int e string da errore
@login_required
def new_sentence_after_check(cv, roc):
    """
    Route per l'inserimento di un caso di plagio, dopo aver fatto tutti i passi di CHECK PLAGIARISM, prende i valori
    di clustering e il risultato del confronto per sapere dove salvare .
    Permette di accedere al form (solo se loggati) e di inserire il caso appene visionato.
    :param cv:  Clustering Value.
    :param roc: Result of confrontation, a volte chiamato result kind, si riferisce a TP o FP, ovvero se plagio o no.
    :return:
    """
    form = SentenceForm()
    if form.validate_on_submit():  # se stiamo inviando il form...
        sentence = Sentence(title=form.title.data, first_song=form.first_song.data, second_song=form.second_song.data,
                            info=form.info.data, author=current_user)  #
        if form.radio_choice.data == 'hasTrialAndVerdict':  # aggiorno i valori di trial e verdict a true
            sentence.has_trial = True
            sentence.has_verdict = True
        if form.radio_choice.data == 'hasTrial':
            sentence.has_trial = True

        temp_result_list = read_result_values_file_from_static_temp()
        if temp_result_list[6].replace('\n', '') == 'TP':  # 6o -> result of confrontation, se è TP settiamo il plagio
            sentence.is_plagiarism = True

        db.session.add(sentence)
        db.session.commit()         # salvo e faccio il commit

        create_sentence_dir(sentence.id)  # creo la cartella ID per la nuova sentenza
        copy_files_from_static_to_dir_and_generate_subfolders(sentence.id)  # copio i files da static/last_check_temp_files (e creosottocart.)

        update_ensamble_dataset_using_datasetcouple(cv, roc)    # aggiorniamo l' ENSAMBLE
        update_clustering_dataset_using_datasetcouple()         # aggiorniamo il CLUSTERING

        if sentence.has_verdict:  # se ha il verdetto
            if form.verdict_file.data:  # e il file è stato effettivamente caricato
                save_verdict_in_sentence_dir(sentence.id, form.verdict_file.data)  # salviamo il verdict
                flash('The Case has been created and the verdict file saved!', 'success')
            else:
                flash('The Case has been created but no uploaded verdict was found!', 'info')
        else:
            flash('The Case has been created!', 'success')
        return redirect(url_for('sentences.all_sentences'))
    return render_template('create_sentence.html', title='New Case', form=form, legend='New Case')  #


@sentences.route("/new_sentence_no_check/new", methods=['GET', 'POST'])  #
@login_required
def new_sentence_no_check():
    """
    Route per l'inserimento diretto di un caso di plagio, in questo caso si accede al form e una volta effettuato
    il submit, tutti i calcoli verranno fatti in background.
    Nota: Vi si accede da NEW CASE nella navbar
    :return:
    """
    form = SentenceWithFilesForm()  #
    if form.validate_on_submit():  # se stiamo inviando il form...
        sentence = Sentence(title=form.title.data, first_song=form.first_song.data, second_song=form.second_song.data,
                            info=form.info.data, author=current_user)  # TP fino a prova cont.
        if form.radio_choice.data == 'hasTrialAndVerdict':  # aggiorno i valori di trial e verdict a true
            sentence.has_trial = True
            sentence.has_verdict = True
        if form.radio_choice.data == 'hasTrial':
            sentence.has_trial = True
        db.session.add(sentence)
        db.session.commit()  # creo la sentenza

        create_sentence_dir(sentence.id)  # creo la directory

        save_songs_in_legacy_and_static(form.song_file1.data, form.song_file2.data)   # salvo le canzoni in legacy per calcolare
        calculate_and_save_values_and_lcs_from_legacy()  # calcola i valori, salva in temp i valori e lcs
        copy_files_from_static_to_dir_and_generate_subfolders(sentence.id)  # copio tutti i files da static/last_check_temp_files

        temp_result_list = read_result_values_file_from_static_temp()  # leggo le informazioni dal file calcolato
        cv = temp_result_list[7].replace('\n', '')
        roc = temp_result_list[6].replace('\n', '')

        update_ensamble_dataset_using_datasetcouple(cv, roc)            # con esse aggiorno ENSAMBLE
        update_clustering_dataset_using_datasetcouple()                 # con esse aggiorno CLUSTERING

        if roc == 'TP':                         # se il calcolo ha rivelato che è plagio
            sentence.is_plagiarism = True       # setto a TRUE - > di default è FALSE
            db.session.commit()                 # rifaccio il commit

        if sentence.has_verdict:  # se ha il verdetto
            if form.verdict_file.data:  # e il file è stato effettivamente caricato
                save_verdict_in_sentence_dir(sentence.id, form.verdict_file.data)  # salviamo il verdict
                flash('The Case has been created and the verdict file saved!', 'success')
            else:
                flash('The Case has been created but no uploaded verdict was found!', 'info')
        else:
            flash('The Case has been created!', 'success')
        return redirect(url_for('sentences.all_sentences'))
    return render_template('create_sentence_with_files.html', title='New Case', form=form, legend='New Case')  #


@sentences.route("/sentence/<int:sentence_id>")
def sentence(sentence_id):
    """
    Route per la visualizzazione di un caso di plagio a partire dal suo id, verranno letti tutti i valori dal file
    result_values.txt associato alla cartella ID e inviati al template Html.
    Nota: in caso di file mancante, il flag result_file_not_found verrà settato a true, permettendo la visualizzazione
        di un messaggio d'errore nel template.
    :param sentence_id:
    :return:
    """
    sentence = Sentence.query.get_or_404(sentence_id)
    result_info = read_result_values_file_from_sentence_folder(sentence_id)  # leggiamo dal file result_values.txt
    file_name1 = result_info[10]  # eliminiamo il newline, questo è l'unico caso in cui da problemi
    file_name2 = result_info[11]
    result_file_not_found = False
    if result_info[0] == '0' and result_info[0] == '0' and result_info[0] == '0':
        result_file_not_found = True                             # se i valori sono a zero, il file non è stato trovato
    return render_template('sentence.html', title='sentence.title', sentence=sentence, result_info=result_info,
                           file_name1=file_name1, file_name2=file_name2, result_file_not_found=result_file_not_found)


@sentences.route("/sentence/<int:sentence_id>/update", methods=['GET', 'POST'])  # update aggiornato con i file e fold.
@login_required
def update_sentence(sentence_id):
    """
    Route per l'aggiornamento di un caso di plagio, permette di accedere al form (precompilato con i precedenti valori)
    e di effettuare cambiamenti;
    nel caso in cui si cambino anche i files .xml delle canzoni, verranno ricalcolati i valori e aggiornati i dataset;
    nel caso venga inserito il file verdict.pdf esso verrà sostituito o aggiunto in base al caso.
    :param sentence_id:
    :return:
    """
    sentence = Sentence.query.get_or_404(sentence_id)  #
    if sentence.author != current_user:  #
        abort(403)  # abort manuale, risposta http per una route forbidden
    form = UpdateSentenceForm()  #
    if form.validate_on_submit():
        if form.song_file1.data and form.song_file2.data:  # se ho inserito due files

            remove_old_dataset_entries(sentence_id)  # rimuovo i vecchi dati dal dataset
            clear_sentence_dir_and_subdirs(sentence_id, except_verdict=True)  # pulizia della cartella ECCETTO verdict.pdf
            delete_sentence_lcs_subfolders(sentence_id)  # cancello le sottocartelle prima di rigenerarle

            save_songs_in_legacy_and_static(form.song_file1.data, form.song_file2.data)  # salvo le canzoni in legacy
            calculate_and_save_values_and_lcs_from_legacy()  # calcola i valori, salva in temp i valori e lcs

            copy_files_from_static_to_dir_and_generate_subfolders(sentence_id)  # files da static/last_check_temp_files

            temp_result_list = read_result_values_file_from_static_temp()  # leggo le informazioni dal file calcolato
            cv = temp_result_list[7].replace('\n', '')
            roc = temp_result_list[6].replace('\n', '')

            update_ensamble_dataset_using_datasetcouple(cv, roc)  # con esse aggiorno ENSAMBLE
            update_clustering_dataset_using_datasetcouple()  # con esse aggiorno CLUSTERING

            if roc == 'TP':
                sentence.is_plagiarism = True  # valuta se il plagio è cambiato
            if roc == 'FP':
                sentence.is_plagiarism = False  # valuta se il plagio è cambiato

        if form.radio_choice.data == 'hasTrialAndVerdict':
            sentence.has_trial = True
            sentence.has_verdict = True
            if form.verdict_file.data:
                add_or_substitute_verdict_in_sentence(sentence_id, form.verdict_file.data)  # aggiungi o sostituisci verdict.pdf
        if form.radio_choice.data == 'hasTrial':
            sentence.has_trial = True
            sentence.has_verdict = False
        if form.radio_choice.data == 'noTrial':
            sentence.has_trial = False
            sentence.has_verdict = False

        sentence.title = form.title.data  #
        sentence.first_song = form.first_song.data  #
        sentence.second_song = form.second_song.data  #
        sentence.info = form.info.data  #

        db.session.commit()
        if form.song_file1.data and form.song_file2.data:
            flash('Your Case has been updated along with the new files!', 'success')
        elif form.song_file1.data or form.song_file2.data:
            flash('Your Case has been updated, but the file was ignored, you cannot update with only one!', 'warning')
        else:
            flash('Your Case has been updated!', 'success')
        return redirect(url_for('sentences.sentence', sentence_id=sentence.id))  # reinviamo alla sentence
    elif request.method == 'GET':  # se è una richiesta get
        form.title.data = sentence.title  # riempiamo già il form con le informazioni necessarie
        form.first_song.data = sentence.first_song  #
        form.second_song.data = sentence.second_song  #
        form.info.data = sentence.info  #
        if sentence.has_verdict:            # in base al valore di sentence, iniziamo già settandolo
            form.radio_choice.data = 'hasTrialAndVerdict'
        elif sentence.has_trial:
            form.radio_choice.data = 'hasTrial'
        else:
            form.radio_choice.data = 'noTrial'
    return render_template('create_sentence_with_files.html', title='Update Case', form=form,
                           legend='Update Case')


@sentences.route("/sentence/<int:sentence_id>/delete", methods=['POST'])  # non fatta la versione old, è ibrido.
@login_required
def delete_sentence(sentence_id):
    """
    Route per l'eliminazione di un caso di plagio ed eliminazione delle cartelle associate
    :param sentence_id:
    :return:
    """
    sentence = Sentence.query.get_or_404(sentence_id)
    if sentence.author != current_user:
        abort(403)  # abort manuale, risposta http per una route forbidden
    remove_old_dataset_entries(sentence.id)  # aggiorno il dataset di quella sentenza

    if os.path.exists(get_folderpath_by_id(sentence.id)):  # se esiste la cartella
        delete_sentence_dir_and_subdirs(sentence.id)  # cancello la cartella associata
    db.session.delete(sentence)
    db.session.commit()
    flash('Your Case has been deleted!', 'success')
    return redirect(url_for('sentences.all_sentences'))


@sentences.route("/search_page", methods=['GET', 'POST'])
def search_page():
    """
    Route per la pagina di ricerca, permette di accedere ad un form dove si potranno inserire stringhe
    contenute nel titolo delle canzoni e nelle info di un caso, verrà ricercato effettuando l'AND di tutte le stringhe
    all'interno dei singoli casi nel database
    :return:
    """
    form = SearchForm()
    if form.validate_on_submit():  # se stiamo inviando il form...

        search_f_song = form.search_f_song.data  # first song
        search_s_song = form.search_s_song.data  # second song
        search_info = form.search_info.data  # info

        # la query in questa maniera funziona anche con campi vuoti, se son pieni farà un AND di tutti loro
        results = Sentence.query.\
            filter(Sentence.first_song.contains(search_f_song)).\
            filter(Sentence.second_song.contains(search_s_song)).\
            filter(Sentence.info.contains(search_info)).\
            order_by(Sentence.date_posted.desc())
        flash('Search Results:', 'info')
        return render_template('search_results.html', title='Search Results', sentences=results)
    return render_template('search_page.html', title='Search Page', form=form)  #


@sentences.route('/view_sentence_lcs/<sentence_id>')
def view_sentence_lcs(sentence_id):
    """
    Route per accedere, in base all'ID, alle informazioni per l'lcs contenute nella cartella associata all' ID
    Vengono contati i files presenti per ogni canzone e calcolati i path per accedervi.
    Vengono poi inviati al template viewlcs.htm per la visualizzazione
    Nota: nel template utilizziamo jinja2 per accedere alle immagini statiche e ai valori passati dal render_template
    :param sentence_id:
    :return:
    """
    img_count_lcs1 = 0  # contiamo i file nella cartella id/color_parts_lcs1
    for file in os.listdir(os.path.join(current_app.root_path,
                                        'static/saved_sentences/'+str(sentence_id)+'/color_parts_lcs1')):
        img_count_lcs1 += 1
        if img_count_lcs1 == 1 and file.find('-') > 1:  # controlliamo se contiene il trattino per evitare il file xml
            _, fntmp = file.split('1', 1)
            fn1, _ = fntmp.split('-')
    img_count_lcs2 = 0  # contiamo i file nella cartella id/color_parts_lcs2
    for file in os.listdir(os.path.join(current_app.root_path,
                                        'static/saved_sentences/'+str(sentence_id)+'/color_parts_lcs2')):
        img_count_lcs2 += 1
        if img_count_lcs2 == 1 and file.find('-') > 1:  # controlliamo se contiene il trattino per evitare il file xml
            _, fntmp = file.split('2', 1)
            fn2, _ = fntmp.split('-')

    path_str1 = 'saved_sentences/' + str(sentence_id) + '/color_parts_lcs1/PROCESS1' + fn1
    path_str2 = 'saved_sentences/' + str(sentence_id) + '/color_parts_lcs2/PROCESS2' + fn2

    return render_template('viewlcs.html', img_count_lcs1=img_count_lcs1, img_count_lcs2=img_count_lcs2,
                           path_str1=path_str1, path_str2=path_str2)


@sentences.route('/alphatab_player/<int:sentence_id>/<string:song_name>')  # route per chiamare alphatab_player.html
def alphatab_player(sentence_id, song_name):
    """
    Route che, a partire dall'id del e dal nome della canzone (file xml associato al caso) genera il path
    necessario al template alphatab_player.html per la visualizzazione dello spartito associato.
    :param sentence_id:
    :param song_name:
    :return:
    """
    file_path = 'saved_sentences/' + str(sentence_id) + '/' + song_name + ".xml"
    return render_template('alphatab_player.html', file_path=file_path)
