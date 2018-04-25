#n是跳幾次
def sss(n,h,sum,k,list):
	if(n>0):
		if(k==h):
			sum+=h
		else:
			sum+=2*h
		#print(sum)
		return sss(n-1,h/2,sum,0,list)
	else:
		#print(sum)
		list.insert(0,sum)
		list.insert(1,h)
		return list
h=100
list = [] 
a=sss(10,100,0,100,list)
print(a,'結果')