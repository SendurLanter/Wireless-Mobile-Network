import matplotlib.pyplot as plt
import os
import numpy as np
#os.environ['CUDA_VISIBLE_DEVICE']='0'
class request:
	def __init__(self,name,source):
		self.name=name
		self.source=source
class file:
	def __init__(self, file_name):
		self.file_name = file_name
		self.count = 0
		self.score = 0
class user:
	def __init__(self):
		self.watching = False
		self.watched = list()
		self.wait_watch = list()
		self.interaction = [0]*1900
users=list()
requests=list()
interaction=list()
social_factor=list()
#init
def init():
	for i in range(1900):
		users.append(user())
	with open('CollegeMsg.txt','r') as f:
		edge=f.read().split()
		i=0
		while i+1<len(edge):
			users[int(edge[i])].interaction[int(edge[i+1])] += 1
			users[int(edge[i+1])].interaction[int(edge[i])] += 1
			i+=3
		for i in range(1900):
			m=float(max(users[i].interaction))
			if m==0:
				continue
			for j in range(1900):
				users[i].interaction[j]/=m
		for i in range(1900):
			social_factor.append(sum(users[i].interaction))

capacity=333
interval=50
watch_num=6
times=10
file_num=1000
cache_list=list()
cache_list2=list()
cache_list3=list()
n1=list()
n2=list()
n3=list()
n4=list()
n5=list()
buf=list()
for i in range(file_num):
	buf.append(file(i))
t=range(interval)
x=range(times)
init()

for n in range(times):
	h1=list()
	h2=list()
	h3=list()
	h4=list()
	h5=list()
	#LFU
	cache_list4=list()
	#greedy
	cache_list5=list()
	occupation5=0
	capacity += 100
	for e in range(int(capacity/100)):
		cache_list4.append(int(np.random.chisquare(500)))

	for i in range(interval):
		#creat files
		files=list()
		for j in range(file_num):
			new_file=file(j)
			files.append(new_file)

		#update requests
		requests=list()
		for j in range(1900):
			if np.random.poisson(2)>=2:
				a=int(np.random.chisquare(500))
				while a>=1000 or a<0 or a in users[j].watched:
					a=int(np.random.chisquare(500))
				requests.append(request(a,j))
				users[j].watched.append(a)
				for k in range(1900):
					if users[k].interaction[j] !=0:
						if np.random.rand() <= users[k].interaction[j]:
							if a not in users[k].watched:
								users[k].wait_watch.append(a)
		for e in requests:
			files[e.name].count+=1
			buf[e.name].count+=1
			files[e.name].score+=social_factor[e.source]

		#wait_watch and spread
		for j in range(1900):
			if len(users[j].wait_watch)>0:
				w = np.random.poisson(3)
				for e in range(w):
					try:
						a = users[j].wait_watch.pop()
						requests.append(request(a,j))
						users[j].watched.append(a)
						for k in range(1900):
							if users[k].interaction[j] !=0:
								if np.random.rand() <= users[k].interaction[j]:
									if a not in users[k].watched:
										users[k].wait_watch.append(a)
					except:
						break
			users[j].wait_watch.clear()

		for e in requests:
			buf[e.name].count+=1
			files[e.name].score+=social_factor[e.source]

		for j in range(1900):
			users[j].watched.clear()

		hit1=0
		hit2=0
		hit3=0
		hit4=0
		hit5=0

		for e in requests:
			if e.name in cache_list:
				hit1+=1
			if e.name in cache_list2:
				hit2+=1
			if e.name in cache_list3:
				hit3+=1
			if e.name in cache_list4:
				hit4+=1
			if e.name in cache_list5:
				hit5+=1

		print(len(requests))
		print(n)
		h1.append(hit1/(len(requests)+1))
		h2.append(hit2/(len(requests)+1))
		h3.append(hit3/(len(requests)+1))
		h4.append(hit4/(len(requests)+1))
		h5.append(hit5/(len(requests)+1))
		cache_list.clear()
		cache_list2.clear()
		cache_list3.clear()
		occupation=0
		occupation2=0
		occupation3=0
		occupation4=0

		while occupation3 <=capacity:
			cache_list3.append(np.random.randint(300,700))
			occupation3 += 100

		buf.sort(key=lambda x: x.count, reverse=False)
		for e in buf:
			if e.file_name in cache_list4:
				cache_list4.remove(e.file_name)
				for i in range(1,len(buf)):
					if buf[-i].file_name not in cache_list4:
						cache_list4.append(buf[-i].file_name)
						break
			if e.file_name in cache_list4:
				cache_list4.remove(e.file_name)
				for i in range(1,len(buf)):
					if buf[-i].file_name not in cache_list4:
						cache_list4.append(buf[-i].file_name)
						break
			break

		files.sort(key=lambda x: x.score, reverse=True)
		for e in files:
			if occupation <=capacity:
				if e.file_name not in cache_list:
					cache_list.append(e.file_name)
					occupation += 100
			else:
				break
		for e in files:
			if occupation5 <=capacity:
				if e.file_name not in cache_list5:
					cache_list5.append(files[0].file_name)
					occupation5 += 100
					break
		print(cache_list4)

		files.sort(key=lambda x: x.count, reverse=True)

		for e in files:
			if occupation2 <=capacity:
				if e.file_name not in cache_list2:
					cache_list2.append(e.file_name)
					occupation2 += 100
			else:
				break
	n1.append(sum(h1)/interval)
	n2.append(sum(h2)/interval)
	n3.append(sum(h3)/interval)
	n4.append(sum(h4)/interval)
	n5.append(sum(h5)/interval)
	#plt.plot(t,h1,"g")
	#plt.plot(t,h2,"b")
	#plt.plot(t,h3,"r")
	#plt.plot(t,h4,"y")
plt.plot(x,n1,"g")
plt.plot(x,n2,"b")
plt.plot(x,n3,"r")
plt.plot(x,n4,"y")
plt.plot(x,n5,"m")
plt.show()