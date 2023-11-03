from inputReader import reader
from BayesNet import BayesNet
import random
filePath = r"example_bayesnet.txt"

bayesObj = reader(filePath)

def produceSample(bayesObj,evidence = dict()):
    currentSample = list()
    weight = 1
    for cpt_X in bayesObj.CPT_list:
        if not(cpt_X.condictionedVariable in evidence):
            currentSample = cpt_X.action(currentSample)
        else:
            currentSample.append(evidence[cpt_X.condictionedVariable])
            weight = weight*cpt_X.cptValue(currentSample)
    return currentSample,weight


def produceSample_Gibb(bayesObj,currentSample_Gibb,evidence = dict()):
    nonEvidentList = list(set(bayesObj.Node).difference(set(evidence.keys())))
    rVar = random.choice(nonEvidentList)
    #print(rVar)
    cpt_X = bayesObj.CPT_dict[rVar]
    currentSample_Gibb = cpt_X.action_Gibb(currentSample_Gibb,bayesObj)
    return currentSample_Gibb



def printSample(sampleList):
    for char in range(97,123):
        for x in sampleList:
            if chr(char) in x:
                print( x,end=",")
    print()
    

currentSample_Gibb = produceSample(bayesObj)[0]
printSample(currentSample_Gibb)
for i in range(1,10):
    currentSample_Gibb = produceSample_Gibb(bayesObj,currentSample_Gibb)
    printSample(currentSample_Gibb)

