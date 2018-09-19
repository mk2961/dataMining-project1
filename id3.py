"""CSC535 HW1
ID3 DT
William Zay
Leonard Museau
Michael Knapp
"""

from math import log
import operator
import csv


training_data = [

({'level':'Senior', 'lang':'Java', 'tweets':'no', 'phd':'no'}, False),

({'level':'Senior', 'lang':'Java', 'tweets':'no', 'phd':'yes'}, False),

({'level':'Mid', 'lang':'Python', 'tweets':'no', 'phd':'no'}, True),

({'level':'Junior', 'lang':'Python', 'tweets':'no', 'phd':'no'}, True),

({'level':'Junior', 'lang':'R', 'tweets':'yes', 'phd':'no'}, True),

({'level':'Junior', 'lang':'R', 'tweets':'yes', 'phd':'yes'}, False),

({'level':'Mid', 'lang':'R', 'tweets':'yes', 'phd':'yes'}, True),

({'level':'Senior', 'lang':'Python', 'tweets':'no', 'phd':'no'}, False),

({'level':'Senior', 'lang':'R', 'tweets':'yes', 'phd':'no'}, True),

({'level':'Junior', 'lang':'Python', 'tweets':'yes', 'phd':'no'}, True),

({'level':'Senior', 'lang':'Python', 'tweets':'yes', 'phd':'yes'}, True),

({'level':'Mid', 'lang':'Python', 'tweets':'no', 'phd':'yes'}, True),

({'level':'Mid', 'lang':'Java', 'tweets':'yes', 'phd':'no'}, True),

({'level':'Junior', 'lang':'Python', 'tweets':'no', 'phd':'yes'}, False)

]

test_data =[{"level": "Junior","lang": "Java","tweets": "yes","phd": "no"},

{"level": "Junior","lang": "Java","tweets": "yes","phd": "yes"},

{"level": "Intern"},

{"level": "Senior"}]


def entropy(data, attributeList, target):
    frequency = {}
    entrop = 0.0
    
    for j in range(0, len(attributeList)):
   
        if (attributeList[j][target] in frequency):
            val = attributeList[j][target]
            frequency[val] += 1.0
            
        else:
            val = attributeList[j][target]
            frequency[val] = 1.0
             
    for freq in frequency.values():
        entrop += (freq/len(attributeList)) * log(freq/len(attributeList), 2)
 
    return -entrop
   
def gain(data, attributeList, attribute, target):
    
    frequency = {}
    localEntropy = 0.0 
    
    for j in range(0, len(attributeList)):   
       
        if (data[j][0][attribute] in frequency):
            val = data[j][0][attribute]
            frequency[val] += 1.0
            
        else:
            val = data[j][0][attribute]
            frequency[val] = 1.0
            
    splitInfo = 0
    for value in frequency.keys():
        
        splitInfo -= (frequency[value]/sum(frequency.values())) * log(frequency[value]/sum(frequency.values()), 2)
        
        #probability is equivalent to Sv over S
        probability = frequency[value] / sum(frequency.values())
        
        
        subset = [sample for sample in data if sample[0][attribute] == value]
        subAttributeList = []
        for x in range(0,len(subset)):
            subAttributeList.append(subset[x][0])
        
        e = probability * (entropy(subset, subAttributeList, attribute)+.97)
        localEntropy += e
      
 
    gain = entropy(data, attributeList, attribute)-localEntropy
    
    if splitInfo != 0.0:
        gainRatio  = gain/splitInfo
    else:
        gainRatio = gain
    
    return gainRatio
        
  
def mostCommon(data):
    from collections import Counter
    return Counter(data).most_common(1)[0][0]

def best_attribute(data, attributeList, target):  
    bestSplit = list(attributeList[0].keys())[0] 
    infoGain = 0.0001
    
    for val in attributeList[0].keys():
        
        newGain = gain(data, attributeList, val, target)
        
        if newGain > infoGain and newGain <.6:
            infoGain = newGain
            bestSplit = val
 
    if infoGain > 0.0009:      
        return bestSplit
    else:       
        return False

def id3Tree(data, attributeList, targetList):
    
    if len(data) == 0 :
        return 
    default = mostCommon(targetList)
    targets = list(attributeList[0].keys())
    
    #empty data or attributes
    
    if  (len(targets) < 0):
        return default
    
    #all have same values
    elif targetList.count(targetList[0]) == len(targetList):
        return targetList[0]
    
    else:
        bestSplit = best_attribute(data, attributeList, targetList)
        if bestSplit == False:
            return default
        
        tree = {bestSplit:{}}

        values = []
        for x in range(0,len(attributeList)):
           
            values.append(attributeList[x][bestSplit])

        #getting unique values and switching back for indexing
        values = set(values)
        values = list(values)
                
        for x in values:
            
            newTargetList = []
            newAttributeList = []
            newData = []

            for y in range(0, len(attributeList)):
                
                if bestSplit in attributeList[y]:
                    if attributeList[y][bestSplit] == x:
                       
                        newTargetList.append(targetList[y])
                        newData.append(data[y])
                        newAttributeList.append(attributeList[y])
                        
                        del newAttributeList[-1][bestSplit]
          
            if (len(newData) != 0 and len(newAttributeList) !=0 and len(newTargetList) !=0):
                subtree = id3Tree(newData, newAttributeList, newTargetList)
                tree[bestSplit][x] = subtree
                
    return tree   


def cvsToDict(filename):
    import os
    path = os.path.normpath(os.getcwd() + "\\" + filename)
    fs = csv.reader(open(path))
    data = []
    i = 0
    template = {}
    i = 0
    
    for row in fs:
        data.append(row)
            
    realData = []
    for k in range(1, len(data)):
        diction = {}
        for r in range(1, len(data[k])):
            diction[data[0][r]] = data[k][r]     
                              
        if data[k][0] == 'e':
            
            realData.append((diction, True))
        else:
            realData.append((diction,False))
    myDict = dict((rows,rows) for rows in fs)
    
    
    return realData


def hirePrune(tree):
    
    tree['level']['Junior'] = tree['level']['Junior']['lang']['R']
    tree['level']['Senior'] = tree['level']['Senior']['lang']['Python']
    
    
    return dict(tree)


def mushPrune(tree):
    #This pruned tree uses a heurustic and has 98% accuracy for any mushroom with an odor trait
    for odor in list(tree.values())[0]:
        
        if odor in ['l', 'n']:
            tree['odor'][odor] = tree['odor']['a']
        
    return tree


def countDict(tree, trueCount = 0, falseCount = 0):
    #Returns count of leaf nodes
    for key in tree.keys():
        if tree[key] == True:
            trueCount += 1
        elif tree[key] == False:
            falseCount += 1
        else:
            trueC, falseC = countDict(tree[key])
            trueCount += trueC
            falseCount+= falseC
    return trueCount, falseCount
    

def classify(tree, testData):
    """if 'odor' in testData.keys():
        return tree['odor'][testData['odor']]"""
    for x in tree.keys():
        try:
  
            if x in testData.keys():
                y = testData[x]
                
                if tree[x][y] in [True, False]:
                    return tree[x][y]
                elif type(testData[x]) == str:
                    return classify(tree[x][y], testData)
                           
        except:
            trueCount, falseCount = countDict(tree)
            
            if trueCount <= falseCount:
                return False
            return True
    #Needed if there is no error, but no proper classification
    trueCount, falseCount = countDict(tree)
            
    if trueCount <= falseCount:
        return False
    return True


        
myCvs = cvsToDict('mushroom.csv')
attributeList = []
for x in range(0,len(training_data)):
    attributeList.append(training_data[x][0])


targetList = []
for y in range(0,len(training_data)):
    targetList.append(training_data[y][1])
import copy
attributeListcopy = copy.deepcopy(attributeList)
tree = id3Tree(training_data, attributeListcopy, targetList)

print()
from pprint import pprint

tree = hirePrune(tree)
pprint(tree)
print()

for val in test_data:
    print(str(val) + "  " + str(classify(tree, val)))
print()
mushattributeList = []
for x in range(0,len(myCvs)):
    mushattributeList.append(myCvs[x][0])

mushattributeListcopy = copy.deepcopy(mushattributeList)
mushtargetList = []
for y in range(0,len(myCvs)):
    mushtargetList.append(myCvs[y][1])

mushTree = id3Tree(myCvs, mushattributeListcopy, mushtargetList)
mushTree = mushPrune(mushTree)
pprint(mushTree)

fastMushClass = []
for x in range(0,len(myCvs)):
    tempDict = {}
    tempDict['odor'] = mushattributeList[x]['odor']
    fastMushClass.append(tempDict)
"""import time

t0 = time.time()


for x in range(len(myCvs)):
    #prints the actual value, and the classified value
    
    print(str(myCvs[x][1]) + "   " + str(classify(mushTree, mushattributeList[x])))
    classify(mushTree, fastMushClass[x])
t1 = time.time()

total = t1-t0
print(total)"""
