def stringToDiagram(st, shp):
    arr = st.split()
    res = []
    ind = 0
    for i in shp:
        res.append(list(map(int, arr[ind:ind + i])))
        ind += i
    return res


def getDiagramMax(diagram): #returns (int, int)
    value = -1
    for row in diagram:
        value = max(value, max(row))
    return value

#can be optimized by keeping max for every row in memory


def getNextToPurge(diagram, diagramMax):
    for i in range(len(diagram)):
        if diagram[i][-1] == diagramMax:
            return (i, len(diagram[i])-1)
    return (-1, -1)


def getIndex(x, arr):
    for i in range(len(arr)-1,-1,-1):
        if arr[i] < x:
            return i
    return -1


def diagramsToDWord(P, Q):
    dWord = []
    value = getDiagramMax(Q)
    toPurge = getNextToPurge(Q, value)
    
    while len(P):
        valueFromP = P[toPurge[0]][toPurge[1]]
    
        if len(Q[toPurge[0]]) > 1:
            Q[toPurge[0]] = Q[toPurge[0]][:toPurge[1]]
            P[toPurge[0]] = P[toPurge[0]][:toPurge[1]]
        else:
            Q = Q[:toPurge[0]]
            P = P[:toPurge[0]]
            #Q = Q[:toPurge[0]] + Q[toPurge[0]+1:]
            #P = P[:toPurge[0]] + P[toPurge[0]+1:]
        
        for r in range(toPurge[0]-1,-1,-1):
            c = getIndex(valueFromP, P[r])
            valueFromP, P[r][c] = P[r][c], valueFromP
            #print(P)
            #print(value, valueFromP)
            #print(Q)
            #print()

        dWord.append((value, valueFromP))

        value = getDiagramMax(Q)
        toPurge = getNextToPurge(Q, value)

    return dWord


def clearDiagram(diagram):
    for i in range(len(diagram)):
        if diagram[i][-1] == 0:
            diagram[i] = diagram[i][:diagram[i].index(0)]



#take column with max number in SSYT and dispose of it from the bottom; repeat until done

def dWordToMatrix(dWord):
    m, n = -1, -1
    for pair in dWord:
        m, n = max(m, pair[0]), max(n, pair[1])
    matrix = [[0 for _ in range(n)] for __ in range(m)]

    for pair in dWord:
        matrix[pair[0]-1][pair[1]-1] += 1
    return matrix


def matrixToText(matrix):
    res = ""
    with open("alphabet.txt","r") as alph:
        abc = alph.readline().strip()
    for line in matrix:
        for c in line:
            res += abc[c]
    return res


with open("encrypted.txt","r") as fin, open("logs_dec.txt","w") as logs, open("output.txt","w") as fout:
    #shp = int(fin.readline().strip())
    shp = list(map(int, fin.readline().strip().split()))
    P = stringToDiagram(fin.readline().strip(), shp)
    Q = stringToDiagram(fin.readline().strip(), shp)

    #clearDiagram(P)
    #clearDiagram(Q)

    logs.write("\n".join(map(str, P)) + f"\n\n" + "\n".join(map(str, Q)) + f"\n\n")

    dWord = diagramsToDWord(P, Q)
    matrix = dWordToMatrix(dWord)
    text = matrixToText(matrix)
    
    logs.write(f"{dWord}\n\n")
    logs.write("\n".join(map(str, matrix)) + f"\n\n")
    logs.write(text)

    fout.write(text)