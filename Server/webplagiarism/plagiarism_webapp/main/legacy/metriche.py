import textdistance as td
import math
import numpy as np
global y_predNorm
global y_trueNorm



#Token based

def jaccard(y_predNorm,y_trueNorm):
    return td.jaccard.similarity(y_predNorm, y_trueNorm)

def coseno(y_predNorm,y_trueNorm):
    return td.cosine.similarity(y_predNorm, y_trueNorm)

#da fare
def cityblock_distance(A, B):
    result = np.sum([abs(a - b) for (a, b) in zip(A, B)])
    return result

def dice_coef(y_predNorm,y_trueNorm):
    return td.sorensen_dice.similarity(y_predNorm, y_trueNorm)




def overlap_coe(y_predNorm,y_trueNorm):
     return td.overlap.similarity(y_trueNorm, y_predNorm)

def tanimoto(y_predNorm,y_trueNorm):
     return td.tanimoto.similarity(y_trueNorm, y_predNorm)


#def ngrams(X,Y):
 #  return NGram.compare(X,Y)


def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[None]*(n + 1) for i in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]
# end of function lcs


#edit based
def hamming(y_predNorm,y_trueNorm):
     return td.hamming.similarity(y_trueNorm, y_predNorm)

def Lev(y_predNorm,y_trueNorm):
     return td.levenshtein.similarity(y_trueNorm, y_predNorm)

def jaro_winkler(y_predNorm,y_trueNorm):
    return td.jaro_winkler.similarity(y_trueNorm, y_predNorm)

def jaro(y_predNorm,y_trueNorm):
    return td.jaro.similarity(y_trueNorm, y_predNorm)

def damerau_levenshtein(y_predNorm,y_trueNorm):
    return td.damerau_levenshtein.similarity(y_trueNorm, y_predNorm)

def needleman_wunsch(y_predNorm,y_trueNorm):
    return td.needleman_wunsch.similarity(y_trueNorm, y_predNorm)

def smith_waterman(y_predNorm,y_trueNorm):
    return td.smith_waterman.similarity(y_trueNorm, y_predNorm)

