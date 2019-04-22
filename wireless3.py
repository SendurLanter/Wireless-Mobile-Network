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

users=list()
UE_x=list()
UE_y=list()

#19個BS的座標
BSs=[(0,0),(0,500),(0,1000),(0,-500),(0,-1000),(250*s3,250),(-250*s3,250),(-250*s3,-250),(250*s3,-250),(250*s3,750),(-250*s3,750),(-250*s3,-750),(250*s3,-750),(500*s3,500),(-500*s3,500),(-500*s3,-500),(500*s3,-500),(500*s3,0),(-500*s3,0)]

class UE:

	def __init__(self,x,y,h):
		self.x=x
		self.y=y
		self.h=h
		self.change_status()

	def check_expire(self):
		if self.t==0:
			return True
		else:
			return False

	def change_status(self):
		self.t=np.random.randint(1,6)
		self.theta=np.random.uniform(0,np.pi*2)
		self.speed=np.random.uniform(1,15)

	def update(self):
		self.x+=self.speed*np.cos(self.theta)
		self.y+=self.speed*np.sin(self.theta)
		self.t-=1

	def handover(self,h):
		self.h=h

for i in range(100):
	while 1:
		x=np.random.uniform(-500/s3,500/s3)
		y=np.random.uniform(-500/s3,500/s3)

		if y+s3*x-500<0 and y-250<0 and y-s3*x-500<0 and y+s3*x+500>0 and y+250>0 and y-s3*x+500>0:
			which_BS=np.random.randint(0,19)
			x+=BSs[which_BS][0]
			y+=BSs[which_BS][1]
			users.append(UE(x,y,which_BS))
			UE_x.append(x)
			UE_y.append(y)
			break

count=0
interference_sum=list()
#initialize
for e in users:
	interference_sum.append(0)

#900秒,動作以秒為單位掃描
for i in range(900):

	#100個user
	for e in users:
		
		#如果上個路線走完了
		if e.check_expire():
			#擲骰子走下一步
			e.change_status()
		else:
			#user i的回合,開始走
			e.update()
			
			#走完後檢查有沒有handover發生
			#掃描19個bs看看是否在附近
			for j in range(len(BSs)):
				#user與BSj的距離
				d2 = ((e.x-BSs[j][0])**2+(e.y-BSs[j][1])**2)**0.5
				
				#先判定地理狀況(外接圓形) 與其中一個bs的距離如果小於她
				if d2<250 and j!=e.h:

					#接著算那瞬間的uplink SINR的interference 所有的user對一特定bs的
					for m in range(len(BSs)):
						if m==j or m==e.h:
							for k in users:
								d = ((k.x-BSs[m][0])**2+(k.y-BSs[m][1])**2)**0.5
								g = ((ht*hr)**2)/(d**4)
								P = g*Pt*Gt*Gr
								interference_sum[m]+=P

					d1 = ((e.x-BSs[e.h][0])**2+(e.y-BSs[e.h][1])**2)**0.5
					g1 = ((ht*hr)**2)/(d1**4)
					P1 = g1*Pt*Gt*Gr

					g2 = ((ht*hr)**2)/(d2**4)
					P2 = g2*Pt*Gt*Gr

					#SINR比較,如果接近的基地台距離小於外接圓半徑且SINR又高, 則handover
					if 10*math.log10(P2/(interference_sum[j]+N-P2)) > 10*math.log10(P1/(interference_sum[e.h]+N-P1)):
						print('time: '+str(i)+'s Source cell ID :'+str(e.h+1)+' Destination cell ID '+str(j+1))
						count+=1
						e.handover(j)
					
					interference_sum[e.h]=0
					interference_sum[j]=0
#B-3
print(count)
#B-1
for i in range(len(BSs)):
	plt.text(BSs[i][0], BSs[i][1], str(i+1),)
	plt.plot(BSs[i][0],BSs[i][1],'o')
plt.show()
#B-2
for i in range(len(BSs)):
	plt.text(BSs[i][0], BSs[i][1], str(i+1),)
	plt.plot(BSs[i][0],BSs[i][1],'o')
plt.plot(UE_x,UE_y,'o')
plt.show()