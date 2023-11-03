from BayesNet import BayesNet
from BayesNet import CPT

#fileReader expectation:
    #variable listed in topological order
    #variable domain defined in earlier order

def csvList(line):
    lastValue = ""
    ret = list()
    for c in line:
        #csv has these extra values:
            #\n , <space> and we add extra | 
        if(c == ',' or c == '\n' or c=='|'):
            if(lastValue != ""):
                ret.append(lastValue)
            lastValue = ""
        elif(c != ' ' ):
            lastValue += c
    return ret
    

def reader(filePath):
    fileObject = open(filePath,"r")
    bayesNet = BayesNet()

    #sample file line1 read
    rawVariableList = fileObject.readline()
    li = csvList(rawVariableList)
    bayesNet.Node = li[1:]

    #sample file line 2-6 read
    for X_var in bayesNet.Node:
        li = csvList(fileObject.readline())
        bayesNet.domainDict[li[0]] = li[1:]

    #sample file line 7-31 read
    for X_var in bayesNet.Node:
        li = csvList(fileObject.readline())
        cpt_obj = CPT(li,bayesNet.domainDict[X_var])
        for i in range(0,bayesNet.cpt_size(li)):
            li = csvList(fileObject.readline())
            cpt_obj.cptTable[tuple(li[0:-1])] = float(li[-1])
        bayesNet.CPT_list.append(cpt_obj)
        bayesNet.CPT_dict[X_var] = cpt_obj

    fileObject.close()
    return bayesNet