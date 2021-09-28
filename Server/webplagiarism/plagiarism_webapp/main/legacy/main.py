import csv
import plagiarism_webapp.main.legacy.thresholdEsamble as se
import plagiarism_webapp.main.legacy.metriche as mt
import plagiarism_webapp.main.legacy.spectClustering as sp
import os


#variabile globale (aggiunta) per dare un valore di restituzione
dizionario_info_da_restituire = {
        "ValoreMetrica1": 0.1,
        "ValoreMetrica2": 0.2,
        "ValoreMetrica3": 0.3,
        "ValoreClustering": 2,  # valore base clustering non partito
        "Metrica1": "m1",
        "Metrica2": "m2",
        "Metrica3": "m3",
        "Threshold": 0.0
    }


class ObjFeature:
  def __init__(self,cosine,overlap,jaro):
    self.cosine = cosine
    self.overlap = overlap
    self.jaro = jaro



#generazione della combinazione migliore in base al dataset in input
def generateBestCombination(nameCsv,valueCorr, finalValue, oneCombination,twoCombination,threeCombination,fourCombination,fiveCombination,sixCombination,sevenCombination,eightCombination,nineCombination,tenCombination) :
                arrayTP = readCSV(nameCsv)
                value= valueCorr
                count = 0
                count2 =0
                for i in range(0, len(arrayTP)):
                    if(value==1):
                     cosine=arrayTP[i][4]
                     jaccard = arrayTP[i][5]
                     sordice= arrayTP[i][6]
                     clustering= arrayTP[i][9]
                     threshold=oneCombination[3]/10
                     if(float(cosine) >= threshold or float(jaccard) >= threshold or float(sordice) >=threshold):
                         if(float(cosine) >= threshold and float(jaccard) >= threshold and float(sordice) >=threshold):
                               count2+=1
                         else:
                            if(int(clustering) == 1):
                                count+=1

                    if(value==2):

                     cosine=arrayTP[i][4]
                     jaccard = arrayTP[i][5]
                     overlap= arrayTP[i][7]
                     clustering= arrayTP[i][9]
                     threshold=twoCombination[3]/10
                     if(float(cosine) >= threshold or float(jaccard) >= threshold or float(overlap) >=threshold):
                         if(float(cosine) >= threshold and float(jaccard) >= threshold and float(overlap) >=threshold):
                               count2+=1
                         else:
                            if(int(clustering) == 1):
                                count+=1


                    if(value==3):

                     cosine=arrayTP[i][4]
                     jaccard = arrayTP[i][5]
                     jaro= arrayTP[i][8]
                     clustering= arrayTP[i][9]
                     threshold=threeCombination[3]/10
                     if(float(cosine) >= threshold or float(jaccard) >= threshold or float(jaro) >=threshold):
                         if(float(cosine) >= threshold and float(jaccard) >= threshold and float(jaro) >=threshold):
                               count2+=1
                         else:
                            if(int(clustering) == 1):
                                     count+=1


                    if(value==4):
                         sordice = arrayTP[i][6]
                         cosine=arrayTP[i][4]
                         overlap= arrayTP[i][7]
                         clustering= arrayTP[i][9]
                         threshold=fourCombination[3]/10
                         if(float(sordice) >= threshold or float(cosine) >= threshold or float(overlap) >=threshold):
                             if(float(sordice) >= threshold and float(cosine) >= threshold and float(overlap) >=threshold):
                                   count2+=1
                             else:
                                  if(int(clustering) == 1):
                                      count+=1
                    if(value==5):
                         sordice = arrayTP[i][6]
                         cosine=arrayTP[i][4]
                         jaro= arrayTP[i][8]
                         clustering= arrayTP[i][9]
                         threshold=fiveCombination[3]/10
                         if(float(sordice) >= threshold or float(cosine) >= threshold or float(jaro) >=threshold):
                             if(float(sordice) >= threshold and float(cosine) >= threshold and float(jaro) >=threshold):
                                   count2+=1
                             else:
                                  if(int(clustering) == 1):
                                      count+=1

                    if(value==6):
                         overlap= arrayTP[i][7]
                         cosine=arrayTP[i][4]
                         jaro= arrayTP[i][8]
                         clustering= arrayTP[i][9]
                         threshold=fiveCombination[3]/10
                         if(float(overlap) >= threshold or float(cosine) >= threshold or float(jaro) >=threshold):
                             if(float(overlap) >= threshold and float(cosine) >= threshold and float(jaro) >=threshold):
                                   count2+=1
                             else:
                                  if(int(clustering) == 1):
                                      count+=1
                    if(value==7):
                         overlap= arrayTP[i][7]
                         sordice = arrayTP[i][6]
                         jaccard = arrayTP[i][5]
                         clustering= arrayTP[i][9]
                         threshold=fiveCombination[3]/10
                         if(float(jaccard) >= threshold or float(sordice) >= threshold or float(overlap) >=threshold):
                             if(float(jaccard) >= threshold and float(sordice) >= threshold and float(overlap) >=threshold):
                                   count2+=1
                             else:
                                if(int(clustering) == 1):
                                    count+=1

                    if(value==8):
                         jaro= arrayTP[i][8]
                         sordice = arrayTP[i][6]
                         jaccard = arrayTP[i][5]
                         clustering= arrayTP[i][9]
                         threshold=fiveCombination[3]/10
                         if(float(jaccard) >= threshold or float(sordice) >= threshold or float(jaro) >=threshold):
                             if(float(jaccard) >= threshold and float(sordice) >= threshold and float(jaro) >=threshold):
                                   count2+=1
                             else:
                                  if(int(clustering) == 1):
                                      count+=1
                    if(value==9):
                         jaro= arrayTP[i][8]
                         overlap= arrayTP[i][7]
                         jaccard = arrayTP[i][5]
                         clustering= arrayTP[i][9]
                         threshold=fiveCombination[3]/10
                         if(float(jaccard) >= threshold or float(overlap) >= threshold or float(jaro) >=threshold):
                             if(float(jaccard) >= threshold and float(overlap) >= threshold and float(jaro) >=threshold):
                                   count2+=1
                             else:
                                  if(int(clustering) == 1):
                                      count+=1
                    if(value==10):
                         sordice = arrayTP[i][6]
                         overlap= arrayTP[i][7]
                         jaro= arrayTP[i][8]
                         clustering= arrayTP[i][9]
                         threshold=fiveCombination[3]/10
                         if(float(sordice) >= threshold or float(overlap) >= threshold or float(jaro) >=threshold):
                             if(float(sordice) >= threshold and float(overlap) >= threshold and float(jaro) >=threshold):
                                   count2+=1
                             else:
                                  if(int(clustering) == 1):
                                      count+=1

                sum=count+count2
                finalValue.append(sum)
                return finalValue


def readCSV(nameCsv):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = nameCsv
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        rowCanzoni=[]
        for row in csv_reader:
             rowCanzoni.append(row)
        rowCanzoni.pop(0)
        arrayDiStringhe =[]
        for i in range(len(rowCanzoni)):
            if(rowCanzoni[i]):
                    arrayDiStringhe.append(rowCanzoni[i])
    return arrayDiStringhe




#genera tutte le combinazioni da valutare
def generateAllCombination():

  combinazioni, threshold = se.main()

  oneCombination = []
  twoCombination = []
  threeCombination = []
  fourCombination = []
  fiveCombination = []
  sixCombination = []
  sevenCombination = []
  eightCombination = []
  nineCombination = []
  tenCombination = []

  oneCombination.append(combinazioni[0][0:6])
  oneCombination.append(combinazioni[0][7:14])
  oneCombination.append(combinazioni[0][15:])
  oneCombination.append(threshold[0])

  twoCombination.append(combinazioni[1][0:6])
  twoCombination.append(combinazioni[1][7:14])
  twoCombination.append(combinazioni[1][15:])
  twoCombination.append(threshold[1])

  threeCombination.append(combinazioni[2][0:6])
  threeCombination.append(combinazioni[2][7:14])
  threeCombination.append(combinazioni[2][15:])
  threeCombination.append(threshold[2])

  fourCombination.append(combinazioni[3][0:6])
  fourCombination.append(combinazioni[3][7:14])
  fourCombination.append(combinazioni[3][15:])
  fourCombination.append(threshold[3])


  fiveCombination.append(combinazioni[4][0:6])
  fiveCombination.append(combinazioni[4][7:14])
  fiveCombination.append(combinazioni[4][15:])
  fiveCombination.append(threshold[4])


  sixCombination.append(combinazioni[5][0:6])
  sixCombination.append(combinazioni[5][7:14])
  sixCombination.append(combinazioni[5][15:])
  sixCombination.append(threshold[5])

  sevenCombination.append(combinazioni[6][0:7])
  sevenCombination.append(combinazioni[6][8:15])
  sevenCombination.append(combinazioni[6][16:])
  sevenCombination.append(threshold[6])

  eightCombination.append(combinazioni[7][0:7])
  eightCombination.append(combinazioni[7][8:15])
  eightCombination.append(combinazioni[7][16:])
  eightCombination.append(threshold[7])

  nineCombination.append(combinazioni[8][0:7])
  nineCombination.append(combinazioni[8][8:15])
  nineCombination.append(combinazioni[8][16:])
  nineCombination.append(threshold[8])


  tenCombination.append(combinazioni[9][0:7])
  tenCombination.append(combinazioni[9][8:15])
  tenCombination.append(combinazioni[9][16:])
  tenCombination.append(threshold[9])


  return oneCombination, twoCombination,threeCombination, fourCombination,fiveCombination,sixCombination,sevenCombination,eightCombination,nineCombination,tenCombination


#generazione combinazione migliore restituendo l'array ottimale
def generateOneCombination(indexMax,indexMin,oneCombination, twoCombination,threeCombination, fourCombination,fiveCombination,sixCombination,sevenCombination,eightCombination,nineCombination,tenCombination,valueTP,valueFP):
      if(indexMax == indexMin):
          if(indexMax == 0):
              return oneCombination
          if(indexMax == 1):
              return twoCombination
          if(indexMax == 2):
              return threeCombination
          if(indexMax == 3):
              return fourCombination
          if(indexMax == 4):
              return fiveCombination
          if(indexMax == 5):
              return sixCombination
          if(indexMax == 6):
              return sevenCombination
          if(indexMax == 7):
              return eightCombination
          if(indexMax == 8):
              return nineCombination
          if(indexMax == 9):
              return tenCombination
      if(indexMax != indexMin):
          if(valueFP[indexMax]<=10):
              if(indexMax == 0):
                  return oneCombination
              if(indexMax == 1):
                  return twoCombination
              if(indexMax == 2):
                  return threeCombination
              if(indexMax == 3):
                  return fourCombination
              if(indexMax == 4):
                  return fiveCombination
              if(indexMax == 5):
                  return sixCombination
              if(indexMax == 6):
                  return sevenCombination
              if(indexMax == 7):
                  return eightCombination
              if(indexMax == 8):
                  return nineCombination
              if(indexMax == 9):
                  return tenCombination
          else :
              if(indexMin == 0):
                  return oneCombination
              if(indexMin == 1):
                  return twoCombination
              if(indexMin == 2):
                  return threeCombination
              if(indexMin == 3):
                  return fourCombination
              if(indexMin == 4):
                  return fiveCombination
              if(indexMin == 5):
                  return sixCombination
              if(indexMin == 6):
                  return sevenCombination
              if(indexMin == 7):
                  return eightCombination
              if(indexMin == 8):
                  return nineCombination
              if(indexMin == 9):
                  return tenCombination




def finalResult(finalCombination):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "datasetCouple.csv"
    abs_file_path = os.path.join(script_dir, rel_path)
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

        song1= str(arrayDiStringhe[0])
        song2=str(arrayDiStringhe[1])

        song1 = song1.replace("[", "")
        song1 = song1.replace("]", "")
        song1 = song1.replace("'", "")
        song2 = song2.replace("[", "")
        song2 = song2.replace("]", "")
        song2 = song2.replace("'", "")


        cosinedistance = mt.coseno(song1,song2)
        jarow = mt.jaro(song1,song2)
        overlap_coe = mt.overlap_coe(song1, song2)
        soresen = mt.dice_coef(song1,song2)
        jaccard = mt.jaccard(song1,song2)

        valueS =finalCombination[3]
        threshold = valueS/10

        if(finalCombination[0] == "cosine" and finalCombination[1] == "jaccard" and finalCombination[2] =="sordice"):
            if(float(cosinedistance) >= threshold or float(jaccard) >= threshold or float(soresen) >=threshold):
                     if(float(cosinedistance) >= threshold and float(jaccard) >= threshold and float(soresen) >=threshold):
                              dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                              dizionario_info_da_restituire["ValoreMetrica2"] = jaccard
                              dizionario_info_da_restituire["ValoreMetrica3"] = soresen
                              dizionario_info_da_restituire["ValoreClustering"] = 2
                              dizionario_info_da_restituire["Metrica1"] = "Cosine"
                              dizionario_info_da_restituire["Metrica2"] = "Jaccard"
                              dizionario_info_da_restituire["Metrica3"] = "Soresen Dice"
                              dizionario_info_da_restituire["Threshold"] = threshold


                     else:
                        clustering = sp.spectralClustering()
                        if(int(clustering) == 1):
                              dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                              dizionario_info_da_restituire["ValoreMetrica2"] = jaccard
                              dizionario_info_da_restituire["ValoreMetrica3"] = soresen
                              dizionario_info_da_restituire["ValoreClustering"] = 1
                              dizionario_info_da_restituire["Metrica1"] = "Cosine"
                              dizionario_info_da_restituire["Metrica2"] = "Jaccard"
                              dizionario_info_da_restituire["Metrica3"] = "Soresen Dice"
                              dizionario_info_da_restituire["Threshold"] = threshold

                        else:
                              dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                              dizionario_info_da_restituire["ValoreMetrica2"] = jaccard
                              dizionario_info_da_restituire["ValoreMetrica3"] = soresen
                              dizionario_info_da_restituire["ValoreClustering"] = 0
                              dizionario_info_da_restituire["Metrica1"] = "Cosine"
                              dizionario_info_da_restituire["Metrica2"] = "Jaccard"
                              dizionario_info_da_restituire["Metrica3"] = "SoresenDice"
                              dizionario_info_da_restituire["Threshold"] = threshold
            else:
                              dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                              dizionario_info_da_restituire["ValoreMetrica2"] = jaccard
                              dizionario_info_da_restituire["ValoreMetrica3"] = soresen
                              dizionario_info_da_restituire["ValoreClustering"] = 0
                              dizionario_info_da_restituire["Metrica1"] = "Cosine"
                              dizionario_info_da_restituire["Metrica2"] = "Jaccard"
                              dizionario_info_da_restituire["Metrica3"] = "SoresenDice"
                              dizionario_info_da_restituire["Threshold"] = threshold


        if(finalCombination[0] == "cosine" and finalCombination[1] == "jaccard" and finalCombination[2] =="overlap"):
            if(float(cosinedistance) >= threshold or float(jaccard) >= threshold or float(overlap_coe) >=threshold):
                     if(float(cosinedistance) >= threshold and float(jaccard) >= threshold and float(overlap_coe) >=threshold):
                              dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                              dizionario_info_da_restituire["ValoreMetrica2"] = jaccard
                              dizionario_info_da_restituire["ValoreMetrica3"] = overlap_coe
                              dizionario_info_da_restituire["ValoreClustering"] = 2
                              dizionario_info_da_restituire["Metrica1"] = "Cosine"
                              dizionario_info_da_restituire["Metrica2"] = "Jaccard"
                              dizionario_info_da_restituire["Metrica3"] = "Overlap"
                              dizionario_info_da_restituire["Threshold"] = threshold


                     else:
                        clustering = sp.spectralClustering()
                        if(int(clustering) == 1):
                              dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                              dizionario_info_da_restituire["ValoreMetrica2"] = jaccard
                              dizionario_info_da_restituire["ValoreMetrica3"] = overlap_coe
                              dizionario_info_da_restituire["ValoreClustering"] = 1
                              dizionario_info_da_restituire["Metrica1"] = "Cosine"
                              dizionario_info_da_restituire["Metrica2"] = "Jaccard"
                              dizionario_info_da_restituire["Metrica3"] = "Overlap"
                              dizionario_info_da_restituire["Threshold"] = threshold

                        else:
                              dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                              dizionario_info_da_restituire["ValoreMetrica2"] = jaccard
                              dizionario_info_da_restituire["ValoreMetrica3"] = overlap_coe
                              dizionario_info_da_restituire["ValoreClustering"] = 0
                              dizionario_info_da_restituire["Metrica1"] = "Cosine"
                              dizionario_info_da_restituire["Metrica2"] = "Jaccard"
                              dizionario_info_da_restituire["Metrica3"] = "Overlap"
                              dizionario_info_da_restituire["Threshold"] = threshold
            else:
                              dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                              dizionario_info_da_restituire["ValoreMetrica2"] = jaccard
                              dizionario_info_da_restituire["ValoreMetrica3"] = overlap_coe
                              dizionario_info_da_restituire["ValoreClustering"] = 0
                              dizionario_info_da_restituire["Metrica1"] = "Cosine"
                              dizionario_info_da_restituire["Metrica2"] = "Jaccard"
                              dizionario_info_da_restituire["Metrica3"] = "Overlap"
                              dizionario_info_da_restituire["Threshold"] = threshold


        if(finalCombination[0] == "cosine" and finalCombination[1] == "jaccard" and finalCombination[2] =="jaro"):
            if(float(cosinedistance) >= threshold or float(jaccard) >= threshold or float(jarow) >=threshold):
                     if(float(cosinedistance) >= threshold and float(jaccard) >= threshold and float(jarow) >=threshold):
                              dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                              dizionario_info_da_restituire["ValoreMetrica2"] = jaccard
                              dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                              dizionario_info_da_restituire["ValoreClustering"] = 2
                              dizionario_info_da_restituire["Metrica1"] = "Cosine"
                              dizionario_info_da_restituire["Metrica2"] = "Jaccard"
                              dizionario_info_da_restituire["Metrica3"] = "Jaro"
                              dizionario_info_da_restituire["Threshold"] = threshold


                     else:
                        clustering = sp.spectralClustering()
                        if(int(clustering) == 1):
                                 dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                                 dizionario_info_da_restituire["ValoreMetrica2"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 1
                                 dizionario_info_da_restituire["Metrica1"] = "Cosine"
                                 dizionario_info_da_restituire["Metrica2"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold

                        else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                                 dizionario_info_da_restituire["ValoreMetrica2"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Cosine"
                                 dizionario_info_da_restituire["Metrica2"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold
            else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                                 dizionario_info_da_restituire["ValoreMetrica2"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Cosine"
                                 dizionario_info_da_restituire["Metrica2"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold

        if(finalCombination[0] == "cosine" and finalCombination[1] == "sordice" and finalCombination[2] =="overlap"):
            if(float(cosinedistance) >= threshold or float(soresen) >= threshold or float(overlap_coe) >=threshold):
                     if(float(cosinedistance) >= threshold and float(soresen) >= threshold and float(overlap_coe) >=threshold):
                          dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                          dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                          dizionario_info_da_restituire["ValoreMetrica3"] = overlap_coe
                          dizionario_info_da_restituire["ValoreClustering"] = 2
                          dizionario_info_da_restituire["Metrica1"] = "Cosine"
                          dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                          dizionario_info_da_restituire["Metrica3"] = "Overlap"
                          dizionario_info_da_restituire["Threshold"] = threshold

                     else:
                        clustering = sp.spectralClustering()
                        if(int(clustering) == 1):
                                 dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                                 dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica3"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreClustering"] = 1
                                 dizionario_info_da_restituire["Metrica1"] = "Cosine"
                                 dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica3"] = "Overlap"
                                 dizionario_info_da_restituire["Threshold"] = threshold

                        else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                                 dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica3"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Cosine"
                                 dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica3"] = "Overlap"
                                 dizionario_info_da_restituire["Threshold"] = threshold
            else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                                 dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica3"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Cosine"
                                 dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica3"] = "Overlap"
                                 dizionario_info_da_restituire["Threshold"] = threshold

        if(finalCombination[0] == "cosine" and finalCombination[1] == "sordice" and finalCombination[2] =="jaro"):
            if(float(cosinedistance) >= threshold or float(soresen) >= threshold or float(jarow) >=threshold):
                     if(float(cosinedistance) >= threshold and float(soresen) >= threshold and float(jarow) >=threshold):
                          dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                          dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                          dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                          dizionario_info_da_restituire["ValoreClustering"] = 2
                          dizionario_info_da_restituire["Metrica1"] = "Cosine"
                          dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                          dizionario_info_da_restituire["Metrica3"] = "Jaro"
                          dizionario_info_da_restituire["Threshold"] = threshold

                     else:
                        clustering = sp.spectralClustering()
                        if(int(clustering) == 1):
                                 dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                                 dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 1
                                 dizionario_info_da_restituire["Metrica1"] = "Cosine"
                                 dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold

                        else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                                 dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Cosine"
                                 dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold
            else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                                 dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Cosine"
                                 dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold
        if(finalCombination[0] == "cosine" and finalCombination[1] == "overlap" and finalCombination[2] =="jaro"):
            if(float(cosinedistance) >= threshold or float(overlap_coe) >= threshold or float(jarow) >=threshold):
                     if(float(cosinedistance) >= threshold and float(overlap_coe) >= threshold and float(jarow) >=threshold):
                         dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                         dizionario_info_da_restituire["ValoreMetrica2"] = overlap_coe
                         dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                         dizionario_info_da_restituire["ValoreClustering"] = 2
                         dizionario_info_da_restituire["Metrica1"] = "Cosine"
                         dizionario_info_da_restituire["Metrica2"] = "Overlap"
                         dizionario_info_da_restituire["Metrica3"] = "Jaro"
                         dizionario_info_da_restituire["Threshold"] = threshold

                     else:
                        clustering = sp.spectralClustering()
                        if(int(clustering) == 1):
                                 dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                                 dizionario_info_da_restituire["ValoreMetrica2"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 1
                                 dizionario_info_da_restituire["Metrica1"] = "Cosine"
                                 dizionario_info_da_restituire["Metrica2"] = "Overlap"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold

                        else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                                 dizionario_info_da_restituire["ValoreMetrica2"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Cosine"
                                 dizionario_info_da_restituire["Metrica2"] = "Overlap"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold
            else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = cosinedistance
                                 dizionario_info_da_restituire["ValoreMetrica2"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Cosine"
                                 dizionario_info_da_restituire["Metrica2"] = "Overlap"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold

        if(finalCombination[0] == "jaccard" and finalCombination[1] == "sordice" and finalCombination[2] =="overlap"):
            if(float(jaccard) >= threshold or float(soresen) >= threshold or float(overlap_coe) >=threshold):
                     if(float(jaccard) >= threshold and float(soresen) >= threshold and float(overlap_coe) >=threshold):
                         dizionario_info_da_restituire["ValoreMetrica1"] = jaccard
                         dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                         dizionario_info_da_restituire["ValoreMetrica3"] = overlap_coe
                         dizionario_info_da_restituire["ValoreClustering"] = 2
                         dizionario_info_da_restituire["Metrica1"] = "Jaccard"
                         dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                         dizionario_info_da_restituire["Metrica3"] = "Overlap"
                         dizionario_info_da_restituire["Threshold"] = threshold

                     else:
                        clustering = sp.spectralClustering()
                        if(int(clustering) == 1):
                                 dizionario_info_da_restituire["ValoreMetrica1"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica3"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreClustering"] = 1
                                 dizionario_info_da_restituire["Metrica1"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica3"] = "Overlap"
                                 dizionario_info_da_restituire["Threshold"] = threshold

                        else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica3"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica3"] = "Overlap"
                                 dizionario_info_da_restituire["Threshold"] = threshold
            else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica3"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica3"] = "Overlap"
                                 dizionario_info_da_restituire["Threshold"] = threshold

        if(finalCombination[0] == "jaccard" and finalCombination[1] == "sordice" and finalCombination[2] =="jaro"):
            if(float(jaccard) >= threshold or float(soresen) >= threshold or float(jarow) >=threshold):
                     if(float(jaccard) >= threshold and float(soresen) >= threshold and float(jarow) >=threshold):
                         dizionario_info_da_restituire["ValoreMetrica1"] = jaccard
                         dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                         dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                         dizionario_info_da_restituire["ValoreClustering"] = 2
                         dizionario_info_da_restituire["Metrica1"] = "Jaccard"
                         dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                         dizionario_info_da_restituire["Metrica3"] = "Jaro"
                         dizionario_info_da_restituire["Threshold"] = threshold

                     else:
                        clustering = sp.spectralClustering()
                        if(int(clustering) == 1):
                                 dizionario_info_da_restituire["ValoreMetrica1"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 1
                                 dizionario_info_da_restituire["Metrica1"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold

                        else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold
            else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica2"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica2"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold

        if(finalCombination[0] == "jaccard" and finalCombination[1] == "overlap" and finalCombination[2] =="jaro"):
            if(float(jaccard) >= threshold or float(overlap_coe) >= threshold or float(jarow) >=threshold):
                     if(float(jaccard) >= threshold and float(overlap_coe) >= threshold and float(jarow) >=threshold):
                                 dizionario_info_da_restituire["ValoreMetrica1"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica2"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 2
                                 dizionario_info_da_restituire["Metrica1"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica2"] = "Overlap"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold

                     else:
                        clustering = sp.spectralClustering()
                        if(int(clustering) == 1):
                                 dizionario_info_da_restituire["ValoreMetrica1"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica2"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 1
                                 dizionario_info_da_restituire["Metrica1"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica2"] = "Overlap"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold

                        else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica2"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica2"] = "Overlap"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold
            else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = jaccard
                                 dizionario_info_da_restituire["ValoreMetrica2"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Jaccard"
                                 dizionario_info_da_restituire["Metrica2"] = "Overlap"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold
        if(finalCombination[0] == "sordice" and finalCombination[1] == "overlap" and finalCombination[2] =="jaro"):
            if(float(soresen) >= threshold or float(overlap_coe) >= threshold or float(jarow) >=threshold):
                     if(float(soresen) >= threshold and float(overlap_coe) >= threshold and float(jarow) >=threshold):
                                 dizionario_info_da_restituire["ValoreMetrica1"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica2"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 2
                                 dizionario_info_da_restituire["Metrica1"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica2"] = "Overlap"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold

                     else:
                        clustering = sp.spectralClustering()
                        if(int(clustering) == 1):
                                 dizionario_info_da_restituire["ValoreMetrica1"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica2"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 1
                                 dizionario_info_da_restituire["Metrica1"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica2"] = "Overlap"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold

                        else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica2"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica2"] = "Overlap"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold
            else:
                                 dizionario_info_da_restituire["ValoreMetrica1"] = soresen
                                 dizionario_info_da_restituire["ValoreMetrica2"] = overlap_coe
                                 dizionario_info_da_restituire["ValoreMetrica3"] = jarow
                                 dizionario_info_da_restituire["ValoreClustering"] = 0
                                 dizionario_info_da_restituire["Metrica1"] = "Soresen Dice"
                                 dizionario_info_da_restituire["Metrica2"] = "Overlap"
                                 dizionario_info_da_restituire["Metrica3"] = "Jaro"
                                 dizionario_info_da_restituire["Threshold"] = threshold


def main():
    """
    Main leggermente modificato per restituire un dizionario
    :return: dizionario_info_da_restituire
    """

    oneCombination, twoCombination,threeCombination, fourCombination,fiveCombination,sixCombination,sevenCombination,eightCombination,nineCombination,tenCombination = generateAllCombination()
    arrayTP =[]
    arrayFP = []
    for i in range(1,11):
        valueTP = generateBestCombination("datasetTP.csv",i,arrayTP,oneCombination,twoCombination,threeCombination,fourCombination,fiveCombination,sixCombination,sevenCombination,eightCombination,nineCombination,tenCombination)
        valueFP = generateBestCombination("datasetFP.csv",i,arrayFP,oneCombination,twoCombination,threeCombination,fourCombination,fiveCombination,sixCombination,sevenCombination,eightCombination,nineCombination,tenCombination)

    valuemax = max(valueTP)
    valuemin = min(valueFP)
    indexMax = valueTP.index(valuemax)
    indexMin = valueFP.index(valuemin)

    finalCombination = generateOneCombination(indexMax,indexMin,oneCombination, twoCombination,threeCombination, fourCombination,fiveCombination,sixCombination,sevenCombination,eightCombination,nineCombination,tenCombination,valueTP,valueFP)

    finalResult(finalCombination)
    return dizionario_info_da_restituire
