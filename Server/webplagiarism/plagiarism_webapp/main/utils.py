from plagiarism_webapp.main.legacy.main import main  # importiamo la funzione main
from plagiarism_webapp.main.legacy.musicParser import music_parser_legacy
from plagiarism_webapp.main.legacy.addCouple import add_couple_main  # importiamo la funzione add_couple_main funziona aggiunta da noi
from plagiarism_webapp.main.legacy.LCS_Parts import calculateLcsFunction
from plagiarism_webapp.main.legacy.musicParser2 import music_parser2_legacy
from flask import current_app
import os


def clean_and_generate_lcs_and_get_file_names():
    """
    Ripulisce le cartelle utilizzate per salvare le informazioni per l'LCS in last_check_temp_files
    genera le stringhe musicali per per il calcolo dell'lcs
    calcola l'lcs e genera le immagini e files in last_check_temp_files.
    :return: fn1, fn2 i nomi dei files xml utilizzati
    """
    reset_lcs_folders()  # pulisce le cartelle usate dall'lcs per la nuova chiamata
    fn1, fn2 = generate_music_string_for_lcs()  # nomi dei file utilizzati
    calculate_lcs_and_generate_images()
    return fn1, fn2


def calculate_results_and_informations():
    """
    A partire dai files xml in LEGACY/PARTS genera le stringhe musicali in LEGACY/datasetcouple.csv
    Calcola le metriche e i valori con clustering e threshold dei due files xml, partendo dalle stringhe musicali
    salva tutte queste informazioni in un dizionario
    legge i nomi dei files delle canzoni da datasetcouple
    restituisce tutti questi valori, sia come dizionario, che come pezzi già suddivisi, per comodità
    :return: dizionario, dizionario smontato (labels, values, clustering, threshold, media, FP o TP (result of conf.)
    e i nomi dei due files .xml.
    """
    generate_music_strings_from_xml_songs()
    dictionary = calculate_metrics_values_with_clustering_and_threshold()
    val_clustering = dictionary.get("ValoreClustering")  # 0 , 1 o 2 per NoPlagio , Plagio e Inutilizzato
    val_threshold = dictionary.get("Threshold") * 100  # moltiplico per 100 per mostrare i valori in scala 0-100

    labels = [dictionary.get("Metrica1"),
              dictionary.get("Metrica2"),
              dictionary.get("Metrica3")]

    values = [round(dictionary.get("ValoreMetrica1") * 100, 2),
              round(dictionary.get("ValoreMetrica2") * 100, 2),
              round(dictionary.get("ValoreMetrica3") * 100,
                    2)]  # moltiplico per 100 per mostrare i valori in scala 0-100

    avg = round(((values[0] + values[1] + values[2]) / 3), 2)

    if val_clustering == 1 or (
            values[0] >= val_threshold and values[1] >= val_threshold and values[2] >= val_threshold):
        result_of_confrontation = 'TP'
    elif val_clustering == 0 or (values[0] < val_threshold and values[1] < val_threshold and values[2] < val_threshold):
        result_of_confrontation = 'FP'

    file_name1, _, file_name2, _ = get_songs_info_from_datasetcouple()
    return dictionary, labels, values, val_clustering, val_threshold, avg, result_of_confrontation, file_name1, file_name2


def write_result_values_in_static_temp(dictionary, avg, result_kind, file_name1, file_name2):
    """
    Metodo che a partire dal dizionario,media, result_king, nome dei files xml,
    restituiti da CALCULATE_RESULTS_AND_INFORMATIONS() crea, in last_check_temp_files il file di testo
    result_values.txt, dove conserviamo (ordine mostrato dal metodo stesso) tutte le informazioni calcolate
    Nota: quando vengono letti successivamente dal file, a volte bisogna fare attenzione a togliere i '\n'
          dalla fine della riga, per evitare errori, questo viene già fatto negli altri metodi.
    :param dictionary:
    :param avg:
    :param result_kind:
    :param file_name1:
    :param file_name2:
    :return:
    """
    file_path = os.path.join(current_app.root_path, 'static/last_check_temp_files/result_values.txt')
    with open(file_path, 'w') as file_output:  # apro il file in scrittura
        file_output.write(dictionary.get("Metrica1")+"\n")
        file_output.write(dictionary.get("Metrica2")+"\n")
        file_output.write(dictionary.get("Metrica3")+"\n")
        file_output.write(str(round(dictionary.get("ValoreMetrica1") * 100, 2))+"\n")
        file_output.write(str(round(dictionary.get("ValoreMetrica2") * 100, 2))+"\n")
        file_output.write(str(round(dictionary.get("ValoreMetrica3") * 100, 2))+"\n")

        file_output.write(result_kind+"\n")
        file_output.write(str(dictionary.get("ValoreClustering"))+"\n")
        file_output.write(str(avg)+"\n")
        file_output.write(str(dictionary.get("Threshold") * 100)+"\n")

        file_output.write(str(file_name1)+"\n")
        file_output.write(str(file_name2))


def save_songs_in_legacy_and_static(song1, song2):
    """
    Salva le canzoni (generalmente prese da un form, inserite quindi dall'utente in formato .xml) nella
    folder PARTS di MAIN/LEGACY e nella folder LAST_CHECK_TEMP_FILES di STATIC.
    Nota: questo serve per permettere ai metodi legacy di funzionare senza problemi e
          per accedere comodamente alle informazioni dalla cartella STATIC.
    :param song1:
    :param song2:
    :return:
    """
    for root, dirs, files in os.walk(os.path.join(current_app.root_path, 'main/legacy/parts')):  # cancella tutto
        for file in files:
            os.remove(os.path.join(root, file))

    song_path1 = os.path.join(current_app.root_path, 'main/legacy/parts', song1.filename)
    song1.save(song_path1)
    song_path2 = os.path.join(current_app.root_path, 'main/legacy/parts', song2.filename)
    song2.save(song_path2)

    song1.seek(0)  # seek per ritornare all'inizio e poter salvare anche in static
    song2.seek(0)

    for root, dirs, files in os.walk(os.path.join(current_app.root_path, 'static/last_check_temp_files')):
        for file in files:
            os.remove(os.path.join(root, file))

    song_path1 = os.path.join(current_app.root_path, 'static/last_check_temp_files', song1.filename)
    song1.save(song_path1)
    song_path2 = os.path.join(current_app.root_path, 'static/last_check_temp_files', song2.filename)
    song2.save(song_path2)
    song1.close()
    song2.close()


def reset_lcs_folders():
    """
    Cancella tutto nelle cartelle static/last_check_temp_files/color_parts_lcs1 e
                                  static/last_check_temp_files/color_parts_lcs2
    NOTA: Utilizzato per ripulire le cartelle prima di un nuovo calcolo.
    :return:
    """
    for root, dirs, files in os.walk(os.path.join(current_app.root_path,
                                                  'static/last_check_temp_files/color_parts_lcs1')):  # cancella tutto
        for file in files:
            os.remove(os.path.join(root, file))
    for root, dirs, files in os.walk(os.path.join(current_app.root_path,
                                                  'static/last_check_temp_files/color_parts_lcs2')):  # cancella tutto
        for file in files:
            os.remove(os.path.join(root, file))


def get_songs_info_from_datasetcouple():  # smonta le stringhe di datasetcouple e restituisce nomi e rappresentazioni
    """
    Estrae i nomi e le rappresentazioni delle canzoni correntemente contenute in main/legacy/datasetCouple.csv
    Nota: metodo di utilità utile per riscrivere le stringhe in altre posizioni o per accedervi comodamente dopo
          un check di plagio
    :return: Stringhe: nome_canzone1, stringa_canzone1, nome_canzone2, stringa_canzone2
    """
    songs_strings = []
    songs_names = []
    path_datasetcouple = os.path.join(current_app.root_path, 'main/legacy/datasetCouple.csv')
    with open(path_datasetcouple) as data_file:  # apro il file datasetCouple.csv in lettura
        # mentre scorro il file
        for row in data_file:
            if len(row) > 2:  # se la riga non è vuota (ovvero è maggiore di 2 caratteri '\n')
                # mi prendo la conversione in stringa della canzone
                _, song_name, song_string = row.split(',', 2)
                # salvo la conversione in stringa della canzone nell'array
                songs_strings.append(song_string)
                # salvo il nome della canzone senza l'estensione del file
                song_name = song_name.replace('.xml', '')
                songs_names.append(song_name)
    return songs_names[1], songs_strings[1], songs_names[2], songs_strings[2]


# ########################### UTILITIES ESTRAPOLATE DAI FILE LEGACY ################################################## #


# Funzione controllata, esegue correttamente il calcolo
def calculate_metrics_values_with_clustering_and_threshold():  # OLD main.py
    """
    Richiama il main legacy
    NOTA BENE: accede a PARTS per le due canzoni, a ENSAMBLE per i pareto, a datasetCouple.py e DatasetFP & TP .csv
    :return: Dict[str, Union[float,int,str]] -- Un dizionario con i valori delle tre metriche, clustering, nomi delle tre metriche, threshold
    """
    return main()


# Funzione controllata, esegue correttamente il calcolo
def generate_music_strings_from_xml_songs(folderName='parts'):  # OLD musicParser.py
    """
    Richiama il metodo folderRead(foldername) da musicParser legacy
    Il metodo legge dalla folder PARTS i file .xml e genera csv
    Genera in datasetcouple.csv le stringhe musicali dai due files .xml
    """
    music_parser_legacy(folderName)


# Funzione controllata, esegue correttamente il calcolo
def update_ensamble_dataset_using_datasetcouple(clustering_value, result_of_confrontation):  # OLD addCouple.py
    """
    Richiama ciò che faceva addCouple legacy (abbiamo messo ciò che veniva eseguito in una funzione add_couple_main() )
    Prende informazioni da PARTS e datasetcouple.csv e aggiorna datasetFP.csv o datasetTP.csv.
    :param clustering_value: Valore del clustering ottenuto dalle metriche (che valore ha tra "0", "1", "2")
    :param result_of_confrontation: Deve essere in forma "TP" o "FP" a seconda se si voglia salvare in TP o FP
    """
    clustering_value_str = str(clustering_value)  # cambiamo sempre a stringa poichè nel codice legacy non fa controlli
    add_couple_main(clustering_value_str, result_of_confrontation)


# Funzioni per l' LCS
def generate_music_string_for_lcs():  # OLD musicparser2.py
    """
        Richiama il metodo folderRead(foldername) da musicParser2 legacy
        Il metodo legge dalla folder PARTS i file .xml e
        Genera i file musicali tradotti in stringa ( versione alternativa )
        NOTA: utilizza una conversione in stringa alternativa dove non viene considerato il tempo musicale, altrimenti
              non calcolerebbe correttamente l' LCS.
        :return: fn1, fn2 ( sono i nomi dei due file utilizzati (utile per la visualizzazione dell'lcs))
        """
    fn1, fn2 = music_parser2_legacy()
    return fn1, fn2  # restiuiamo i nomi dei file


def calculate_lcs_and_generate_images():  # OLD LCS_Parts.py
    """
        Richiama il metodo calculateLcsFunction() da LCS_Parts legacy (nome metodo modificato : era mainFunction() )
        Il metodo legge dal file datasetcouple2.csv
        Calcola da esso l' LCS e genera i file immagine con le note colorate in ColorPartsLCS1 e ColorPartsLCS2
        (folders della cartella LAST_CHECK_TEMP_FILES)
        NOTA BENE : IN LCS PARTS SI RICHIAMANO DELLE VARIABILI D'AMBIENTE PER USARE MUSESCORE !!
                    Bisogna quindi avere installato MUSESCORE E AGGIORNARE LE STRINGHE IN BASE AL PROPRIO SISTEMA.
        """
    calculateLcsFunction()
