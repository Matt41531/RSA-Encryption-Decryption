from random import randint
import math

#AUTHOR: Matthew Rife
#START DATE: 4/2/18


#NOTICE: These top functions work but I decided to leave them out because they add lots of time to the program in return to making sure that the primality test doesn't get fooled by a Carmichael number.

'''
def gcd(a,b):
	if (a<b):
		return gcd(b,a)
	if (a%b) == 0:
		return b
	return gcd(b, a % b)



def Miller_Rabin(n):
	found = False
	if n & 1 == 0:
		return False
	else:
		s = 0
		d = n - 1
		while d & 1 == 0:
			s += 1
			d = d >> 1
		while not found:
			a = randint(2, n -2)
			x = pow(a, d, n)
			if x != 1 and x + 1 != n:
				for r in xrange(1,s):
					x = pow(x,2,n)
					if x == 1:
						return False
					elif x == n - 1:
						a = 0
						found = True
						break
				if a:
					return False
		return True



def is_Carmichael(n):
	b = 2
	while b < n:
		if (gcd(b, n) == 1):
			if (mod_expon(b, n - 1, n) != 1):
				return False
		b += 1
	return True			
'''

#PURPOSE: Generate x^a (mod n) for very large numbers very quickly ( runtime (O)(Log a)) using the binary method
#INPUT:values of the base x, the exponent a, and the modulo n
#OUTPUT: returns X^a (mod n)
def mod_expon(x,a,n):
	result = 1
	x = x % n
	while a > 0:
		if (a % 2 == 1):
			result = (result * x) % n
		a = a >> 1
		x = (x * x) % n
	return result


#PURPOSE: Determine if X is prime or composite
#INPUT: Value x
#OUTPUT: returns true or false for if x is probably prime or certainly composite
def is_prime(x):
	#Use fermats primality test if x is odd, otherwise discard
	#if x fails, discard otherwise proceed
	#use another method to ensure x is prime
	
	#Check if x is even, if so then x is not prime
	if (x % 2) == 0:
		return False
	#If x is odd, use fermats little theorem a^n-1 = 1 (mod n). So do the modular exponentiation and those with values 1 as the result may be prime
	else:
		result = mod_expon(2, x-1, x)
	
	if result == 1:
		#Do some more sophisticated testing here if needed
		return True
	else:
		return False

#PURPOSE: Calculate the the modular inverse of a number e mod n using euclids extended algorithm
#INPUT: With x = e^-1 (mod n), takes input e and n
#OUTPUT: value x as mentioned above, or nothing if there is no inverse
def euclid_extended(e, n):
	t = 0
	new_t = 1	
	r = n 
	new_r = e
	
	while not (new_r == 0):
		quotient = r / new_r
		t, new_t = new_t, t - quotient * new_t
		r, new_r = new_r, r - quotient * new_r
			
	if t < 0:
		t = t + n

	return t
			
#PURPOSE: Generate the public key (e, n) and the private key d
#INPUT: none
#OUTPUT:two separate files named private_key and public_key with their respective keys in each 
def key_setup():
	p = 0;
	q = 0;
	range_start = 10**(100-1)
	range_end = (10**100)-1
	found = False
	#Generate random integers with at least 100 integers then check it is prime. If so, that will be p
	while not found:
		num = randint(range_start, range_end)
		found = is_prime(num)
	p = num

	found = False
	#Generate random integers with at least 100 integers then check it is prime. If so, that will be q
	while not found:
		num = randint(range_start, range_end)
		found = is_prime(num)
	q = num
	
	n = p * q
	new_n = (p-1) * (q-1)
	e = 65537
	d = euclid_extended(e, new_n)
	with open("public_key.txt", 'w') as f:
		print >> f, n,",", e 
	
	with open("private_key.txt", 'w') as f:
		print >> f, d

#PURPOSE:encrypt the message from message.txt using the public key from public_key.txt
#INPUT:public_key.txt, message.txt, are required
#OUTPUT:ciphertext as a number in ciphertext.txt	
def encrypt():
	with open("public_key.txt", 'r') as f:
		buf = f.read()		
	
	#Add an error handling here in case the file doesn't have both n and e separated by a comma
	n, e = buf.split(",")
	n = int(n)
	e = int(e)
	with open("message.txt", 'r') as f:
		message = f.read()
		size = f.tell()
	print("ORIGINAL MESSAGE: " + message) 
	list_message = []
	#Divide message up into 82 character blocks
	for x in range(0, int(math.ceil(size/81.0))):
		list_message.append(message[(81*x):81*(x+1)])

	
	int_message = 0
	list_int_message = []
	count = 0
	for x in range(len(list_message)):
		#DEBUG:print("HERE IS A MESSAGE PART ")	
		#DEBUG:print(list_message[x])
		#Do a loop to run through each character, convert from ascii to integer
		for y in list_message[x]:
			y = ord(y) * (256**count )
			int_message += y	
			count += 1
		list_int_message.append(int_message)
		int_message = 0 
		count = 0
			
	
	#DEBUG:for x in range(len(list_int_message)):
	#	print("HERE IS A INT MESSAGE PART ")
	#	print(list_int_message[x])
	
	list_ciphertext = []

	for x in range(len(list_int_message)):
		ciphertext = mod_expon(list_int_message[x],e,n)
		list_ciphertext.append(ciphertext)
		
	str_ciphertext = ''
	str_ciphertext = ''.join(str(v) for v in list_ciphertext)
	#DEBUG:print("Final cipher ")
	#DEBUG:print(str_ciphertext)
	
	with open("ciphertext.txt", 'w') as f:
		for x in range(0,len(list_ciphertext)):
			if x < len(list_ciphertext) - 1:
				print >> f, list_ciphertext[x], ","
			else:
				print >> f, list_ciphertext[x]
		

#PURPOSE:decrypt the ciphertext and turn it back into the string message
#INPUT:ciphertext as a number from ciphertext.txt, public_key.txt, and private_key.txt
#OUTPUT:prints the decrypted message as a string
def decrypt():
	with open("ciphertext.txt", 'r') as f:
		ciphertext = f.read()
		size = f.tell()
	with open("private_key.txt", 'r') as f:
		d = f.read()
	d = int(d)
	with open("public_key.txt", 'r') as f:
		buf = f.read()
	n, e = buf.split(",")
	n = int(n)
	e = int(e)
	list_cipher = []
	message = []

	#Split the file up back into the blocks of ciphertext
	list_cipher = ciphertext.split(",")

	int_message = []

	#Decrypt the ciphertext using M = C^D (mod n)
	for x in range(0, len(list_cipher)):		
		int_message.append(mod_expon(int(list_cipher[x]), d, n))
		#DEBUG:print("int message = " + str(int_message[x]))
		
	ascii_values = []

	#Convert the int message into the correct ascii message
	for y in range(0, len(int_message)):
		for x in range(0, 81):
			message.append(int_message[y] % (256**(x + 1)))
			if x > 0:
				ascii_values.append((message[x + 81*y] - message[(x+81*y)-1])/(256**x))		
			else:
				ascii_values.append(message[x+ 81*y])

	




	final_message = ''
	final_message = ''.join(chr(v) for v in ascii_values)
	print("DECRYPTED MESSAGE: " + final_message)


def main():
	key_setup()
	encrypt()
	decrypt()

	
main();
