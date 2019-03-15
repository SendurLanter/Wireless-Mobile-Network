import math
import numpy as np
import matplotlib.pyplot as plt
Pt=(10**(33/10))/1000
Gt=10**(14/10)
Gr=10**(14/10)
print(Pt)
ht=50+1.5
hr=1.5
k=1.38*10**(-23)
T=273+27
B=10*10**6
N=k*T*B
Pr=list()
dist=list()
'''
for d in range(1,10000):
	g=((ht*hr)**2)/(d**4)
	P=g*Pt*Gr*Gr
	Pr.append(10*math.log(P))
	dist.append(d)
plt.plot(dist, Pr)
plt.show()'''

'''
for d in range(1,10000):
	g=((ht*hr)**2)/(d**4)
	P=10**(np.random.normal(0,6)/10)*g*Pt*Gr*Gr
	Pr.append(10*math.log(P))
	dist.append(d)'''

for d in range(1,10000):
	g=((ht*hr)**2)/(d**4)
	P=10**(np.random.normal(0,6)/10)*g*Pt*Gr*Gr
	SINR=P/N
	Pr.append(10*math.log(SINR))
	dist.append(d)

plt.plot(dist, Pr)
plt.show()
