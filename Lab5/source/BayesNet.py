import random

class CPT:
    def __init__(self):
        self.condictionedVariable = None
        self.condictionedDomain = list()
        self.uncondictionedvariable = list()
        self.cptTable = dict()

    def __init__(self,variableList,condictionDomainList):
        self.condictionedVariable = variableList[0]
        self.condictionedDomain = condictionDomainList
        self.uncondictionedVariable = variableList[1:]
        self.cptTable = dict()

    def action(self,evidenceList):
        cumulativeVal = 0
        randomNo = random.random()
        for key,value in self.cptTable.items():
            if(self.dictKeyCheck(key,evidenceList)):
                cumulativeVal += value
                if(randomNo <= cumulativeVal):
                    return list(set(evidenceList).union(set(key)))
                

    #to check if all needed variables are present in evidentList
    #evidenceList [+a,-b,+c,+d]   key [+b,+d] where CPT.condictionedVariable = A (a)
    def dictKeyCheck(self,key,evidenceList):
        flg = True
        for k in key:
            if not(k in self.condictionedDomain):
                flg = flg & (k in evidenceList)  
        return flg 
     
    def cptValue(self,queryList):
        for key,value in self.cptTable.items():
            flg = True
            for eachVal in key:
                if eachVal in queryList:
                    flg = flg & True
                else: 
                    flg = flg & False
            if flg:
                return value
        return -1

    def action_Gibb(self,evidenceList,bayesNetObj):
        cumulativeVal = 0
        evidenceList = list(set(evidenceList).difference(set(self.condictionedDomain)))
        #print("EVIDENTLIST:",evidenceList)
        randomNo = random.random()
        eachVal = dict()
        denum = 0
        for cpt_domain in self.condictionedDomain:
            num = self.cptValue(evidenceList + [cpt_domain])
            for each_CPT in bayesNetObj.CPT_list:
                if self.condictionedVariable in each_CPT.uncondictionedVariable:
                    num *= each_CPT.cptValue(evidenceList + [cpt_domain])
            eachVal[cpt_domain] = num
        for d in eachVal.values():
            denum += d
        for domain_val, prob in eachVal.items():
            cumulativeVal += (prob/denum)
            if(randomNo <= cumulativeVal):
                return evidenceList + [domain_val]

            

class BayesNet(CPT):
    def __init__(self):
        self.Node = list()
        #list of variables
        self.CPT_list = list()
        #list of cpts
        self.domainDict = dict()
        #domainDict['B'] = ['+b','-b']
        self.CPT_dict = dict()

    def cpt_size(self,variableList):
        row = 1
        for X in variableList:
            row *= len(self.domainDict[X])
        return row



    

