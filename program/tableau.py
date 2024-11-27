class SizeError(Exception):
    pass

class HorizontalEdge:
    def __init__(self, edgeLabel=set()):
        self.upperBox = None
        self.lowerBox = None
        self.edgeLabel = edgeLabel


class Box:
    def __init__(self, tableau, upperEdge=None, lowerEdge=None, insideLabel=0):
        self.tableau = tableau
        self.insideLabel = insideLabel
        self.__upperEdge = upperEdge
        self.lowerEdge = lowerEdge
        self.rightBox = None
        self.lowerBox = None
        self.leftBox = None
        self.upperBox = None
    
    def __str__(self):
        return str(self.insideLabel)
        
    @property
    def upperEdge(self):
        return self.upperBox.lowerEdge if not self.upperBox == None else self.__upperEdge
        
    def isVacant(self):
        if self.insideLabel == 0:
            return True
        else:
            return False
    
    def isOuterCorner(self):
        if (self.rightBox == None) and (self.lowerBox == None) and (self.lowerEdge.edgeLabel == set()):
            return True
        else:
            return False
        
    def isInnerCorner(self):
        if self.isVacant():
            if (self.rightBox == None) and (self.lowerBox == None):
                return True
            else:
                if self.rightBox == None:
                    if not self.lowerBox.isVacant():
                        return True
                elif self.lowerBox == None:
                    if not self.rightBox.isVacant():
                        return True
                elif (not self.rightBox.isVacant()) and (not self.lowerBox.isVacant()):
                    return True
        else:
            return False
        
    def rowNumber(self):
        count = 0
        if not self.upperBox == None:
            count = self.upperBox.rowNumber() + 1
        return count
    
    def columnNumber(self):
        count = 0
        if not self.leftBox == None:
            count = self.leftBox.columnNumber() + 1
        return count

    def coordinate(self):
        return (self.rowNumber(), self.columnNumber())

    def countRightBoxes(self):
        count = 0
        if not self.rightBox == None:
            count = self.rightBox.countRightBoxes() + 1
        return count


#    tmpUpperLabel = boxX.upperEdge.edgeLabel
#    boxX.upperEdge.edgeLabel = boxY.upperEdge.edgeLabel
#    boxY.upperEdge.edgeLabel = tmpUpperLabel
#
#    tmpLowerLabel = boxX.lowerEdge.edgeLabel
#    boxX.lowerEdge.edgeLabel = boxY.lowerEdge.edgeLabel
#    boxY.lowerEdge.edgeLabel = tmpLowerLabel

class Tableau:
    def __init__(self, diagram):
        # initiate the boxes s.t. all the box labels is 0 is elements is None
        # and setting the right, left, lower and upper adjecent boxes for each boxes
        self.diagram = diagram
        self.elements = [[Box(self, HorizontalEdge(), HorizontalEdge()) for j in range(diagram[0])]]
        self.elements += [[Box(self, None, HorizontalEdge(), 0) for j in range(diagram[i+1])] for i in range(len(diagram)-1)]
        for i in range(len(diagram)):
            for j in range(diagram[i]):
                box = self.elements[i][j]
                if j < (diagram[i] - 1):
                    box.rightBox = self.elements[i][j+1]
                if i < (len(diagram) - 1) and (j < diagram[i+1]):
                    box.lowerBox = self.elements[i+1][j]
                if not j == 0:
                    box.leftBox = self.elements[i][j-1]
                if not i == 0:
                    box.upperBox = self.elements[i-1][j]
                box.lowerEdge.upperBox = box
                box.lowerEdge.lowerBox = box.lowerBox if not box.lowerBox == None else None

    
    def __str__(self):
        insideLabels = ""
        for i in range(len(self.diagram)):
            insideLabels += "["
            for j in range(self.diagram[i]):
                if j < self.diagram[i]-1:
                    insideLabels += str(self.elements[i][j]) + ", "
                else:
                    insideLabels += str(self.elements[i][j]) + "]"
            if i < len(self.diagram)-1:
                insideLabels += "\n"
            else:
                insideLabels += ","
        return insideLabels


    def copy(self):
        T = Tableau(self.diagram.copy())
        for j in range(self.diagram[0]):
            T.elements[0][j].upperEdge.edgeLabel = self.elements[0][j].upperEdge.edgeLabel.copy()
        for i in range(len(self.diagram)):
            for j in range(self.diagram[i]):
                T.elements[i][j].insideLabel = self.elements[i][j].insideLabel
                T.elements[i][j].lowerEdge.edgeLabel = self.elements[i][j].lowerEdge.edgeLabel.copy()
        return T
    
    
    def deleteOuterBox(self, coordinate):
        box = self.elements[coordinate[0]][coordinate[1]]
        if not box.isOuterCorner():
            pass
        if not box.upperBox == None:
            box.upperBox.lowerBox = None
        if not box.leftBox == None:
            box.leftBox.rightBox = None
        del self.elements[coordinate[0]][coordinate[1]]
        self.diagram[coordinate[0]] -= 1
        self.diagram.remove(0) if 0 in self.diagram else -1


    def isSuperStandard(self):
        if self.diagram == []:
            return False
        for j in range(self.diagram[0]):
            if not self.elements[0][j].insideLabel == j + 1:
                return False
            if not self.elements[0][j].lowerEdge.edgeLabel == set():
                return False
        for i in range(1, len(self.diagram)):
            for j in range(self.diagram[i]):
                if not self.elements[i][j].insideLabel == j + sum(self.diagram[:i]) + 1:
                    return False
                if not self.elements[i][j].lowerEdge.edgeLabel == set():
                    return False
        return True
            
        
    def innerCorner(self, searchRange=None):
        if searchRange == None:
            searchRange = self.diagram
#        else:
#            for i, rowCount in enumerate(searchRange):
#                if rowCount > self.diagram[i]:
#                    raise SizeError
        result = []
        for i in range(len(searchRange)):
            for j in range(searchRange[i]):
                box = self.elements[i][j]
                if box.isInnerCorner():
                    result.append(box)
        return result
    
    def slide(self, vacantBox):
        if vacantBox.rightBox == None:
            swapLabel(vacantBox, vacantBox.lowerBox)
            return vacantBox.lowerBox
        if vacantBox.lowerBox == None:
            swapLabel(vacantBox, vacantBox.rightBox)
            return vacantBox.rightBox
        if vacantBox.lowerBox.insideLabel <= vacantBox.rightBox.insideLabel:
            swapLabel(vacantBox, vacantBox.lowerBox)
            return vacantBox.lowerBox
        else:
            swapLabel(vacantBox, vacantBox.rightBox)
            return vacantBox.rightBox

    def consecutiveSlide(self, vacantBox):
        if not vacantBox.isInnerCorner():
            pass
        while not vacantBox.isOuterCorner():
            vacantBox = self.slide(vacantBox)
        self.deleteOuterBox(vacantBox.coordinate())

    def rectification(self, searchRange):
        for (i, j) in readingOrder(searchRange, [], "NW"):
            innerCorner = self.elements[i][j]
            self.consecutiveSlide(innerCorner)

    def equivariantSlide(self, vacantBox):
        if (vacantBox.rightBox == None) and (vacantBox.lowerBox == None):
            vacantBox.insideLabel = min(vacantBox.lowerEdge.edgeLabel)
            vacantBox.lowerEdge.edgeLabel -= {min(vacantBox.lowerEdge.edgeLabel)}
            return None
        
        if vacantBox.rightBox == None:
            if vacantBox.lowerEdge.edgeLabel == set():
                swapLabel(vacantBox, vacantBox.lowerBox)
                return vacantBox.lowerBox
            else:
                vacantBox.insideLabel = min(vacantBox.lowerEdge.edgeLabel)
                vacantBox.lowerEdge.edgeLabel -= {min(vacantBox.lowerEdge.edgeLabel)}
                return None
        
        if vacantBox.lowerBox == None:
            if vacantBox.lowerEdge.edgeLabel == set():
                swapLabel(vacantBox, vacantBox.rightBox)
                return vacantBox.rightBox
            else:
                if min(vacantBox.lowerEdge.edgeLabel) < vacantBox.rightBox.insideLabel:
                    vacantBox.insideLabel = min(vacantBox.lowerEdge.edgeLabel)
                    vacantBox.lowerEdge.edgeLabel -= {min(vacantBox.lowerEdge.edgeLabel)}
                    return None
                else:
                    swapLabel(vacantBox, vacantBox.rightBox)
                    return vacantBox.rightBox
        
        if vacantBox.lowerEdge.edgeLabel == set():
            if vacantBox.lowerBox.insideLabel < vacantBox.rightBox.insideLabel:
                swapLabel(vacantBox, vacantBox.lowerBox)
                return vacantBox.lowerBox
            else:
                swapLabel(vacantBox, vacantBox.rightBox)
                return vacantBox.rightBox
        else:
            m = min(vacantBox.lowerEdge.edgeLabel)
            if m < vacantBox.rightBox.insideLabel:
                vacantBox.insideLabel = m
                vacantBox.lowerEdge.edgeLabel -= {m}
                return None
            else:
                swapLabel(vacantBox, vacantBox.rightBox)
                return vacantBox.rightBox

    
    def equivariantConsecutiveSlide(self, vacantBox):
        while not vacantBox.isOuterCorner():
            vacantBox = self.equivariantSlide(vacantBox)
            if vacantBox == None:
                break
        self.deleteOuterBox(vacantBox.coordinate()) if not vacantBox == None else -1
    
    def equivariantRectificationOfColumn(self, columnNumber, n):
        vacantBoxes = []
        edgeLabelsAndRowNumber = {}
        factors = []

        # get the vacant boxes on the column ordering rectification order and get the all edge labels on the column
        box = self.elements[0][columnNumber]
        while not box == None:
            if box.isVacant():
                vacantBoxes.insert(0, box)
            if not box.lowerEdge.edgeLabel == set():
                for l in box.lowerEdge.edgeLabel:
                    edgeLabelsAndRowNumber.setdefault(l, box.rowNumber())
            box = box.lowerBox

        for innerCorner in vacantBoxes:
            self.equivariantConsecutiveSlide(innerCorner)
        
        # find the final position of the edge labels and calculate its factor
        if not(self.diagram == []) and columnNumber < self.diagram[0]:
            box = self.elements[0][columnNumber]
            while not box == None:
                if box.insideLabel in edgeLabelsAndRowNumber.keys():
                    initialRowNum = edgeLabelsAndRowNumber.pop(box.insideLabel)
                    initialBeta = manhattanDistance(n, (initialRowNum, columnNumber))
                    finalBeta = manhattanDistance(n, (box.rowNumber(), columnNumber+box.countRightBoxes()))
                    factors.append((initialBeta + 1, finalBeta))
                box = box.lowerBox
            if not edgeLabelsAndRowNumber == {}:
                return 0
            else:
                return factors        
        else:
            return []
    
    def equivariantRectification(self, searchRange, n):
        # n is the number of columns of the universal shape which contains self
        weight = []
        # if there exists any edge labels on the outer of smallShape, we define its weight as 0
        #for i in range(len(self.diagram)):
        #    for j in range(searchRange[0], self.diagram[i]):
        #        if not self.elements[i][j].lowerEdge.edgeLabel == set():
        #            weight = 0

        for i in reversed(range(searchRange[0])):
            factorsOftheColumn = self.equivariantRectificationOfColumn(i, n)
            if (type(weight) == list) and (not factorsOftheColumn == 0):
                weight += factorsOftheColumn
            else:
                weight = 0
        return weight

    def isLittlewoodRichardson(self, zeroRange, maxlabel):
        coordinateList = readingOrder(self.diagram, zeroRange, "WS")
        labelCount = [0 for i in range(maxlabel)]
        for (i, j) in coordinateList:
            l = self.elements[i][j].insideLabel
            labelCount[l-1] += 1
            if (not l == 1) and (labelCount [l-1] > labelCount[l-2]):
                return False
        return True
    
    def outputEdgeLabels(self):
        edgeLables = ""
        for i in range(len(self.diagram)):
            edgeLables += "["
            for j in range(self.diagram[i]):
                edgeLables += str(self.elements[i][j].lowerEdge.edgeLabel)
                edgeLables += "," if j < self.diagram[0]-1 else ""
            edgeLables += "]\n" if i < len(self.diagram) -1 else "]"
        return edgeLables
    
    def weight(self, searchRange, n, mode="str"):
        if mode == "str":
            T = self.copy()
            w = T.equivariantRectification(searchRange, n)
            result = ""
            for (r, s) in w:
                result += "(y_" + str(r) + " - " + "y_" + str(s) + ")"
            if result == "":
                result = "1"
            return result
        
        if mode == "int":
            T = self.copy()
            return T.equivariantRectification(searchRange, n)


def swapLabel(boxX, boxY):
    tmpInsideLabel = boxX.insideLabel
    boxX.insideLabel = boxY.insideLabel
    boxY.insideLabel = tmpInsideLabel

def transpose(diagram):
    result = []
    while len(diagram) > 0:
        result += [len(diagram) for i in range(diagram[-1])]
        tmp = list(map( lambda x: x - diagram[-1], diagram))
        diagram = [s for s in tmp if not s == 0]
    return result

def manhattanDistance(numberOfColumn, coordinate):
    return coordinate[0] - coordinate[1] + numberOfColumn

# mode is in {"ES", "SW"}
# ES: read the boxes left to right and up to bottom
# WS: read the boxes right to left and up to bottom
# WN: read the boxes right to left and bottom to up
# return the list of coordinates which is aligned corresponding order
def readingOrder(shape, exclusionRange=[], mode="ES"):
    if mode == "ES":
        result = []
        for i in range(len(shape)):
            if i < len(exclusionRange):
                for j in range(exclusionRange[i], shape[i]):
                    result.append((i,j))
            else:
                for j in range(shape[i]):
                    result.append((i,j))
    
    if mode == "WS":
        result = []
        for i in range(len(shape)):
            if i < len(exclusionRange):
                for j in reversed(range(exclusionRange[i], shape[i])):
                    result.append((i,j))
            else:
                for j in reversed(range(shape[i])):
                    result.append((i,j))
    
    if mode == "WN":
        result = []
        for i in reversed(range(len(shape))):
            if i < len(exclusionRange):
                for j in reversed(range(exclusionRange[i], shape[i])):
                    result.append((i,j))
            else:
                for j in reversed(range(shape[i])):
                    result.append((i,j))

        
    if mode == "NW":
        reverseOrder = readingOrder(transpose(shape), transpose(exclusionRange), "WN")
        result = list(map( lambda x: (x[1], x[0]), reverseOrder))
        return result

    return result



# return all the skew tableau with largeShape/smallShape and content
# if type(content) == int, you can use 1, 2,..., content as the label as many as you want
# if type(content) == list, you can use 1, 2, ..., len(content) as many as content[i] 
def allSkewTableauxWithShapeWithContent(largeShape, smallShape, content):
    if type(content) == int:
        m = content
        n = sum(largeShape)
        content = [n for i in range(m)]
    maxLabel = len(content)
    T = Tableau(largeShape)
    boxCoordinateList = readingOrder(largeShape, smallShape)
    result = [(T, content)]
    tmp = []

    while len(boxCoordinateList) > 0:
        coordinate = boxCoordinateList.pop(0)
        for (previousTableau, remainContent) in result:
            targetBox = previousTableau.elements[coordinate[0]][coordinate[1]]
            upperLabel = targetBox.upperBox.insideLabel if not targetBox.upperBox == None else 0
            leftLabel = targetBox.leftBox.insideLabel if not targetBox.leftBox == None else 1
            m = max(upperLabel + 1, leftLabel)
            for newLabel in range(m, maxLabel + 1):
                tmpRemainContent = remainContent.copy()
                if tmpRemainContent[newLabel-1] > 0:
                    newTableau = previousTableau.copy()
                    newTableau.elements[coordinate[0]][coordinate[1]].insideLabel = newLabel
                    tmpRemainContent[newLabel-1] -= 1
                    tmp.append((newTableau, tmpRemainContent))
        result = tmp
        tmp = []

    return result
    

def allStandardTableauxWithShape(largeShape, smallShape, n):
    content = [1 for i in range(n)]
    return allSkewTableauxWithShapeWithContent(largeShape, smallShape, content)


# calculate littlewood richardson number by counting the skew tableaux with shape n/l and content m whose yamanouchi word is reverse lattice
def littlewoodRichardson_yamanouchi(l, m, n):
    if len(l) > len(n):
        return 0
    if not sum(l) + sum(m) == sum(n):
        return 0
    for i in range(len(l)):
        if l[i] > n[i]:
            return 0
    
    tableauList = list(map(lambda x: x[0], allSkewTableauxWithShapeWithContent(n, l, m)))
    count = 0
    for t in tableauList:
        if t.isLittlewoodRichardson(l, len(m)):
            count += 1
    return count


def littlewoodRichardson_jeudetaquin(l, m, n):
    if len(l) > len(n):
        return 0
    if not sum(l) + sum(m) == sum(n):
        return 0
    for i in range(len(l)):
        if l[i] > n[i]:
            return 0
        
    tableauList = list(map(lambda x: x[0], allSkewTableauxWithShapeWithContent(n, l, m)))
    count = len(tableauList)
    #superSemiStandardTableau = Tableau(m, [[ i+1 for j in range(m[i]) ] for i in range(len(m))])
    for t in tableauList:
        t.rectification(l)
        for i in range(len(t.diagram)):
            for j in range(t.diagram[i]):
                if not t.elements[i][j].insideLabel == i+1:
                    count -= 1
                    break
            else:
                continue
            break
    return count




def listToSet(content):
    result = []
    for i in range(len(content)):
        if content[i] > 0:
            result.append(i+1)
    return set(result)


def powerset(S):
    result = [set()]
    for x in S:
        tmp = []
        for subset in result:
            tmp.append({x} | subset)
        result += tmp
    return result


# determine the all horizontal edge labels of the skew tableau with shape large/small
def allEdgeLabeledTableauxWithShape(largeShape, smallShape, n):
    reducedLargeShape = list(map( lambda x: smallShape[0] if x > smallShape[0] else x, largeShape ))
    boxCoordinates = readingOrder(reducedLargeShape, smallShape)
    southMostVacantCoordinates = [(transpose(smallShape)[i]-1, i) for i in range(len(transpose(smallShape)))]
    boxCoordinates = southMostVacantCoordinates + boxCoordinates
    tableauContentList = allStandardTableauxWithShape(largeShape, smallShape, n)
    tableauContentList = list(map( lambda x: (x[0], listToSet(x[1])), tableauContentList))
    for (i, j) in boxCoordinates:
        tmp = []
        for (previousTableau, residueContent) in tableauContentList:
            box = previousTableau.elements[i][j]
            # if the upper box does not exist or is not vacant, then we have to assign only lower edge label of the box
            lowerBound = box.insideLabel
            upperBound = box.lowerBox.insideLabel if not box.lowerBox == None else n
            availableLabels = residueContent & set(range(lowerBound, upperBound + 1))
            for s in powerset(availableLabels):
                newTableau = previousTableau.copy()
                newResidueContent = residueContent - s
                newTableau.elements[i][j].lowerEdge.edgeLabel = s
                tmp.append((newTableau, newResidueContent))
        tableauContentList = tmp
        tmp = []
    return tableauContentList
                    



def calculateAllEdgeLabeledTableaux(l, m, n, numberOfColumn):
    tableauList = []
    for T,C in allEdgeLabeledTableauxWithShape(n, l, sum(m)):
        TCopy = T.copy()
        weight = TCopy.equivariantRectification(l, numberOfColumn)
        if TCopy.isSuperStandard() and TCopy.diagram == m and (not weight == 0):
            tableauList.append(T)
    return tableauList


def equal(T, U):
    if not T.diagram == U.diagram:
        return False
    for i in range(len(T.diagram)):
        for j in range(T.diagram[i]):
            if not T.elements[i][j].insideLabel == U.elements[i][j].insideLabel:
                return False
            if not T.elements[i][j].lowerEdge.edgeLabel == U.elements[i][j].lowerEdge.edgeLabel:
                return False
    return True




####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

#T = Tableau([5,4,3,2])
##T.elements[0][3].insideLabel = 3
##T.elements[1][2].insideLabel = 2
##T.elements[1][3].insideLabel = 6
##T.elements[2][1].insideLabel = 4
#T.elements[1][1].lowerEdge.edgeLabel = {1}
#T.elements[1][2].lowerEdge.edgeLabel = {5}
#print(T)
#weight = T.weight([5,4,3,2], 5, mode="str")
#print(T)
#print(T.diagram)
#print(weight)



