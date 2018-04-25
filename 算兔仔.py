def rabit(n):
	for www in range(1,n+1):
		print("第",www,"個月:",fi(www),sep="")
		
def fi(n):
	if( n==1 or n==2):
		return 1
	elif(n>2):
		return fi(n-1)+fi(n-2)
a=input("請輸入月數:")
print(a)
rabit(a)