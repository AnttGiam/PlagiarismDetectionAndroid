from os import listdir
from flask import current_app
from plagiarism_webapp.main.utils import get_songs_info_from_datasetcouple, \
    write_result_values_in_static_temp, calculate_results_and_informations,\
    clean_and_generate_lcs_and_get_file_names,\
    save_songs_in_legacy_and_static, update_ensamble_dataset_using_datasetcouple  # <- usato in sentences/routes
from plagiarism_webapp.models import Sentence
from plagiarism_webapp import db
import os
from shutil import copyfile, copytree


#######################################################################################################################
# Metodi per l'aggiunta di files nella directory
#######################################################################################################################


def add_or_substitute_verdict_in_sentence(sentence_id, verdict_file):
    """
    Metodo per l'aggiunta o sostuzione del file verdict.pdf, a partire dall' ID di un caso si accede alla sua cartella
    se il file esiste, viene prima rimosso e poi viene richiamata la funzione per aggiungere il nuovo verdict.pdf
    :param sentence_id:
    :param verdict_file:
    :return:
    """
    sentence_dir_path = get_folderpath_by_id(sentence_id)
    file_list = os.listdir(sentence_dir_path)
    if 'verdict.pdf' in file_list:
        os.remove(os.path.join(sentence_dir_path, 'verdict.pdf'))  # cancello il vecchio verdict.pdf
    save_verdict_in_sentence_dir(sentence_id=sentence_id, verdict_file=verdict_file)


def save_verdict_in_sentence_dir(sentence_id, verdict_file):
    """
    Metodo di utilità, dato l'id di una sentenza e il file del verdetto, salviamolo nella directory associata
    :param sentence_id:
    :param verdict_file:
    :return: Booleano, True se la cartella esiste e il file viene quindi aggiunto , False altrimenti
    """
    folder_path = get_folderpath_by_id(sentence_id)
    exists = os.path.exists(folder_path)
    if exists:  # se la cartella esiste...
        verdict_file_path = os.path.join(folder_path, 'verdict.pdf')  # prepariamo il path ( rinomina anche il file )
        verdict_file.save(verdict_file_path)  # salviamo il file verdict.pdf nella cartella
        return True
    return False


def copy_files_from_static_to_dir_and_generate_subfolders(sentence_id):
    """
    Metodo utilizzato quando abbiamo già fatto il controllo del plagio, abbiamo quindi già i files in static, nella
    cartella static/last_check_temp_files, copiamo quindi i files nelle cartelle associate all'id ricevuto in input
    Nota: Prima di copiare i files per l'lcs, generiamo anche le sottocartelle, lo facciamo qui per poter usare
          comodamente la funzione copytree.
    :param sentence_id:
    :return:
    """
    # Copia dei files xml, result e pdf #########################################################
    folder_path = get_folderpath_by_id(sentence_id)
    last_check_temp_files = os.path.join(current_app.root_path, 'static/last_check_temp_files')

    files = os.listdir(last_check_temp_files)
    for file in files:
        tmp_path = os.path.join(last_check_temp_files, file)
        if os.path.isfile(tmp_path):  # solo se si tratta di un file. copialo nella folder ID
            copyfile(tmp_path, os.path.join(folder_path, file))

    # last_check_temp_files_lcs1 = os.path.join(current_app.root_path, 'static/last_check_temp_files/color_parts_lcs1')
    #  last_check_temp_files_lcs2 = os.path.join(current_app.root_path, 'static/last_check_temp_files/color_parts_lcs2')
    #  lcs1_folder_path = folder_path + '/color_parts_lcs1'
    #  lcs2_folder_path = folder_path + '/color_parts_lcs2'
    #  copytree(last_check_temp_files_lcs1, lcs1_folder_path)  # creazione e copia delle cartelle lcs
    #  copytree(last_check_temp_files_lcs2, lcs2_folder_path)  # usando la ricorsione di copytree
    # COMMENTATO PER FARLO PARTIRE SU LINUX DEL PROF

#######################################################################################################################
# Metodi per la gestione delle cartelle
#######################################################################################################################


def create_sentence_dir(sentence_id):
    """
    Metodo di utilità, dato l'id di una sentenza, crea la nuova cartella ID
    Nota: Non crea le sottocartelle per l'lcs, quelle vengono create quando servono
          dal metodo copy_files_from_static_to_dir_and_generate_subfolders()
    :param sentence_id:
    :return: Stringa contenente il path della cartella ID appena creata
    """
    folder_path = get_folderpath_by_id(sentence_id)
    try:
        os.mkdir(folder_path)
    except OSError as error:  # errore, cartella già esistente
        print(error)
    return folder_path


def delete_sentence_lcs_subfolders(sentence_id):
    """
    Metodo che si occupa di eliminare SOLO le sottocartelle (per l'LCS)
    NOTA: Utilizzato per l'aggiornamento di un caso, dopo aver ripulito le cartelle, in modo da poterle rigenerare
        comodamente quando verrà richiamato il metodo copy_files_from_static_to_dir_and_generate_subfolders() .
    :param sentence_id:
    :return:
    """
    folder_path = get_folderpath_by_id(sentence_id)
    lcs1_folder_path = folder_path + '/color_parts_lcs1'
    lcs2_folder_path = folder_path + '/color_parts_lcs2'
    try:
        os.rmdir(lcs1_folder_path)
        os.rmdir(lcs2_folder_path)
        print("Directory has been removed successfully")
    except OSError as error:
        print(error)
        print("Directory can not be removed")  # errore, cartella non vuota


def delete_sentence_dir_and_subdirs(sentence_id):
    """
    Metodo di utilità, dato l'id di una sentenza, cancella i contenuti ed elimina la cartelle associate
    Nota: cancelliamo prima le sottocartelle, non si possono rimuovere cartelle contenenti qualcosa.
    :param sentence_id:
    :return:
    """
    clear_sentence_dir_and_subdirs(sentence_id)  # cancelliamo i files nella cartella
    folder_path = get_folderpath_by_id(sentence_id)
    lcs1_folder_path = folder_path + '/color_parts_lcs1'
    lcs2_folder_path = folder_path + '/color_parts_lcs2'
    try:
        os.rmdir(lcs1_folder_path)
        os.rmdir(lcs2_folder_path)
        os.rmdir(folder_path)        # rimuoviamo le cartelle , nota: se i file non sono stati eliminati dà eccezione
        print("Directory has been removed successfully")
    except OSError as error:
        print(error)
        print("Directory can not be removed")  # errore, cartella non vuota


def clear_sentence_dir_and_subdirs(sentence_id, except_verdict=False):
    """
    Metodo di utilità, dato l'id di una sentenza, elimina il contenuto dalle cartelle associate
    Se il paramtro except_verdict è TRUE non si elimina il file verdict.pdf, se viene omesso o settato a FALSE
    il controllo non viene fatto e tutto viene eliminato.
    :param sentence_id:
    :param except_verdict:
    :return:
    """
    folder_path = get_folderpath_by_id(sentence_id)
    lcs1_folder_path = folder_path + '/color_parts_lcs1'
    lcs2_folder_path = folder_path + '/color_parts_lcs2'
    for root, dirs, files in os.walk(folder_path):  # pulisci i file dalla cartella ID
        for file in files:
            if except_verdict and file == 'verdict.pdf':  # se except_verdic e il file è verdict.pdf non fare nulla
                pass  # do nothing
            else:                                          # altrimenti elimina come di consueto
                os.remove(os.path.join(root, file))
    for root, dirs, files in os.walk(lcs1_folder_path):  # pulisci i file dalla prima sottocartella per l'lcs
        for file in files:
            os.remove(os.path.join(root, file))
    for root, dirs, files in os.walk(lcs2_folder_path):  # pulisci i file dalla seconda sottocartella per l'lcs
        for file in files:
            os.remove(os.path.join(root, file))


#######################################################################################################################
# Semplici metodi di comodità per creare il path della cartella con nome = id della sentenza e vedere se cartella esiste
#######################################################################################################################


def get_folderpath_by_id(sentence_id):
    """
    Semplice metodo di comodità, dato l'id di una sentenza, converte l'id a stringa e
    costruisce il path della cartella in static/saved_sentences/NOME_CARTELLA
    :param sentence_id:
    :return: Stringa contenente il path richiesto
    """
    foldername = str(sentence_id)
    path = os.path.join(current_app.root_path, 'static/saved_sentences/' + foldername)
    return path


#######################################################################################################################
# Metodi per l'aggiornamento del dataset
#######################################################################################################################


def remove_old_dataset_entries(sentence_id):  # ELIMINAZIONE VECCHIA ROW DEI DATASET DURANTE CANCELLAZIONE
    """
    A partire dall'id di una sentenza che sta per essere cancellata esegue l'eliminazione delle vecchie informazioni da
     datasetTP/datasetFP (ensamble) e da datasetFit (clustering)
    :param sentence_id:
    :return:
    """
    delete_old_dataset_row(sentence_id)
    delete_songs_from_datasetfit(sentence_id)  # cancelliamo anche dal datasetfit per il CLUSTERING


# ############## metodi derivanti da quelli richiamati da main.utils ###################


def calculate_and_save_values_and_lcs_from_legacy():
    """
    Utilizzando alcuni metodi da main/utils.py calcoliamo tutti i valori
    ( a partire da due files .xml presenti in legacy PARTS) e salviamoli nel file result_values.txt
    in last_check_temp_files, poi ripuliamo le cartelle associate e ricalcoliamo  l'lcs, salvando sempre in
    last_check_temp_files
    Nota: Utilizzato per l'inserimento di un caso con files con New Case e per l'update dei files di un caso
          (dove andranno ricalcolati i valori)
    :return:
    """
    # facciamo i controlli se sia plagio e aggiungiamo al dataset (fp o tp)
    dictionary, labels, values, val_clustering, val_threshold, avg, result_of_confrontation, file_name1, file_name2 \
        = calculate_results_and_informations()
    # salva il file del risultato nella cartella temporanea
    write_result_values_in_static_temp(dictionary, avg, result_of_confrontation, file_name1, file_name2)
    # _, _ = clean_and_generate_lcs_and_get_file_names()  # non utilizziamo il return dei nomi dei files(già li abbiamo)
    # commentato per permettere il funzionamento su linux


# ################# metodi per la cancellazione e sostituzione delle righe dal dataset FP & TP ############### #


def delete_old_dataset_row(sentence_id):
    """
    A partire dall'id di una sentenza nel database cancella la coppia di canzoni da datasetTP o datasetFP
    (se salvata in uno dei due)
    :param sentence_id:
    :return:
    """
    dataset_fp_path = os.path.join(current_app.root_path, 'main/legacy/datasetFP.csv')
    dataset_tp_path = os.path.join(current_app.root_path, 'main/legacy/datasetTP.csv')
    sentence_dir_path = get_folderpath_by_id(sentence_id)

    songs_names = []
    listdir_names = listdir(sentence_dir_path)  # mi prendo i nomi dei file
    for file_name in listdir_names:                   # salvo soltanto i files xml
        if '.xml' in file_name:
            songs_names.append(file_name)

    old_song_name_1, _ = os.path.splitext(songs_names[0])  # tolgo l'estensione
    old_song_name_2, _ = os.path.splitext(songs_names[1])  # il _ sarebbe l'estensione che scartiamo

    # costruisco riga da cercare
    row = old_song_name_1 + ';' + old_song_name_2 + ';'
    reverse_row = old_song_name_2 + ';' + old_song_name_1 + ';'

    sentence = Sentence.query.get_or_404(sentence_id)  # accedo alla sentence nel database
    if sentence.is_plagiarism:  # se è plagio sarà salvato in TP, altrimenti in FP  # todo check
        with open(dataset_tp_path, "r") as f:  # apro il file in lettura
            lines_list = f.readlines()  # salvo le righe
        with open(dataset_tp_path, "w") as f:  # riapro il file in scrittura
            for line in lines_list:  # per ogni riga
                if not (line.startswith(row) or line.startswith(reverse_row)):
                    f.write(line)
    else:  # FP # todo check
        with open(dataset_fp_path, "r") as f:  # apro il file in lettura
            lines_list = f.readlines()  # salvo le righe
        with open(dataset_fp_path, "w") as f:  # riapro il file in scrittura
            for line in lines_list:  # per ogni riga
                if not (line.startswith(row) or line.startswith(reverse_row)):
                    f.write(line)


########################################################################################################################
# funzioni per l' aggiornamento datasetFit
########################################################################################################################

def update_clustering_dataset_using_datasetcouple():
    """
    Sfruttando i valori di datasetCouple.csv aggiunge le canzoni al datasetfit.csv ( del progetto legacy )
    :return:
    """
    first_song_name, first_string_repr, second_song_name, second_string_repr = get_songs_info_from_datasetcouple()
    string_row1 = first_song_name + ',' + first_string_repr  # costruisco le stringhe
    string_row2 = second_song_name + ',' + second_string_repr
    lines_list = get_all_rows_from_datasetfit()  # prendo tutte le rows del datasetfit
    lines_list.append(string_row1)  # aggiungo le stringhe alla lista ( come se le avessimo prese dal vecchio file)
    lines_list.append(string_row2)  # non hanno il numero, proprio come le linee restituite da get all rows
    rewrite_rows_in_datasetfit(lines_list=lines_list)  # riscrivo la nuova lista in datasetfit


def delete_songs_from_datasetfit(sentence_id):
    """
    Dato l'id di una sentenza nel database elimina le righe di quelle canzoni da datasetfit.csv ( del progetto legacy )
    :param sentence_id:
    :return:
    """
    sentence_dir_path = get_folderpath_by_id(sentence_id)

    songs_names = []
    listdir_names = listdir(sentence_dir_path)  # mi prendo i nomi dei file
    for file_name in listdir_names:  # salvo soltanto i files xml
        if '.xml' in file_name:
            songs_names.append(file_name)

    old_song1, _ = os.path.splitext(songs_names[0])  # tolgo l'estensione
    old_song2, _ = os.path.splitext(songs_names[1])  # il _ sarebbe l'estensione che scartiamo

    lines = get_all_rows_from_datasetfit(except_this_one=old_song1)  # prendo tutte le righe eccetto old_song1
    rewrite_rows_in_datasetfit(lines_list=lines)  # riscrivo le linee nel file
    lines = get_all_rows_from_datasetfit(except_this_one=old_song2)  # prendo tutte le righe eccetto old_song2
    rewrite_rows_in_datasetfit(lines_list=lines)  # riscrivo le linee nel file


def get_all_rows_from_datasetfit(except_this_one='X,X,X,X,X'):
    """
    Salva tutte le righe di datasetFit.csv ( del progetto legacy ) nella lista lines, se presente la variabile
    except_this_one la utilizza per non salvare quella stringa ( così in un futuro salvataggio verrà ignorata )
    Nota: Except this one viene utilizzato per ottenere tutte le righe eccetto quella da eliminare per poi riscriverle.
    :param except_this_one:
    :return: Lista contenente le righe : lines
    """
    lines = []  # empty list
    song_name = except_this_one
    path_datasetfit = os.path.join(current_app.root_path, 'main/legacy/datasetFit.csv')
    with open(path_datasetfit) as data_file:  # apro il file datasetFit.csv in lettura
        for row in data_file:  # per ogni riga
            if row.find(',' + song_name + ',') == -1:  # se row.find songname da -1 significa CHE NON E' QUELLA
                # Queste righe sono tutte tranne quella che contiene song_name, quindi rimuovo il numero dalla linea
                _, new_line = row.split(',', 1)  # tolgo fino alla virgola <<<
                lines.append(new_line)  # e la salvo nella nostra lista
    return lines  # restituisco le linee del files


def rewrite_rows_in_datasetfit(lines_list):  # riscrivo datasetfit a partire da una lista
    """
    Prende una lista in input e riscrive tutte le righe di quella lista in datasetFit.csv ( del progetto legacy )
    :param lines_list:
    :return:
    """
    path_datasetfit = os.path.join(current_app.root_path, 'main/legacy/datasetFit.csv')
    del lines_list[0]  # elimino la prima linea ( che rappresenta la legenda )
    count = 1  # cominciamo da 1
    with open(path_datasetfit, 'w') as file_output:  # apro il file in scrittura
        file_output.write('N,SongName,SongString\n')  # riscrivo la prima linea ( che rappresenta la legenda )
        for line in lines_list:  # per ogni linea salvata
            riga_da_scrivere_nuova = str(count) + ',' + line  # aggiungo l'indice ( e la virgola tolta prima)
            file_output.write(riga_da_scrivere_nuova)  # e la scrivo
            count += 1  # incremento quindi il contatore


# ############## aggiunta finale per mettere plagio o non plagio a sentence # ###############

def set_is_plagiarism(sentence_id, result_of_confrontation):
    """
    Metodo di comodità, dato l'id di una sentenza e il valore se TP o FP aggiorna la colonna is_plagiarism nel database
    Nota: non viene settato il caso FALSE, in quanto è il valore di default nella table sentence (nel database)
    :param sentence_id:
    :param result_of_confrontation:
    :return:
    """
    sentence = Sentence.query.get_or_404(sentence_id)
    if result_of_confrontation == 'TP':
        sentence.is_plagiarism = True
        db.session.commit()


# ################## Metodi per la lettura dei valori dal file result_values.txt nella cartella ID o temp ########### #


def read_result_values_file_from_sentence_folder(sentence_id):
    """
    Metodo utilizzato per leggere il file result_values.txt dalla directory associata all' ID di un caso
    restituiamo una lista di valori se tutto va bene, altrimenti la lista è tutta composta di '0'
    Nota: nella route per la visualizzazione di un caso singolo ( sentence ) abbiamo un controllo, che nel caso
          trovi alcuni valori a '0', si rende conto del problema e mostra un warning
    :param sentence_id:
    :return:
    """
    lines = []  # empty list
    file_path = os.path.join(current_app.root_path, get_folderpath_by_id(sentence_id) + '/result_values.txt')
    try:
        with open(file_path) as data_file:  # apro il file result_values.txt in lettura
            for row in data_file:  # per ogni riga
                lines.append(row.strip('\n'))  # salvo nella nostra lista e tolgo i newline
    except OSError as error:  # errore
        print(error)
        lines = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']   # finti risultati
    return lines  # restituisco le linee del file


def read_result_values_file_from_static_temp():
    """
    Metodo utilizzato per leggere il file result_values.txt quando è ancora in last_check_temp_values
    Nota: questo ci è utile quando abbiamo bisogno di alcuni di quei valori per l'inserimento o aggiornamento di casi
    :return:
    """
    lines = []  # empty list
    file_path = os.path.join(current_app.root_path, 'static/last_check_temp_files/result_values.txt')
    with open(file_path) as data_file:  # apro il file result_values.txt in lettura
        for row in data_file:  # per ogni riga
            lines.append(row.strip('\n'))  # salvo nella nostra lista
    return lines  # restituisco le linee del file


# ## ### #### ##### ###### ################################### ###### ##### ##### ### ## #
