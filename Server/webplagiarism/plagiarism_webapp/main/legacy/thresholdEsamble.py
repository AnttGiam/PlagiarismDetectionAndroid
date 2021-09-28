from itertools import combinations
import numpy as np
import csv
import os


#calcola i valori soglia e li salva all'interno di un csv
def threshold(nameCsvInput,t,p,n, k,contoDi0,contoDi01,contoDi02,contoDi03,contoDi04,contoDi05,contoDi06,contoDi07,contoDi08,contoDi09,contoDi1 ):

     arrayThreshold= [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,0.9, 1]
     arrayDataset = readCSV(nameCsvInput)
     lenArray= len(arrayDataset)
     tp = []

     if(k==-1):
         variabile=1
     else:
         for i in range (0,lenArray):
             value=float(arrayDataset[i][t])
             valueRound = round(value,1)
             valueTwo=float(arrayDataset[i][p])
             valueRoundTwo = round(valueTwo,1)
             valueThree = float(arrayDataset[i][n])
             valueRoundThree= round(valueThree,1)
             sum = valueRound+ valueRoundTwo+ valueRoundThree
             mean = sum/3
             tp.append(round(mean,1))

         for j in range(0, len(tp)):
             if(k==11 and j==0):
                break
             if(tp[j] == arrayThreshold[k]):
                 if(tp[j] == 0.1):
                    contoDi0 +=1
                 if(tp[j] == 0.1):
                    contoDi01 +=1
                 if(tp[j] == 0.2):
                   contoDi02 +=1
                 if(tp[j] == 0.3):
                   contoDi03 +=1
                 if(tp[j] == 0.4):
                     contoDi04 +=1
                 if(tp[j]==0.5):
                    contoDi05 +=1
                 if(tp[j]==0.6):
                    contoDi06 +=1
                 if(tp[j]==0.7):
                      contoDi07 +=1
                 if(tp[j]==0.8):
                      contoDi08 +=1
                 if(tp[j]==0.9):
                      contoDi09 +=1
                 if(tp[j]==1):
                      contoDi1 +=1
             k+=1
             if(k==11):
                k=0
             if(j == len(arrayDataset)-1):
                     if(k==10):
                         nameCsv = "pareto" + str(t) + str(p) + str(n)+".csv"
                         generateCSV(nameCsv,contoDi0, contoDi01,contoDi02,contoDi03,contoDi04,contoDi05,contoDi06,contoDi07,contoDi08,contoDi09,contoDi1)
                         threshold(nameCsvInput,t,p,n,-1,0,0,0,0,0,0,0,0,0,0,0)
                     k+=1
                     threshold(nameCsvInput,t,p,n,k,contoDi0,contoDi01,contoDi02,contoDi03,contoDi04,contoDi05,contoDi06,contoDi07,contoDi08,contoDi09,contoDi1)


#genera il numpyarray per calcolare il pareto front
def generateNP(nFile):
    array=[]
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = 'ensamble/'+nFile
    abs_file_path = os.path.join(script_dir, rel_path) # <-- creiamo il path assoluto
    with open(abs_file_path) as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
                array.append(row)
        firstString = array[0][0]
        secondString = array[2][0]
        first = int(firstString)
        second = int(secondString)
        b = np.array([[first,second]])

        for i in range(1,len(array[0])):
            firstString=array[0][i]
            secondString=array[2][i]
            first= int(firstString)
            second= int(secondString)
            b=np.append(b,[[first,second]],0)

        return b


#permette di leggere i csv dei dataset su cui si vuole effettuare l'analisi
def readCSV(nameCsv):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = nameCsv
    abs_file_path = os.path.join(script_dir, rel_path) # <-- abbiamo così ottenuto un path funzionante
    with open(abs_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        rowCanzoni=[]
        i=0
        for row in csv_reader:
             rowCanzoni.append(row)
        rowCanzoni.pop(0)
        arrayDiStringhe =[]
        for i in range(len(rowCanzoni)):
            if(rowCanzoni[i]):
                    arrayDiStringhe.append(rowCanzoni[i])

    return arrayDiStringhe


#permette di generare i csv per il pareto front
def generateCSV(nameCsv,contoDi0, contoDi01,contoDi02,contoDi03,contoDi04,contoDi05,contoDi06,contoDi07,contoDi08,contoDi09,contoDi1):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = 'ensamble/'+nameCsv
    abs_file_path = os.path.join(script_dir, rel_path) # <-- costruiamo il path completo
    with open(abs_file_path, 'a') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quoting=csv.QUOTE_MINIMAL)

        filewriter.writerow([contoDi0, contoDi01,contoDi02,contoDi03,contoDi04,contoDi05,contoDi06,contoDi07,contoDi08,contoDi09,contoDi1])



#calcola il pareto front
def identify_pareto(scores):
    # Count number of items
    population_size = scores.shape[0]
    # Create a NumPy index for scores on the pareto front (zero indexed)
    population_ids = np.arange(population_size)
    # Create a starting list of items on the Pareto front
    # All items start off as being labelled as on the Parteo front
    pareto_front = np.ones(population_size, dtype=bool)
    # Loop through each item. This will then be compared with all other items
    for i in range(population_size):
        # Loop through all other items
        for j in range(population_size):
            # Check if our 'i' pint is dominated by out 'j' point
            if all(scores[j] >= scores[i]) and any(scores[j] > scores[i]):
                # j dominates i. Label 'i' point as not on Pareto front
                pareto_front[i] = 0
                # Stop further comparisons with 'i' (no more comparisons needed)
                break

    # Return ids of scenarios on pareto front
    if(len(population_ids[pareto_front]) >= 3):
        if(population_ids[pareto_front][1]<=4):
            return population_ids[pareto_front][2]
        else:
             return population_ids[pareto_front][1]
    if(len(population_ids[pareto_front]) == 2):
        if(population_ids[pareto_front][0]<=4):
             return population_ids[pareto_front][1]
        else:
             return population_ids[pareto_front][0]
    if(len(population_ids[pareto_front]) == 3):
        return population_ids[pareto_front][2]
    if(len(population_ids[pareto_front]) == 1):
          return population_ids[pareto_front][0]



def main():
         #i numeri in array Metrics rappresentano rispettivamente coseno, jaccard, sor dice, overlap, jaro
         arrayMetrics= [4,5,6,7,8]
         arrayAllPareto =[]
         arrayAllCombinazioni =[]
         #creo un array di 3 combinazioni
         comb = combinations(arrayMetrics, 3)
         for i in list(comb):
            combinations1 = i[0]
            combinations2= i[1]
            combinations3= i[2]
            #calcolo le threshold per ogni combinazione
            threshold("datasetTP.csv" ,combinations1,combinations2,combinations3,0,0,0,0,0,0,0,0,0,0,0,0)
            threshold("datasetFP.csv",combinations1,combinations2,combinations3, 0,0,0,0,0,0,0,0,0,0,0,0)
            #creo un array per tracciare le combinazioni
            if(combinations1 == 4 and combinations2 == 5 and combinations3==6):
               arrayAllCombinazioni.append("cosine" + "/jaccard" + "/sordice")
            if(combinations1 == 4 and combinations2 == 5 and combinations3==7):
               arrayAllCombinazioni.append("cosine" + "/jaccard" + "/overlap")
            if(combinations1 == 4 and combinations2 == 5 and combinations3==8):
               arrayAllCombinazioni.append("cosine" + "/jaccard" + "/jaro")
            if(combinations1 == 4 and combinations2 == 6 and combinations3==7):
               arrayAllCombinazioni.append("cosine" + "/sordice" + "/overlap")
            if(combinations1 == 4 and combinations2 == 6 and combinations3==8):
               arrayAllCombinazioni.append("cosine" + "/sordice" + "/jaro")
            if(combinations1 == 4 and combinations2 == 7 and combinations3==8):
               arrayAllCombinazioni.append("cosine" + "/overlap" + "/jaro")
            if(combinations1 == 6 and combinations2 == 7 and combinations3==8):
               arrayAllCombinazioni.append("sordice" + "/overlap" + "/jaro")
            if(combinations1 == 5 and combinations2 == 6 and combinations3==7):
               arrayAllCombinazioni.append("jaccard" + "/sordice" + "/overlap")
            if(combinations1 == 5 and combinations2 == 6 and combinations3==8):
               arrayAllCombinazioni.append("jaccard" + "/sordice" + "/jaro")
            if(combinations1 == 5 and combinations2 == 7 and combinations3==8):
               arrayAllCombinazioni.append("jaccard" + "/overlap" + "/jaro")
            #genero la stringa con il nome del csv per costruire il numpy array
            nameCsv = "pareto" + str(combinations1) + str(combinations2) + str(combinations3)+".csv"
            #genero numpyArray
            scores=generateNP(nameCsv)
            #genero il pareto front
            scorePareto =identify_pareto(scores)
            arrayAllPareto.append(scorePareto)

         return arrayAllCombinazioni,arrayAllPareto



