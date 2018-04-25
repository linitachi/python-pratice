a=90

def fw(n):
	i=2
	print(n,'=',end="")
	while 1:
		if(n%i==0):
			print(i,end="")
			if(n!=i):
				print('*',end="")
			n=n/i
			continue
		if(i>n):
			print("\n結束")
			break
		i+=1
	

fw(a)