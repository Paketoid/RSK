def stringToDiagram(st, shp):
    arr = st.split()
    res = []
    for i in range(len(arr)//shp):
        res.append(list(map(int, arr[i*shp:(i+1)*shp])))
    return res


def getDiagramMax(diagram): #returns (int, int)
    value = -1
    for row in diagram:
        value = max(value, max(row))
    return value


def getNextToPurge(diagram, diagramMax):
    for i in range(len(diagram)-1, -1, -1):
        if diagram[i][-1] == diagramMax:
            return (i, len(diagram[i])-1)
    return (-1, -1)


def getIndex(x, arr):
    for i in range(len(arr)):
        if x <= arr[i]:
            return i
    return len(arr)


def diagramsToDWord(P, Q):
    dWord = []
    value = getDiagramMax(P)
    toPurge = getNextToPurge(P, value)
    
    while len(P):
        print(len(P), P[toPurge[0]], value)
        valueFromQ = Q[toPurge[0]][toPurge[1]]
    
        if len(Q[toPurge[0]]) > 1:
            Q[toPurge[0]] = Q[toPurge[0]][:-1]
            P[toPurge[0]] = P[toPurge[0]][:-1]
        else:
            Q = Q[:-1]
            P = P[:-1]
            #Q = Q[:toPurge[0]] + Q[toPurge[0]+1:]
            #P = P[:toPurge[0]] + P[toPurge[0]+1:]
        
        for r in range(toPurge[0]-1,-1,-1):
            if value > P[r][-1]:
                value, P[r][-1] = P[r][-1], value
                continue
            c = getIndex(value, P[r])
            value, P[r][-1] = P[r][-1], value
            print(value)
        print()
        dWord.append((value, valueFromQ))

        value = getDiagramMax(P)
        toPurge = getNextToPurge(P, value)
        

    return dWord


def clearDiagram(diagram):
    for i in range(len(diagram)):
        if diagram[i][-1] == 0:
            diagram[i] = diagram[i][:diagram[i].index(0)]



#take column with max number in SSYT and dispose of it from the bottom; repeat until done

def dWordToMatrix(dWord):
    m, n = dWord[0]
    matrix = [[0 for _ in range(m)] for __ in range(n)]

    for pair in dWord:
        matrix[pair[1]-1][pair[0]-1] += 1
    return matrix


def matrixToText(matrix):
    res = ""
    for line in matrix:
        for c in line:
            res += chr(c + ord(' '))
    return res


with open("encrypted.txt","r") as fin, open("output.txt","w") as fout:
    shp = int(fin.readline().strip())
    P = stringToDiagram(fin.readline().strip(), shp)
    Q = stringToDiagram(fin.readline().strip(), shp)

    clearDiagram(P)
    clearDiagram(Q)

    fout.write("\n".join(map(str, P)) + f"\n\n" + "\n".join(map(str, Q)) + f"\n\n")

    dWord = diagramsToDWord(P, Q)
    fout.write("\n".join(map(str, P)) + f"\n\n" + "\n".join(map(str, Q)) + f"\n\n")
    matrix = dWordToMatrix(dWord)
    #text = matrixToText(matrix)
    
    fout.write(f"{dWord}\n\n")
    fout.write("\n".join(map(str, matrix)))
    #fout.write(text + "\n")