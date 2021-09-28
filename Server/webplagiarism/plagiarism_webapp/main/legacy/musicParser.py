import music21 as m
import os
import csv


#Creo una nuova classe con lo scopo di poter generare una lista di canzoni con il
# parsing dell'MXL in string e vettore numerico di intervalli associato
class SongParse:
  def __init__(self, songName, songString):
    self.songName = songName
    self.songString = songString

class DurationObject:
  def __init__(self, d, cnt,perc):
    self.duration = d
    self.cntDuration = cnt
    self.percDuration = perc


songParseList=[]
minimi=[]


def search_min(song):

    minArray = []
    partStream = song.parts.stream()
    lenOfPart = partStream[0].recurse().notesAndRests
    nlenOfPart = len(lenOfPart)
    it = iter(range(0, nlenOfPart))

    for i in it:
        a = song.recurse().notesAndRests[i]
        if (a.isNote):
            minArray.append(a.duration.quarterLength)
        if (a.isChord):
            pitchPrec=0
            for x in a._notes:
                if (x.pitch.ps > pitchPrec):
                    pitchPrec = x.pitch.ps
                    pitchPrecD = x.duration.quarterLength

            minArray.append(pitchPrecD)

    minimo=min(minArray)
    return minimo

def generateDurationArray(song,l):
    arrayDuration =[]
    c4=0
    c2=0
    c1=0
    c05=0
    c25=0
    c125=0
    cntGeneral=0
    it = iter(range(0, l))

    for i in it:
        a = song.recurse().notesAndRests[i]
        print(a)
        if(a.isRest):
            print('nulla')
        if (a.isNote):
            d = a.duration.quarterLength
            d=float(d)
            print("DURATA:",d)
            if (d==4):
                c4=c4+1
                cntGeneral=cntGeneral+1
            if (d==2):
                c2=c2+2
                cntGeneral=cntGeneral+1
            if (d==1):
                c1=c1+1
                cntGeneral=cntGeneral+1
            if (d==0.5):
                c05=c05+1
                cntGeneral=cntGeneral+1
            if (d==0.25):
                c25=c25+1
                cntGeneral=cntGeneral+1
            if (d==0.125):
                c125=c125+1
                cntGeneral=cntGeneral+1

        if (a.isChord):
            pitchCorrente = 0;
            d=0;
            for x in a._notes:
                if (x.pitch.ps > pitchCorrente):
                    pitchCorrente = x.pitch.ps
                    d = x.duration.quarterLength
            if (d == 4):
                c4 = c4 + 1
                cntGeneral = cntGeneral + 1
            if (d == 2):
                c2 = c2 + 2
                cntGeneral = cntGeneral + 1
            if (d == 1):
                c1 = c1 + 1
                cntGeneral = cntGeneral + 1
            if (d == 0.5):
                c05 = c05 + 1
                cntGeneral = cntGeneral + 1
            if (d == 0.25):
                c25 = c25 + 1
                cntGeneral = cntGeneral + 1
            if (d == 0.125):
                c125 = c125 + 1
                cntGeneral = cntGeneral + 1

    print('CNTGENEARAL:',cntGeneral)
    print('C4',c4)


    perc4=c4/cntGeneral
    perc2=c2/cntGeneral
    perc1=c1/cntGeneral
    perc05=c05/cntGeneral
    perc25=c25/cntGeneral
    perc125=c125/cntGeneral

    arrayDuration.append(DurationObject(4,c4,perc4))
    arrayDuration.append(DurationObject(2,c2,perc2))
    arrayDuration.append(DurationObject(1,c1,perc1))
    arrayDuration.append(DurationObject(0.5,c05,perc05))
    arrayDuration.append(DurationObject(0.25,c25,perc25))
    arrayDuration.append(DurationObject(0.125,c125,perc125))


    return arrayDuration

def generateCSV():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = 'datasetCouple.csv'
    abs_file_path = os.path.join(script_dir, rel_path)  # <-- abbiamo così ottenuto un path funzionante
    with open(abs_file_path, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['N','SongName', 'SongString'])
        i=1
        for song in songParseList:
            filewriter.writerow([i,song.songName,song.songString])
            i=i+1

        script_dir2 = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path2 = 'minimisoglia003.csv'
        abs_file_path2 = os.path.join(script_dir2, rel_path2)  # <-- abbiamo così ottenuto un path funzionante
        with open(abs_file_path2, 'w') as csvfile2:
            filewriter = csv.writer(csvfile2, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['MINIMO'])
            i = 1
            for min in minimi:
                filewriter.writerow([min])
                i = i + 1

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
            if file.endswith((".mid",".mxl",".xml")):
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

def pauseSearch(noteOrRests,ind,delete):
    if (ind<=-1):
        return -1;
    if (noteOrRests[ind].isNote):
        a=noteOrRests[ind]
        d=a.duration.quarterLength
        for i in range(0,len(delete)):
            if (d==delete[i]):
                pauseSearch(noteOrRests, ind - 1,delete)
        print("termina")
        return ind
    if (noteOrRests[ind].isChord):
        print("termina")
        return ind
    if (noteOrRests[ind].isRest):
        return pauseSearch(noteOrRests,ind-1,delete)


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
    delete=[]
    durationArray=generateDurationArray(song,nlenOfPart)
    minD=0.125
    soglia=0.03
    print(durationArray)
    print(durationArray[0].duration," ",durationArray[0].cntDuration," ",durationArray[0].percDuration)
    print(durationArray[1].duration," ",durationArray[1].cntDuration," ",durationArray[1].percDuration)
    print(durationArray[2].duration," ",durationArray[2].cntDuration," ",durationArray[2].percDuration)
    print(durationArray[3].duration," ",durationArray[3].cntDuration," ",durationArray[3].percDuration)
    print(durationArray[4].duration, " ", durationArray[4].cntDuration," ",durationArray[4].percDuration)
    print(durationArray[5].duration," ",durationArray[5].cntDuration," ",durationArray[5].percDuration)

    if (durationArray[5].percDuration>=soglia):
        minD=0.125
    else:
        delete.append(0.125)
        if (durationArray[4].percDuration>=soglia):
            minD = 0.25
        else:
            delete.append(0.25)
            if (durationArray[3].percDuration >= soglia):
                minD = 0.5
            else:
                delete.append(0.5)
                if (durationArray[2].percDuration >= soglia):
                    minD = 1
                else:
                    delete.append(1)
                    if (durationArray[1].percDuration >= soglia):
                        minD = 2
                    else:
                        delete.append(2)
                        if (durationArray[0].percDuration >= soglia):
                            minD = 4

    print("MIND: ",minD)

    minimi.append(minD)



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

        if (i==1):
            #durationFirstNote
            d = a.duration.quarterLength
            # Calcola il numero di caratteri consecutivi da inserire dopo la differenza nell'intervallo
            # dividendo la durata della seconda nota della differenza per la durata minima dell'intero spartito

            cntB=d/minD

            cntB= int(cntB)
            sb = ''
            for j in range(0, cntB):
                sb = sb + 'b'

            s2=s2+sb

        # print(a)
        print('... ', i, ' ...')

        if (a.isRest):
            print("PAUSA")

            d = a.duration.quarterLength
            cntB=d/minD

            cntB= int(cntB)
            sb = ''
            for j in range(0, cntB):
                sb = sb + 'b'

            s2=s2+'p'+sb


            indUtileForward = pauseSearchForward(song.recurse().notesAndRests, i + 1,nlenOfPart)
            print("indice utile: ", indUtileForward)
            if (indUtileForward<=-1):
                break
            #Dopo aver ricercato l'indice il programma salta direttamente alla prima nota utile dopo la pausa
            for j in range(i, indUtileForward - 1):
                next(it)
            i = indUtileForward

        if (a.isNote):

            if (a.tie != None):
                if(a.tie.type=='start'):
                    print(a.tie.type)
                    tieDuration=0
                    d = a.duration.quarterLength
                    if (d == 4):
                        tieDuration=tieDuration+4
                    if (d==3):
                        tieDuration =tieDuration+ 3
                    if (d == 2):
                        tieDuration =tieDuration+ 2
                    if (d==1.5):
                        tieDuration = tieDuration+1.5
                    if (d == 1):
                        tieDuration = tieDuration+1
                    if (d == 0.5):
                        tieDuration = tieDuration+0.5
                    if (d==0.75):
                        tieDuration =tieDuration+0.75
                    if (d == 0.25):
                        tieDuration =tieDuration+ 0.25
                    continue;

            if (a.tie != None):
                if(a.tie.type=='stop'):
                    print(a.tie.type)
                    d = a.duration.quarterLength
                    if (d == 4):
                        tieDuration=tieDuration+4
                    if (d==3):
                        tieDuration =tieDuration+ 3
                    if (d == 2):
                        tieDuration =tieDuration+ 2
                    if (d==1.5):
                        tieDuration = tieDuration+1.5
                    if (d == 1):
                        tieDuration = tieDuration+1
                    if (d == 0.5):
                        tieDuration = tieDuration+0.5
                    if (d==0.75):
                        tieDuration =tieDuration+ 0.75
                    if (d == 0.25):
                        tieDuration =tieDuration+ 0.25

                    indUtile = i-3

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

                            d = a.duration.quarterLength
                            d=int(d)
                            tieDuration=tieDuration+d

                            cntB = tieDuration / minD

                            cntB = int(cntB)
                            sb = ''
                            for j in range(0, cntB):
                                sb = sb + 'b'

                            pitchPrec = max;
                            pitchDiff = pitchCorrente - pitchPrec
                            pitchDiff = round(pitchDiff)
                            if (pitchDiff > 0):
                                pitchDiffString = str(pitchDiff)
                                pitchDiffString = '+' + pitchDiffString
                                s2 = s2 + pitchDiffString + sb + '*';

                            else:
                                pitchDiff = str(pitchDiff)
                                s2 = s2 + pitchDiff + sb + '*';

                        if (song.recurse().notesAndRests[indUtile].isNote):
                            cntB = tieDuration / minD

                            cntB = int(cntB)
                            sb = ''
                            for j in range(0, cntB):
                                sb = sb + 'b'

                            pitchCorrente = a.pitch.ps
                            pitchPrec = song.recurse().notesAndRests[indUtile].pitch.ps;
                            print("OPERAZIONE: ", pitchCorrente, " - ", pitchPrec)
                            pitchDiff = pitchCorrente - pitchPrec
                            # Cast from Float to String
                            pitchDiff = round(pitchDiff)
                            if (pitchDiff > 0):
                                pitchDiffString = str(pitchDiff)
                                pitchDiffString = '+' + pitchDiffString
                                s2 = s2 + pitchDiffString + sb + '*';
                            else:
                                pitchDiff = str(pitchDiff)
                                s2 = s2 + pitchDiff + sb + '*';
            if (a.tie == None):

                print("NOTA")
                print("indice utile aggiornato in note: ", i)
                indUtile = pauseSearch(song.recurse().notesAndRests, i - 1,delete)
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
                        d = a.duration.quarterLength

                        cntB = d / minD

                        cntB = int(cntB)
                        sb = ''
                        for j in range(0, cntB):
                            sb = sb + 'b'


                        pitchPrec = max;
                        pitchDiff = pitchCorrente - pitchPrec
                        pitchDiff = round(pitchDiff)
                        if (pitchDiff>0):
                            pitchDiffString =str(pitchDiff)
                            pitchDiffString='+'+pitchDiffString
                            s2 = s2 + pitchDiffString +sb+ '*';

                        else:
                            pitchDiff = str(pitchDiff)
                            s2 = s2 + pitchDiff +sb+ '*';

                    if (song.recurse().notesAndRests[indUtile].isNote):
                        d = a.duration.quarterLength

                        cntB = d / minD

                        cntB = int(cntB)
                        sb = ''
                        for j in range(0, cntB):
                            sb = sb + 'b'


                        pitchCorrente = a.pitch.ps
                        pitchPrec = song.recurse().notesAndRests[indUtile].pitch.ps;
                        print("OPERAZIONE: ", pitchCorrente, " - ", pitchPrec)
                        pitchDiff = pitchCorrente - pitchPrec
                        # Cast from Float to String
                        pitchDiff = round(pitchDiff)
                        if (pitchDiff > 0):
                          pitchDiffString = str(pitchDiff)
                          pitchDiffString = '+' + pitchDiffString
                          s2 = s2 + pitchDiffString +sb+ '*';
                        else:
                          pitchDiff = str(pitchDiff)
                          s2 = s2 + pitchDiff +sb+ '*';

                x = a;
                s = getMusicProperties(x);
                print(s);

        if (a.isChord):
                print("ACCORDO")
                for x in a._notes:
                    s = getMusicProperties(x);
                    print(s);

                indUtile = pauseSearch(song.recurse().notesAndRests, i - 1,delete)
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

                        cntB = pitchCorrenteD / minD

                        cntB = int(cntB)
                        sb = ''
                        for j in range(0, cntB):
                            sb = sb + 'b'




                        pitchDiff = pitchCorrente - pitchPrec
                        pitchDiff = round(pitchDiff)
                        if (pitchDiff > 0):
                          pitchDiffString = str(pitchDiff)
                          pitchDiffString = '+' + pitchDiffString
                          s2 = s2 + pitchDiffString +sb +'*';
                        else:
                          pitchDiff = str(pitchDiff)
                          s2 = s2 + pitchDiff + sb+'*';



                    if (song.recurse().notesAndRests[indUtile].isNote):
                        pitchCorrente = 0;
                        pitchCorrenteD = 0;

                        for x in a._notes:
                            if (x.pitch.ps > pitchCorrente):
                                pitchCorrente = x.pitch.ps
                                pitchCorrenteD = x.duration.quarterLength
                                notaChord = x

                        cntB = pitchCorrenteD / minD

                        cntB = int(cntB)
                        sb = ''
                        for j in range(0, cntB):
                            sb = sb + 'b'

                        pitchPrec = song.recurse().notesAndRests[indUtile].pitch.ps;

                        pitchDiff = pitchCorrente - pitchPrec
                        # Cast from Float to String
                        pitchDiff = round(pitchDiff)
                        if (pitchDiff > 0):
                          pitchDiffString = str(pitchDiff)
                          pitchDiffString = '+' + pitchDiffString
                          s2 = s2 + pitchDiffString +sb+'*';
                        else:
                          pitchDiff = str(pitchDiff)
                          s2 = s2 + pitchDiff +sb+ '*';




    # s2=s2.replace("p*p","p")
    # s2=s2.replace("p*p*p","p")
    # s2=s2.replace("p*p*p*p","p")
    s2= s2.replace("*", "");
    #s2= s2.replace("+", "");
    #s2= s2.replace("p", "");

    print(s2)

    #generateSongArray(s2)

    #Aggiungo un nuovo elemento nella lista delle canzoni di cui ho effettuato il Parsing
    songParseList.append(SongParse(songName,s2))

    print("Done.")


def music_parser_legacy(foldername='parts'):
    songParseList.clear()  # All'inizio ripulisco le liste!!! Ecco cosa causava il problema
    minimi.clear()
    tieDuration = 0  # lo lascio perchè c'era da legacy, ma è inutile

    folderRead(foldername)


if __name__ == '__main__':
    music_parser_legacy()
