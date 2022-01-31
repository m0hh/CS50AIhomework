from dis import dis
from pagerank import transition_model
from pomegranate import *
from numpy.random import choice

a = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
p = "1.html"

d = 0.85



out  = transition_model(a,p,d)



def sample_pagerank(corpus, damping_factor, n):
    prob = 1 / len(corpus)
    st = dict()
    for key in corpus:
        st[key] = prob
    print('start', st)
    dist = []
    for key in corpus:
        t = transition_model(corpus, key, damping_factor)
        for keyy, value in t.items():
            l = []
            l.append(key)
            l.append(keyy)
            l.append(value)
            dist.append(l)
    print("dist", dist)

        

    d1 = DiscreteDistribution(st)
    d2 = ConditionalProbabilityTable(dist,[d1])

    model = MarkovChain([d1,d2])
    
    final = model.sample(n)
    f = len(final)
    r = dict()
    for key in corpus:
        r[key] = final.count(key) / f
    return r

#output =  sample_pagerank(a,d,10000)
'''
a = ['a','b','c']
prob = ['.3','.3','.4']

draw = choice(a,1,prob)
print(draw)
print(a)

'''

dic = list()

a = sum(dic)
print(a)

while sum(dic) > 0.03:
    print("tototo")