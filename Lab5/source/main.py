from inputReader import reader
from Sampling import sampleCounter

#change as per usage
filePath = r"example_bayesnet.txt"
N = 100000

bayesObj,query,evidence = reader(filePath)
main = sampleCounter()
p = main.Prior_counter(bayesObj,query,N,evidence)
r = main.rejection_counter(bayesObj,query,N,evidence)
l = main.likelihood_counter(bayesObj,query,N,evidence)
g = main.gibbs_counter(bayesObj,query,N,evidence)

print("Prior Sampling:",p)
print("Rejection Sampling:",r)
print("Likelihood Weighting:",l)
print("Gibbs Sampling:",g)







