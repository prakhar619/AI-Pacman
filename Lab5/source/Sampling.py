import random
class sampleGenerator():
    def produceSample(self,bayesObj,evidence = dict()):
        currentSample = list()
        weight = 1
        for cpt_X in bayesObj.CPT_list:
            if not(cpt_X.condictionedVariable in evidence):
                currentSample = cpt_X.action(currentSample)
            else:
                currentSample.append(evidence[cpt_X.condictionedVariable])
                weight = weight*cpt_X.cptValue(currentSample)
        return currentSample,weight

    def produceSample_Gibb(self,bayesObj,currentSample_Gibb,evidence = dict()):
        nonEvidentList = list(set(bayesObj.Node).difference(set(evidence.keys())))
        rVar = random.choice(nonEvidentList)
        #print(rVar)
        cpt_X = bayesObj.CPT_dict[rVar]
        currentSample_Gibb = cpt_X.action_Gibb(currentSample_Gibb,bayesObj)
        return currentSample_Gibb
    
class sampleCounter(sampleGenerator):
    def Prior_counter(self,bayesNet,query,N,evidence):
        count = 0
        totalcount = 0  
        query = list(query.values())+list(evidence.values())       
        evidence = list(evidence.values())   
        for i in range(0,N):
            sample,weight = self.produceSample(bayesNet)
            if self.query_sample_Matcher(query,sample):
                count += weight
            if self.query_sample_Matcher(evidence,sample):
                totalcount += weight 
        return count/totalcount
    
    def rejection_counter(self,bayesNet,query,N,evidence):
        count = 0
        totalcount = 0
        query = list(query.values())
        evidence = list(evidence.values())
        for i in range(0,N):
            sample,weight = self.produceSample(bayesNet)
            if self.query_sample_Matcher(evidence,sample):
                totalcount += weight
                if self.query_sample_Matcher(query,sample):
                    count +=weight
        if(totalcount == 0):
            return -1
        return count/totalcount

    def likelihood_counter(self,bayesNet,query,N,evidence):
        count = 0
        totalcount = 0 
        query = list(query.values())  
        for i in range(0,N):
            sample,weight = self.produceSample(bayesNet,evidence)
            if self.query_sample_Matcher(query,sample):
                count += weight
            totalcount += weight 
        return count/totalcount
    
    def gibbs_counter(self,bayesNet,query,N,evidence):
        count = 0
        totalcount = 0
        query = list(query.values())
        sample,weight = self.produceSample(bayesNet,evidence)
        for i in range(0,N):
            sample = self.produceSample_Gibb(bayesNet,sample,evidence)
            if self.query_sample_Matcher(query,sample):
                count += 1
            totalcount += 1
        return count/totalcount

    
    def query_sample_Matcher(self,query,sample):
        flg = True
        for q in query:
            flg = flg & (q in sample)
        return flg

    def printSample(sampleList):
        for char in range(97,123):
            for x in sampleList:
                if chr(char) in x:
                    print( x,end=",")
        print()



