import math
import numpy as np
import matplotlib.pyplot as plt
#基地台功率
Pt=(10**(33/10))/1000
#手機功率
Pt_m=(10**(23/10))/1000
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
UE_x_b=list()
UE_y_b=list()
BS_x=list()
BS_y=list()

dist=list()
#bonus
dist_b=list()
#p received
Pr=list()
#p mobile 發
Pr_m=list()
Pr_dB=list()
Pr_m_dB=list()
#bonus
Pr_m_b=list()
Pr_m_dB_b=list()
#p BS received
Pr_BS=list()
#SINR at UE
SINR_UE=list()
#SINR at BS
SINR_BS=list()
#bonus
SINR_BS_b=list()

#19個BS的座標
BSs=[(0,0),(1000,0),(-1000,0),(0,1000),(0,-1000),(0,500),(0,-500),(250*s3,250),(-250*s3,250),(-250*s3,-250),(250*s3,-250),(250*s3,500*s3),(-250*s3,500*s3),(-250*s3,-500*s3),(250*s3,-500*s3),(500*s3,500),(-500*s3,500),(-500*s3,-500),(500*s3,-500)]

#downlink
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

			#BS發,downlink
			P = g*Pt*Gt*Gr
			Pr.append(P)
			Pr_dB.append(10*math.log10(P))

			#手機發,uplink
			P_m = g*Pt_m*Gt*Gr
			Pr_m.append(P_m)
			Pr_m_dB.append(10*math.log10(P_m))

			Pi=0
			#計算其他基地台的interference			
			for i in range(1,19):
				d=( (BSs[i][0]-x)**2 + (BSs[i][1]-y)**2 )**0.5
				g=((ht*hr)**2)/(d**4)
				Pi+=g*Pt*Gt*Gr

			SINR_UE.append(10*math.log10(P/(Pi+N)))

			break

#uplink
#SINR at BS 
for i in range(50):

	SINR_BS.append(10*math.log10(Pr_m[i]/(sum(Pr_m)-Pr_m[i]+N)))

#1-1
plt.subplot(3,2,1)
plt.plot(UE_x,UE_y,'o',0,0,'x')
#1-2
plt.subplot(3,2,3)
plt.plot(dist,Pr_dB,'o')
#1-3
plt.subplot(3,2,5)
plt.plot(dist,SINR_UE,'o')
#2-1
plt.subplot(3,2,2)
plt.plot(UE_x,UE_y,'o',0,0,'x')
#2-2
plt.subplot(3,2,4)
plt.plot(dist,Pr_m_dB,'o')
#2-3
plt.subplot(3,2,6)
plt.plot(dist,SINR_BS,'o')
plt.show()


#bonus
for e in BSs:			
	BS_x.append(e[0])
	BS_y.append(e[1])
	for i in range(50):
		while 1:
			x=np.random.uniform(-500/s3,500/s3)
			y=np.random.uniform(-500/s3,500/s3)
			#須滿足六角形的方程式
			if y+s3*x-500<0 and y-250<0 and y-s3*x-500<0 and y+s3*x+500>0 and y+250>0 and y-s3*x+500>0:
				r=(x**2+y**2)**0.5
				dist_b.append(r)
				g=((ht*hr)**2)/(r**4)
				P_m = g*Pt_m*Gt*Gr
				Pr_m_b.append(P_m)
				Pr_m_dB_b.append(10*math.log10(P_m))

				x+=e[0]
				y+=e[1]
				UE_x_b.append(x)
				UE_y_b.append(y)

				break

#19個BS
for i in range(19):
	#每個中的50個UE
	for j in range(50):
		interference=0
		#所有其他UE
		for k in range(50*19):
			#自己的case
			if k==i*50+j:
				continue
			else:
				#此BS對另一個ue的距離
				r=((BS_x[i]-UE_x_b[k])**2+(BS_y[i]-UE_y_b[k])**2)**0.5
				g=((ht*hr)**2)/(r**4)
				P_m = g*Pt_m*Gt*Gr
				interference+=P_m

		SINR_BS_b.append(10*math.log10(Pr_m_b[i*50+j]/(interference+N)))

plt.subplot(3,1,1)
plt.plot(BS_x,BS_y,'o')
plt.plot(UE_x_b,UE_y_b,'x')
plt.subplot(3,1,2)
plt.plot(dist_b,Pr_m_dB_b,'o')
plt.subplot(3,1,3)
plt.plot(dist_b,SINR_BS_b,'o')
plt.show()