import tkinter
from threading import Thread
from time import sleep, time
import numpy as np
import math

devicenumber = 40
#基地台功率
Pt=(10**(33/10))/1000
#手機功率
Pt_m=(10**(23/10))/1000
#gain
Gt=10**(14/10)
Gr=10**(14/10)
ht=7
hr=1.5
k=1.38*10**(-23)
T=273+27
B=10*(10**6)
Bd2d=5*10**6
N=k*T*B

userlist = list()
dots=list()
circles=list()
pairs=list()

class model():
	
	def __init__(self):
		#bs
		cell.create_oval(400-10, 400-10, 410, 410, fill = 'green')

		#生成device
		for i in range(devicenumber):
			x=np.random.normal(0,70)
			y=np.random.normal(0,70)
			device = user(x,y,i)
			userlist.append(device)
			dot = cell.create_oval(x+400, y+400, x+405, y+405, width = 3)
			dots.append(dot)


	def cal_interference(self):
		for i in range(devicenumber):
			count=0
			for j in range(devicenumber):
				if userlist[j].uploading :
					if j!=i :
						d = ((userlist[i].x-userlist[j].x)**2+(userlist[i].y-userlist[j].y)**2)**0.5
						g = ((hr*hr)**2)/(d**4)
						P = g*Pt_m*Gt*Gr
						count += P

			userlist[i].interference = count+N


	#處理是否要d2d與配對
	def parse_request(self,requests):
		count=1

		for e in requests:
			d2d=False
			choice=list()
			for i in range(devicenumber):
				if not userlist[i].uploading and e.source!=i and e.file_name in userlist[i].cache:
					#配對
					choice.append(i)
					d2d=True

			if d2d:
				#找最適合的pair
				distance=math.inf
				decision=None
				for h in choice:
					d=(userlist[h].x-userlist[e.source].x)**2+(userlist[h].y-userlist[e.source].y)**2
					if d<distance:
						distance=d
						decision=h
				userlist[decision].uploading = True
				userlist[e.source].pair = decision

			else:
				userlist[e.source].pair = devicenumber
				count+=1
		self.bs2d_num=count


	def polling(self):
		requests=list()

		for i in range(devicenumber):
			
			if not userlist[i].downloading :
				dice=np.random.poisson(2)

				#發request
				if dice > 5:
					requested_file = userlist[i].creat_request()
					requests.append(request(i,requested_file))
					userlist[i].downloading=True
					circle = cell.create_oval(userlist[i].x+400-5, userlist[i].y+400-5, userlist[i].x+410, userlist[i].y+410 ,fill = 'green')
					circles.append(circle)

		return requests

	def update_download(self):

		for i in range(devicenumber):
			#處理下載
			if userlist[i].downloading:
				if userlist[i].pair!=None:
									
					#d2d
					if userlist[i].pair != devicenumber:
						d = ( (userlist[i].x - userlist[userlist[i].pair].x)**2 + (userlist[i].y - userlist[userlist[i].pair].y)**2)**0.5
						g = ((hr*hr)**2)/(d**4)
						P = g*Pt_m*Gt*Gr
						Cd2d = Bd2d*math.log2( 1+ (P/(userlist[i].interference-P) ))

						d = ((userlist[i].x)**2+(userlist[i].y)**2)**0.5
						g = ((hr*hr)**2)/(d**4)
						P = g*Pt*Gt*Gr
						Cbs = B/self.bs2d_num/2*math.log2( 1+ (P/(userlist[i].interference) ))

						if Cd2d > Cbs:
							C=Cd2d
							line = cell.create_line(userlist[i].x+400, userlist[i].y+400, userlist[userlist[i].pair].x+400, userlist[userlist[i].pair].y+400,fill = 'blue',width = 2)
						else:
							C=Cbs
							line = cell.create_line(userlist[i].x+400, userlist[i].y+400,400,400,fill = 'red',width = 2)

					#bs2d
					else:
						d = ((userlist[i].x)**2+(userlist[i].y)**2)**0.5
						g = ((hr*hr)**2)/(d**4)
						P = g*Pt*Gt*Gr
						C=B/self.bs2d_num/2*math.log2( 1+ (P/(userlist[i].interference) )) 
						line = cell.create_line(userlist[i].x+400, userlist[i].y+400,400,400,fill = 'red',width = 2)
					pairs.append(line)
					
					userlist[i].remaining -= C
					

					#如果下載完了
					if userlist[i].remaining<=0 :
						print('done')
						if userlist[i].pair != devicenumber:
							userlist[userlist[i].pair].uploading=False
						userlist[i].downloading = False
						userlist[i].pair = None 


	def update_location(self):
		for i in range(devicenumber):
			#處理走路
			if not userlist[i].walking :
				dice=np.random.poisson(2)

				#決定走路
				if dice > 3:
					userlist[i].walking=True
					#direction=np.random.uniform(0,6.28)
					userlist[i].destination=[4*np.random.uniform(-0.5,0.5),4*np.random.uniform(-0.5,0.5),70]
			else:
				#print(userlist[j].x)
				userlist[i].walk()		


class user:

	def __init__(self,x,y,n):
		self.x=x
		self.y=y
		self.id=n
		self.pair=None
		self.interference=0
		self.downloading=False
		self.uploading=False
		self.walking=False
		self.destination=None
		self.cache=np.random.randint(30,70,20)
	
	def creat_request(self):
		a=-1
		while a<0 or a>100:
			a = np.random.normal(50,10)
		requested = int(a)
		self.remaining=10*1024*1024*8

		return requested

	def walk(self):
		self.x+=self.destination[0]
		#if self.x>600: self.x-=abs(self.destination[0])
		#if self.x<200: self.x+=abs(self.destination[0])
		self.y+=self.destination[1]
		#if self.y>600: self.y-=abs(self.destination[1])
		#if self.y<200: self.y+=abs(self.destination[1])
		self.destination[2]-=1
		cell.move(dots[self.id], self.destination[0], self.destination[1])
		if self.destination[2] == 0:
			self.walking=False


class request:
	def __init__(self,source,file_name):
		self.source=source
		self.file_name=file_name


def simulate():
	sleep(7)
	Model = model()

	for i in range(300):
		#sleep(0.01)
		start=time()
		#s_time=cell.create_text(100,150,text='time: '+str(i) +'s',font=('Arial', 20))
		for e in circles:
			cell.delete(e)
		circles.clear()
		#if len(pairs)>50:
		for e in pairs:
			cell.delete(e)
		pairs.clear()

		Model.update_location()	
		Model.cal_interference()
		Model.update_download()
		requests=Model.polling()
		Model.parse_request(requests)
		#cell.delete(s_time)
		while time()-start<0.05:
			pass

if __name__ == '__main__':
	root = tkinter.Tk()
	cell = tkinter.Canvas(root,width=800, height=800)
	cell.pack()
	Thread(target = simulate).start()
	root.mainloop()