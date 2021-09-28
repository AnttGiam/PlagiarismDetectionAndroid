import music21 as m
import os
import csv


#Creo una nuova classe con lo scopo di poter generare una lista di canzoni con il
# parsing dell'MXL in string e vettore numerico di intervalli associato
class SongParse:
  def __init__(self, songName, songString):
    self.songName = songName
    self.songString = songString

songParseList=[]


def generateCSV():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = 'datasetCouple2.csv'
    abs_file_path = os.path.join(script_dir, rel_path)  # <-- abbiamo così ottenuto un path funzionante
    with open(abs_file_path, 'w') as csvfile:

        filewriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['N','SongName', 'SongString'])
        i=1
        for song in songParseList:
            filewriter.writerow([song.songString])
            i=i+1

def folderRead(folderName):
    location = os.getcwd()  # get present working directory location here
    counter = 0  # keep a count of all files found
    csvfiles = []  # list to store all csv files found at location
    filebeginwithhello = []  # list to keep all files that begin with 'hello'
    otherfiles = []  # list to keep any other file that do not match the criteria

    script_dir = os.path.dirname(__file__)  # <-- da dove si trova lo script ovvero : Legacy
    rel_path = folderName
    abs_file_path = os.path.join(script_dir, rel_path)  # <-- aggiungiamo parts -> Legacy/parts
    for file in os.listdir(abs_file_path):
        try:
            if file.endswith((".mid",".mxl", ".xml")):
                print("mxl file found:\t", file)
                generateString(file,folderName);
                csvfiles.append(str(file))
                counter = counter + 1
        except Exception as e:
            raise e
            print("No files found here!")

    print("Total files found:\t", counter)

    generateCSV();
    print("-------- END ----------")
    return csvfiles  # aggiunta per leggere i nomi dei files

def generateSongArray(songString):
    for letter in songString:
        print(letter)

def getMusicProperties(x):
    s = '';
    t='';
    s = str(x.pitch) + ", " + str(x.duration.type) + ", " + str(x.duration.quarterLength);
    s += ", "
    if x.tie != None:
        t = x.tie.type;
    s += t + ", " + str(x.pitch.ps) + ", " + str(x.octave); # + str(x.seconds)  # x.seconds not always there
    return s

def pauseSearch(noteOrRests,ind):
    if (ind<=-1):
        return -1;
    if (noteOrRests[ind].isNote):
        print("termina")
        return ind
    if (noteOrRests[ind].isChord):
        print("termina")
        return ind
    if (noteOrRests[ind].isRest):
        return pauseSearch(noteOrRests,ind-1)


def pauseSearchForward(noteOrRests,ind,nlenOfPart):
    print("SONO NELLA RICORSIONE")
    print("LUNGHEZZA :  ",nlenOfPart)
    if(ind>=nlenOfPart):
        return -1
    if (noteOrRests[ind].isRest):
        return  pauseSearchForward(noteOrRests,ind+1,nlenOfPart)
    if (noteOrRests[ind].isNote):
        print("termina")
        return ind
    if (noteOrRests[ind].isChord):
        print("termina")
        return ind


def generateString(songName,folderName):
    script_dir3 = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path3 = folderName+"/"+songName
    abs_file_path3 = os.path.join(script_dir3, rel_path3)  # <-- abbiamo così ottenuto un path funzionante
    path = abs_file_path3
    song = m.converter.parse(path)
    i = 0;

    s2 = '';
    s3='';
    # Snippet per recuperare il numero di note del primo spartito
    # partStream è l' array degli strumenti
    # parStream[0] rappresenta il primo spartito
    partStream = song.parts.stream()
    # print(partStream[0])
    # Questa riga sottostante permette di recuperare il numero di note del primo spartito (o primo strumento)
    # NB: nel numero totale sono incluse anche le pause (oltre le note effettive)
    lenOfPart = partStream[0].recurse().notesAndRests
    # print(len(lenOfPart))
    nlenOfPart = len(lenOfPart)
    # for p in partStream:
    #  print(p.id)

    it = iter(range(0, nlenOfPart))

    print('pitch, duration_string, duration, tie, midi pitch, octave')
    for i in it:
        a = song.recurse().notesAndRests[i]
        # print(a)
        print('... ', i, ' ...')

        if (a.isRest):
            print("PAUSA")
            s2 = s2 + "p*"
            indUtileForward = pauseSearchForward(song.recurse().notesAndRests, i + 1,nlenOfPart)
            print("indice utile: ", indUtileForward)
            if (indUtileForward<=-1):
                break
            #Dopo aver ricercato l'indice il programma salta direttamente alla prima nota utile dopo la pausa
            for j in range(i, indUtileForward - 1):
                next(it)
            i = indUtileForward

        if (a.isNote):
            print("NOTA")
            print("indice utile aggiornato in note: ", i)
            indUtile = pauseSearch(song.recurse().notesAndRests, i - 1)
            print("INDICE :", indUtile)
            if (indUtile <= -1):
                print("NON FARE NULLA")
            else:
                if (song.recurse().notesAndRests[indUtile].isChord):
                    max = 0;
                    maxDur = 0;
                    for x in song.recurse().notesAndRests[indUtile]._notes:
                        if (x.pitch.ps > max):
                            max = x.pitch.ps
                            maxD = x.duration.quarterLength

                    pitchCorrente = a.pitch.ps
                    pitchPrec = max;
                    pitchDiff = pitchCorrente - pitchPrec
                    pitchDiff = round(pitchDiff)
                    if (pitchDiff>0):
                        pitchDiffString =str(pitchDiff)
                        pitchDiffString='+'+pitchDiffString
                        s2 = s2 + pitchDiffString + '*';

                    else:
                        pitchDiff = str(pitchDiff)
                        s2 = s2 + pitchDiff + '*';




                if (song.recurse().notesAndRests[indUtile].isNote):
                    pitchCorrente = a.pitch.ps
                    pitchPrec = song.recurse().notesAndRests[indUtile].pitch.ps;
                    print("OPERAZIONE: ", pitchCorrente, " - ", pitchPrec)
                    pitchDiff = pitchCorrente - pitchPrec
                    # Cast from Float to String
                    pitchDiff = round(pitchDiff)
                    if (pitchDiff > 0):
                      pitchDiffString = str(pitchDiff)
                      pitchDiffString = '+' + pitchDiffString
                      s2 = s2 + pitchDiffString + '*';
                    else:
                      pitchDiff = str(pitchDiff)
                      s2 = s2 + pitchDiff + '*';

            x = a;
            s = getMusicProperties(x);
            print(s);

        if (a.isChord):
            print("ACCORDO")
            for x in a._notes:
                s = getMusicProperties(x);
                print(s);

            indUtile = pauseSearch(song.recurse().notesAndRests, i - 1)
            if (indUtile <= -1):
                print("NON FARE NULLA")
            else:
                if (song.recurse().notesAndRests[indUtile].isChord):
                    pitchPrec = 0;
                    pitchPrecD = 0;
                    for x in song.recurse().notesAndRests[indUtile]._notes:
                        if (x.pitch.ps > pitchPrec):
                            pitchPrec = x.pitch.ps
                            pitchPrecD = x.duration.quarterLength
                            notaChord = x

                    pitchCorrente = 0;
                    pitchCorrenteD = 0;
                    for x in a._notes:
                        if (x.pitch.ps > pitchCorrente):
                            pitchCorrente = x.pitch.ps
                            pitchCorrenteD = x.duration.quarterLength
                            notaChord = x

                    pitchDiff = pitchCorrente - pitchPrec
                    pitchDiff = round(pitchDiff)
                    if (pitchDiff > 0):
                      pitchDiffString = str(pitchDiff)
                      pitchDiffString = '+' + pitchDiffString
                      s2 = s2 + pitchDiffString + '*';
                    else:
                      pitchDiff = str(pitchDiff)
                      s2 = s2 + pitchDiff + '*';



                if (song.recurse().notesAndRests[indUtile].isNote):
                    pitchCorrente = 0;
                    pitchCorrenteD = 0;
                    for x in a._notes:
                        if (x.pitch.ps > pitchCorrente):
                            pitchCorrente = x.pitch.ps
                            pitchCorrenteD = x.duration.quarterLength
                            notaChord = x

                    pitchPrec = song.recurse().notesAndRests[indUtile].pitch.ps;

                    pitchDiff = pitchCorrente - pitchPrec
                    # Cast from Float to String
                    pitchDiff = round(pitchDiff)
                    if (pitchDiff > 0):
                      pitchDiffString = str(pitchDiff)
                      pitchDiffString = '+' + pitchDiffString
                      s2 = s2 + pitchDiffString + '*';
                    else:
                      pitchDiff = str(pitchDiff)
                      s2 = s2 + pitchDiff + '*';





    # s2=s2.replace("p*p","p")
    # s2=s2.replace("p*p*p","p")
    # s2=s2.replace("p*p*p*p","p")
    s2= s2.replace("*", "");

    print(s2)

    #generateSongArray(s2)

    #Aggiungo un nuovo elemento nella lista delle canzoni di cui ho effettuato il Parsing
    songParseList.append(SongParse(songName,s2))

    print("Done.")


def music_parser2_legacy(foldername='parts'):
    songParseList.clear()  # All'inizio ripulisco la lista
    csvfiles = folderRead(foldername)
    file_name1, _ = os.path.splitext(csvfiles[0])  # prendiamo nome e estensione con il modulo os
    file_name2, _ = os.path.splitext(csvfiles[1])  # prendiamo nome e estensione con il modulo os
    return file_name1, file_name2



if __name__ == '__main__':
    music_parser2_legacy()
