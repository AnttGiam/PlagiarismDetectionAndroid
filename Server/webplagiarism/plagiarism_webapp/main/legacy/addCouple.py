import plagiarism_webapp.main.legacy.metriche as mt
import csv
import os
import sys

def generateCSV(nameCsv, songNameOne, songNameTwo, rap1, rap2, cosinedistance,jaccard,sorensen_dice,overlap_coe,jaro,clustering):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = nameCsv
    abs_file_path = os.path.join(script_dir, rel_path)  # <-- abbiamo così ottenuto un path funzionante
    with open(abs_file_path, 'a') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)

        filewriter.writerow([songNameOne, songNameTwo,rap1, rap2 , cosinedistance,jaccard,sorensen_dice,overlap_coe,
                        jaro,clustering])



def folderRead(folderName):
    counter = 0  # keep a count of all files found

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = folderName
    abs_file_path = os.path.join(script_dir, rel_path)  # <-- creiamo il path assoluto
    for file in os.listdir(abs_file_path):
        try:
            if file.endswith((".xml")):
                print("xml file found:\t", file)
                if(counter == 0):
                        nameSong1 = file
                if(counter == 1):
                        nameSong2 = file
                counter = counter + 1
        except Exception as e:
            raise e
            print("No files found here!")

    print("Total files found:\t", counter)
    return nameSong1, nameSong2


def add_couple_main(clustering_value, result_of_confrontation):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "datasetCouple.csv"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rowCanzoni = []
        for row in csv_reader:
            rowCanzoni.append(row)

        rowCanzoni.pop(0)

        arrayDiStringhe = []
        for i in range(len(rowCanzoni)):
            if (rowCanzoni[i]):
                arrayDiStringhe.append(rowCanzoni[i])
        rap1 = str(arrayDiStringhe[0])
        rap2 = str(arrayDiStringhe[1])

    rap1 = rap1.replace("[", "")
    rap1 = rap1.replace("]", "")
    rap1 = rap1.replace("'", "")

    rap2 = rap2.replace("[", "")
    rap2 = rap2.replace("]", "")
    rap2 = rap2.replace("'", "")

    nameSong1, nameSong2 = folderRead('parts')

    nameSong1R = nameSong1.replace(".xml", "")
    nameSong2R = nameSong2.replace(".xml", "")

    cosinedistance = mt.coseno(rap1, rap2)
    overlap_coe = mt.overlap_coe(rap1, rap2)
    jaro = mt.jaro(rap1, rap2)
    soresen_dice = mt.dice_coef(rap1, rap2)
    jaccard = mt.jaccard(rap1, rap2)

    clustering = clustering_value
    csvNome = result_of_confrontation

    if (csvNome == "TP"):
        if (clustering == "0" or clustering == "1"):
            generateCSV("datasetTP.csv", nameSong1R, nameSong2R, rap1, rap2, cosinedistance, jaccard, soresen_dice,
                        overlap_coe, jaro, clustering)

        if (clustering == "2"):
            generateCSV("datasetTP.csv", nameSong1R, nameSong2R, rap1, rap2, cosinedistance, jaccard, soresen_dice,
                        overlap_coe, jaro, 1)

    if (csvNome == "FP"):
        if (clustering == "0" or clustering == "1"):
            generateCSV("datasetFP.csv", nameSong1R, nameSong2R, rap1, rap2, cosinedistance, jaccard, soresen_dice,
                        overlap_coe, jaro, clustering)

        if (clustering == "2"):
            generateCSV("datasetFP.csv", nameSong1R, nameSong2R, rap1, rap2, cosinedistance, jaccard, soresen_dice,
                        overlap_coe, jaro, 0)


