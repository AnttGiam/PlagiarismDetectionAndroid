import chars2vec
import csv
from sklearn.cluster import SpectralClustering
import os


def spectralClustering():
    words=[]

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = 'datasetFit.csv'
    abs_file_path = os.path.join(script_dir, rel_path)  # <-- abbiamo così ottenuto un path funzionante
    with open(abs_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                words.append(row[2])
                line_count += 1

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = 'datasetCouple.csv'
    abs_file_path = os.path.join(script_dir, rel_path)  # <-- abbiamo così ottenuto un path funzionante
    with open(abs_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        arrayDiStringhe=[]
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                words.append(row)
                line_count += 1
            for i in range(len(words)):
               if(words[i]):

                    stringa = str(words[i])
                    stringa = stringa.replace("[", "")
                    stringa = stringa.replace("]", "")
                    stringa = stringa.replace("'", "")
                    arrayDiStringhe.append(stringa)


    c2v_model = chars2vec.load_model('eng_50')
    word_embeddings = c2v_model.vectorize_words(arrayDiStringhe)
    #print(word_embeddings)
    #print(len(word_embeddings))

    clustering = SpectralClustering(n_clusters=9,
                 random_state=0).fit(word_embeddings)
    labels=clustering.labels_
    #print(labels)
    l=len(labels)

    if (labels[l-1]==labels[l-2]):
        #print('TRUE')
        return True
    else:
        #print('FALSE')
        return False
