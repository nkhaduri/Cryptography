from oracle import *
from helper import *

# modular inverse taken from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm 
def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, x, y = egcd(b % a, a)
		return (g, y - (b // a) * x, x)

def mod_inv(a, b):
	g, x, _ = egcd(a, b)
	if g == 1:
		return x % b
	else:
		return -1

def sign(challenge, N):
	Oracle_Connect()

	m = ascii_to_int(challenge)
	m1 = m/2
	m2 = (m*mod_inv(m1, N))%N
	m_inv_1 = mod_inv(Sign(1), N)
	print (Sign(m1) * Sign(m2) * m_inv_1)%N
	
	Oracle_Disconnect()
	

def main():
	challenge = 'Crypto is hard --- even schemes that look complex can be broken'
	N = 119077393994976313358209514872004186781083638474007212865571534799455802984783764695504518716476645854434703350542987348935664430222174597252144205891641172082602942313168180100366024600206994820541840725743590501646516068078269875871068596540116450747659687492528762004294694507524718065820838211568885027869
	sign(challenge, N)

if __name__ == '__main__':
	main()


