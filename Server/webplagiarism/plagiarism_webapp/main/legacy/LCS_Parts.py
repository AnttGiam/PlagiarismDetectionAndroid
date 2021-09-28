import music21 as m
import csv
import os
from music21 import *
from flask import current_app


us = environment.UserSettings()

# Versione L.C. # Path per il computer di L.C.
#us['musescoreDirectPNGPath'] = 'E:/Programs Installation/MuseScore 3/bin/MuseScore3.exe'
#us['musicxmlPath'] = 'E:/Programs Installation/MuseScore 3/bin/MuseScore3.exe'

# Versione D.D.S.  # Path per il computer di D.D.S.
# us['musescoreDirectPNGPath'] = 'C:/Program Files/MuseScore 3/bin/MuseScore3.exe'
# us['musicxmlPath'] = 'C:/Program Files/MuseScore 3/bin/MuseScore3.exe'


def readCsv():
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = 'datasetCouple2.csv'
        abs_file_path = os.path.join(script_dir, rel_path)  # <-- abbiamo così ottenuto un path funzionante
        with open(abs_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            rowCanzoni=[]
            for row in csv_reader:
                    rowCanzoni.append(row)

            rowCanzoni.pop(0)

            arrayDiStringhe =[]
            for i in range(len(rowCanzoni)):
                if(rowCanzoni[i]):
                        arrayDiStringhe.append(rowCanzoni[i])
            return arrayDiStringhe


def lcs(S,T):
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(S[i-c+1:i+1])

    return lcs_set



def calculateLcsFunction():
    arrayCouple=readCsv()
    song1 = str(arrayCouple[0])
    song2 = str(arrayCouple[1])

    song1 = song1.replace("[", "")
    song1 = song1.replace("]", "")
    song1 = song1.replace("'", "")

    #INSERIRE LETTURA DATASET COUPLE APPOSTO

    song2 = song2.replace("[", "")
    song2 = song2.replace("]", "")
    song2 = song2.replace("'", "")
  # print(song1)
  #  print(song2)

    counter = 0

    script_dir2 = os.path.dirname(__file__)  # <-- da dove si trova lo script ovvero : Legacy
    rel_path2 = 'parts'
    abs_file_path2 = os.path.join(script_dir2, rel_path2)  # <-- aggiungiamo parts -> Legacy/parts
    song_name1 = ''  # # aggiunta per risolvere il bug di viewlcs
    song_name2 = ''  # # aggiunta per risolvere il bug di viewlcs
    for file in os.listdir(abs_file_path2):
            try:
                if file.endswith((".xml")):
                  #  print("mxl file found:\t", file)
                    if (counter==0):
                        pathSong1 = os.path.join(abs_file_path2, file)  # './parts/'+file
                        song_name1, _ = os.path.splitext(file)  # prendiamo nome e estensione con il modulo os
                    if (counter==1):
                        pathSong2 = os.path.join(abs_file_path2, file)  # './parts/'+file
                        song_name2, _ = os.path.splitext(file)  # prendiamo nome e estensione con il modulo os

                    counter = counter + 1
            except Exception as e:
                raise e
             #   print("No files found here!")


    songC1 = m.converter.parse(pathSong1)
    songC2 = m.converter.parse(pathSong2)


    # test 1
    ret = lcs(song1,song2)
    cnt=0
    for s in ret:
        if (cnt==0):
            sottostringa=s
        cnt+=1

    #print (s)

   # print(ret)

   # print(sottostringa)
    l=len(sottostringa)
   # print(l)

  #  print(song1.find(sottostringa))
    indexSong1=song1.find(sottostringa)

   # print(song2.find(sottostringa))
    indexSong2=song2.find(sottostringa)

    for i in range(indexSong1,indexSong1+l):
        nota = songC1.recurse().notesAndRests[i]
        nota.style.color = '#cb3234'

    for i in range(indexSong2,indexSong2+l):
        nota = songC2.recurse().notesAndRests[i]
        nota.style.color = '#cb3234'

    #vecchia versione nostra aggiornata, abbiamo deciso di cambiare proprio e di salvarli in static
    #script_dir3 = os.path.dirname(__file__)  # <-- da dove si trova lo script ovvero : Legacy
    #rel_path3 = 'ColorPartsLCS1/PROCESS1.png'
    #rel_path4 = 'ColorPartsLCS2/PROCESS2.png'
    #process1_path = os.path.join(script_dir3, rel_path3)  # <-- aggiungiamo parts -> Legacy/parts
    #process2_path = os.path.join(script_dir3, rel_path4)  # <-- aggiungiamo parts -> Legacy/parts

    #test -> voglio salvarle in static
    process1_path = os.path.join(current_app.root_path, 'static/last_check_temp_files/color_parts_lcs1',
                                 'PROCESS1'+song_name1+'.png')
    process2_path = os.path.join(current_app.root_path, 'static/last_check_temp_files/color_parts_lcs2',
                                 'PROCESS2'+song_name2+'.png')

    songC1.write('musicxml.png', fp=process1_path)
    songC2.write('musicxml.png', fp=process2_path)




if __name__ == '__main__':
    calculateLcsFunction()
