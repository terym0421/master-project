class SizeError(Exception):
    pass

class DownwardPiece:
    def __init__(self, label):
        self.label = label
        # label format is as follows:
        # label = [N, SE, SW]
        # where NW = NorthWest, SE = SouthEast and so on...

    def __str__(self):
        return str(self.label)
    
    def copy(self):
        return DownwardPiece(self.label)

    @property
    def southEast(self):
        return self.label[1]
        
    @property
    def southWest(self):
        return self.label[2]
 
    @property
    def north(self):
        return self.label[0]



class Puzzle:
    def __init__(self, edgeLength, northWest, northEast, south, downwardPieceList=[]):
        if not( edgeLength == len(northWest)):
            raise SizeError
        if not( edgeLength == len(northEast)):
            raise SizeError
        if not( edgeLength == len(south)):
            raise SizeError
        self.edgeLength = edgeLength
        self.northWest = northWest
        self.northEast = northEast
        self.south = south
        self.downwardPieceList = downwardPieceList
    
    def __str__(self):
        output = "["
        for p in self.downwardPieceList:
            output = output + "".join(p.label) + ", "
        output = output + "]"
        return output


    def deleteTheLowestPieces(self, m):
        # delete the lowest m rows. 
        # if the size of edge length is smaller than or equal to m, then we do nothing
        if self.edgeLength <= m:
            return self.copy()
        else:
            reducedSouthEdge = ""
            fst = int((m-1) * self.edgeLength - (m * (m - 1) / 2))
            # the self.downwardPieceList[fst:] pieces are in the m's row
            for piece in self.downwardPieceList[fst:fst+self.edgeLength-m]:
                reducedSouthEdge += piece.label[0]
            reducedPieces = self.downwardPieceList[fst+self.edgeLength-m:]
            reducedPuzzle = Puzzle(self.edgeLength-m, self.northWest[m:], self.northEast[:self.edgeLength-m], reducedSouthEdge, reducedPieces)
            return reducedPuzzle

    def copy(self):
        newPieceList = [p.copy() for p in self.downwardPieceList]
        return Puzzle(self.edgeLength, self.northWest, self.northEast, self.south, newPieceList)
    
    def weight(self, mode="str"):
        if mode == "str":
            result = ""

            triangulatedPieceList = []
            s = 0
            t = self.edgeLength - 1
            for i in range(1, self.edgeLength):
                triangulatedPieceList.append(self.downwardPieceList[s:t])
                tmp = t
                s = tmp
                t += (self.edgeLength- 1 -i)

            #print(triangulatedPieceList)
            for i, row in enumerate(triangulatedPieceList):
                for j, piece in enumerate(row):
                    if piece.label == ["b","0","1"]:
                        rightFoot = i + j + 2
                        leftFoot = j + 1
                        result += "(y_" + str(rightFoot) + " - y_" + str(leftFoot)+")"
            if result == "":
                result = "1"
            return result
        
        if mode == "int":
            result = []

            triangulatedPieceList = []
            s = 0
            t = self.edgeLength - 1
            for i in range(1, self.edgeLength):
                triangulatedPieceList.append(self.downwardPieceList[s:t])
                tmp = t
                s = tmp
                t += (self.edgeLength- 1 -i)

            #print(triangulatedPieceList)
            for i, row in enumerate(triangulatedPieceList):
                for j, piece in enumerate(row):
                    if piece.label == ["b","0","1"]:
                        rightFoot = i + j + 2
                        leftFoot = j + 1
                        result.append((rightFoot, leftFoot))
            if result == []:
                result = 1
            return result

upwardDictionary = {"0":{"0":"0", "1":"a", "a":"-1", "b":"1"},
                    "1":{"0":"-1", "1":"1", "a":"0", "b":"-1"},
                    "a":{"0":"1", "1":"-1", "a":"-1", "b":"-1"},
                    "b":{"0":"-1", "1":"-1", "a":"-1", "b":"-1"}}
#upwardDictionary = {"0":{"0":"0", "1":"a", "a":"-1"},
#                    "1":{"0":"-1", "1":"1", "a":"0"},
#                    "a":{"0":"1", "1":"-1", "a":"-1"}}
# upwardDictionary[NW][S] = the label of the NE label when the corresponding edge label to the variables is as in the table
#

downwardDictionary = {"0":["00", "a1"], "1":["11", "0a", "b0"], "a":["10"], "b":"-1"} 
#downwardDictionary = {"0":["00", "a1"], "1":["11", "0a"], "a":["10"]}
# downwardDictionary[x] = the possible labels of N and SE edge if the SW edge label is x
# e.g.) "b1" means the north edge is "b" and the southeast edge is "1"
# you can calculate other puzzle theories by changing these dictionary

def determineTheLowestPieces(P):
    # if the size of P is 1, then we need to check only the three edges compatible
    if P.edgeLength == 1:
        northWest = P.northWest[0]
        northEast = P.northEast[0]
        south = P.south[0]
        if upwardDictionary[northWest][south] == northEast:
            return [P]
        else:
            return []

    # determine the left most piece of P in the lowest row
    result = []
    northWest = P.northWest[0]
    south = P.south[0]
    newLabel = upwardDictionary[northWest][south]
    if newLabel == "-1":
        return result
    else:
        for possibleLabel in downwardDictionary[newLabel]:
            newPiece = DownwardPiece([possibleLabel[0], possibleLabel[1], newLabel])
            Q = P.copy()
            Q.downwardPieceList.append(newPiece)
            result.append(Q)
    
    # determine all the remain Pieces
    for i in range(1, P.edgeLength):
        tmp = []
        for possiblePuzzle in result:
            lastPiece = possiblePuzzle.downwardPieceList[-1]
            northWest = lastPiece.southEast
            south = P.south[i]
            newLabel = upwardDictionary[northWest][south]
            if not newLabel == "-1":
                if i < P.edgeLength - 1:
                    for possibleLabel in downwardDictionary[newLabel]:
                        newPiece = DownwardPiece([possibleLabel[0], possibleLabel[1], newLabel])
                        Q = possiblePuzzle.copy()
                        Q.downwardPieceList.append(newPiece)
                        tmp.append(Q)
                else:
                    if newLabel == P.northEast[-1]:
                        tmp.append(possiblePuzzle)
        result = tmp
    return result





def calculateAllPuzzle(northWest, northEast, south):
    n = len(northWest)
    P = Puzzle(n, northWest, northEast, south)
    result = determineTheLowestPieces(P.copy())
    for i in range(n-1):  
        tmp = []
        for p in result:
            reducedPuzzleList = determineTheLowestPieces(p.deleteTheLowestPieces(i+1))
            for reducedPuzzle in reducedPuzzleList:
                pCopy = p.copy()
                pCopy.downwardPieceList += reducedPuzzle.downwardPieceList
                tmp.append(pCopy)
        result = tmp
    return result



####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
#
#
#def convertStringToDiagram(string):
#    L = list(string)
#    n = len(L)
#    k = 0
#    I = []
#    for (i, s) in enumerate(L):
#        if s == "1":
#            k += 1
#            I.append(i+1)
#    
#    diagram = [n - k - I[0] + 1]
#    for i in range(k-1):
#        diagram.append(diagram[i] - (I[i+1] - I[i]) + 1)
#    return diagram
#
#
#def convertDiagramToString(inputDiagram, n, k):
#    diagram = inputDiagram.copy()
#    I = [n - k + 1 - diagram[0]]
#    if len(diagram) < k:
#        diagram += [0 for i in range(k-len(diagram))]
#    for j in range(k-1):
#        I.append(I[j] + diagram[j] - diagram[j+1] + 1)
#    string = [0 for j in range(n)]
#    for s in I:
#        string[s-1] = 1
#    result = list(map( lambda x: str(x), string ))
#    return "".join(result)
#
#
#l = [3,1,1]
#m = [3,2]
#n = [4,3,2]
#c = 7
#k = 3
#
#
##puzzleList = calculateAllPuzzle(convertDiagramToString(l, c, k), convertDiagramToString(m, c, k), convertDiagramToString(n, c, k))
#puzzleList = calculateAllPuzzle("0100110", "0101001", "1010100")
#for p in puzzleList:
#    print(p)