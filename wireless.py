import math
import numpy as np
import matplotlib.pyplot as plt
Pt=(10**(33/10))/1000
Gt=10**(14/10)
Gr=10**(14/10)
#print(Pt)
ht=50+1.5
hr=1.5
k=1.38*10**(-23)
T=273+27
B=10*(10**6)
N=k*T*B
interference=0

Pr=list()
dist=list()
#path loss
for d in range(1,1000):
	g=((ht*hr)**2)/(d**4)
	P=g*Pt*Gt*Gr
	Pr.append(P)
	dist.append(d)

plt.subplot(2,2,1)
plt.plot(dist, Pr)

Pr=list()
dist=list()
#path loss's SINR
for d in range(1,1000):
	g=((ht*hr)**2)/(d**4)
	P=g*Pt*Gt*Gr
	SINR=P/(N+interference)
	Pr.append(10*math.log10(SINR))
	dist.append(d)

plt.subplot(2,2,3)
plt.plot(dist, Pr)

Pr=list()
dist=list()
#path loss and shadowing 
for d in range(1,1000):
	g=((ht*hr)**2)/(d**4)
	P=(10**(np.random.normal(0,6)/10))*g*Pt*Gt*Gr
	Pr.append(10*math.log10(P))
	dist.append(d)

plt.subplot(2,2,2)
plt.plot(dist, Pr)

Pr=list()
dist=list()
#path loss and shadowing's SINR
for d in range(1,1000):
	g=((ht*hr)**2)/(d**4)
	P=(10**(np.random.normal(0,6)/10))*g*Pt*Gt*Gr
	SINR=P/(N+interference)
	Pr.append(10*math.log10(SINR))
	dist.append(d)

plt.subplot(2,2,4)
plt.plot(dist, Pr)
plt.show()
