def rabit(n):
	for www in range(1,n+1):
		print("��",www,"�Ӥ�:",fi(www),sep="")
		
def fi(n):
	if( n==1 or n==2):
		return 1
	elif(n>2):
		return fi(n-1)+fi(n-2)
a=input("�п�J���:")
print(a)
rabit(a)