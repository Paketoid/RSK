import random
from bisect import bisect
import math
from collections import Counter


def textToMatrix(text, n, m):
    with open("alphabet.txt","r") as alph:
        abc = alph.readline().replace("\n", "")
    A = [text[i*m:(i+1)*m] for i in range(n)]
    res = [[abc.find(c) for c in line] for line in A]
    return res


def matrixToDWord(matrix):
    dWord = []
    n, m = len(matrix), len(matrix[0])
    for j in range(m):
        for i in range(n):
            dWord += [(i+1, j+1)]*matrix[i][j]
    return dWord


def getIndex(x, arr):
    for i in range(len(arr)):
        if x < arr[i]:
            return i
    return len(arr)


def dWordToDiagram(dWord):
    P, Q = [], []
    def insert(i, j):
        for r in range(len(P)):
            if j >= P[r][-1]:
                P[r].append(j); Q[r].append(i)
                return
            #c = bisect(P[r], i)
            c = getIndex(j, P[r])
            #print(c, len(P[r]))
            P[r][c], j = j, P[r][c]
        P.append([j])
        Q.append([i])

    for pair in dWord:
        insert(pair[0], pair[1])
    return (P, Q)


def getDimensions(text):
    x = len(text)
    for i in range(int(math.sqrt(x)), 0, -1):
            if x % i == 0:
                return (i, x // i)
    return (1, x)


def getShape(diagram):
    shape = [len(row) for row in diagram]
    return shape


def getWeight(diagram):
    wei = Counter()
    for row in diagram:
        wei += Counter(row)
    return [(i, wei[i]) for i in range(1, len(wei)+1)]

#n, m = 5, 6

with open("input.txt", "r") as fin, open("logs.txt", "w") as logs, open("encrypted.txt", "w") as fout:
    text = fin.readline().strip()
    n, m = getDimensions(text)
    matrix = textToMatrix(text, n, m)
    dWord = sorted(matrixToDWord(matrix))
    P, Q = dWordToDiagram(dWord)
    lamb = getShape(P)
    P_w, Q_w = getWeight(P), getWeight(Q)

    logs.write(f"{n}, {m}\n\n")
    logs.write(f"{dWord}\n\n")
    logs.write(f"{lamb}\n\n")
    logs.write("\n".join(map(str, P)) + f"\n\n" + "\n".join(map(str, Q)) + f"\n\n")
    logs.write("\n".join(map(str, matrix)))
    logs.write(f"\n\nP_w={P_w}\nQ_w={Q_w}")

    #fout.write(f"{lamb[0]}\n")
    #fout.write(" ".join([" ".join(list(map(str, row))+["0"]*(len(P[0])-len(row))) for row in P]) + f"\n" + " ".join([" ".join(list(map(str, row))+["0"]*(len(Q[0])-len(row))) for row in Q]))
    fout.write(" ".join(list(map(str, lamb))) + f"\n")
    fout.write(" ".join([" ".join(list(map(str, row))) for row in P]) + f"\n" + " ".join([" ".join(list(map(str, row))) for row in Q]))
    #+["0"]*(len(Q[0])-len(row))
    #+["0"]*(len(P[0])-len(row))