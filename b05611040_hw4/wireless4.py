import math
import numpy as np
import matplotlib.pyplot as plt

#基地台功率
Pt=(10**(33/10))/1000
#手機功率
Pt_m=(10**(0/10))/1000
#gain
Gt=10**(14/10)
Gr=10**(14/10)
ht=50+1.5
hr=1.5
k=1.38*10**(-23)
T=273+27
B=10*(10**6)
N=k*T*B
s3=3**0.5

UE_x=list()
UE_y=list()
dist=list()
SINR_UE=list()
C=list()
loss_rate=list()
loss_rate_b=list()
traffic=list()
traffic_b=list()

#19個BS的座標
BSs=[(0,0),(0,500),(0,1000),(0,-500),(0,-1000),(250*s3,250),(-250*s3,250),(-250*s3,-250),(250*s3,-250),(250*s3,750),(-250*s3,750),(-250*s3,-750),(250*s3,-750),(500*s3,500),(-500*s3,500),(-500*s3,-500),(500*s3,-500),(500*s3,0),(-500*s3,0)]

for i in range(50):
	while 1:
		x=np.random.uniform(-500/s3,500/s3)
		y=np.random.uniform(-500/s3,500/s3)
		#須滿足六角形的方程式
		if y+s3*x-500<0 and y-250<0 and y-s3*x-500<0 and y+s3*x+500>0 and y+250>0 and y-s3*x+500>0:
			UE_x.append(x)
			UE_y.append(y)

			#距離
			r=(x**2+y**2)**0.5
			dist.append(r)
			#path loss
			g=((ht*hr)**2)/(r**4)

			P = g*Pt*Gt*Gr
			Pi=0

			#計算其他基地台的interference			
			for i in range(1,19):
				d=( (BSs[i][0]-x)**2 + (BSs[i][1]-y)**2 )**0.5
				g=((ht*hr)**2)/(d**4)
				Pi+=g*Pt*Gt*Gr

			SINR=P/(Pi+N)
			C.append(B*math.log2(1+SINR))

			break
#print(C)

#traffic為constant時
for x in range(1024*1024,2*8*4*1024*1024+1,1024*1024*8):
	traffic.append(x)
	buf=0
	error=0
	for i in range(1000):
		for e in C:
			if e<x:
				if buf > 6*8*1024*1024:
					error+=x-e
				else:
					buf+=x-e

	loss_rate.append(error/float(x*50*1000))
	#print(x*50*1000)
	#print(error)

print(traffic)
print(loss_rate)

#traffic 為 poisson時
for lamb in range(1024*1024,2*8*4*1024*1024+1,1024*1024*8):
	traffic_b.append(lamb)
	buf=0
	error=0	
	for e in C:
		for i in range(1000):
			x=np.random.poisson(lamb)
			if e<x:
				if buf > 6*8*1024*1024:
					error+=x-e
				else:
					buf+=x-e

	loss_rate_b.append(error/float(x*50*1000))
	#print(x*50*1000)
	#print(error)
print(traffic_b)
print(loss_rate_b)

#1-1
plt.plot(0,0,'x')
plt.plot(UE_x,UE_y,'o')
plt.show()

#1-2
plt.plot(dist,C,'o')
plt.show()

#1-3
plt.bar(traffic,loss_rate,width=1024*1024*6)
plt.show()

#B-1
plt.plot(0,0,'x')
plt.plot(UE_x,UE_y,'o')
plt.show()

#B-2
plt.plot(dist,C,'o')
plt.show()

#B-3
plt.bar(traffic_b,loss_rate_b,width=1024*1024*6)
plt.show()