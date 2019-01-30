import sys
from oracle import *

block_size = 16

def forge(cipher_file):
	with open(cipher_file, 'r') as file:
		data = file.read()
		blocks = [data[i*block_size: (i+1)*block_size] for i in range(len(data)/block_size)]
		if len(data) % block_size != 0:
			blocks.append(data[(len(data)/block_size) * block_size:])

		if len(blocks)%2 != 0:
			print "Number of blocks should be even"
			return
			
		Oracle_Connect()
		t0 = Mac(blocks[0] + blocks[1], min(2 * block_size, len(data)))

		for i in range(2, len(blocks)-1, 2):
			new_m = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(blocks[i], str(t0))) + blocks[i+1]
			t0 = Mac(new_m, len(new_m))

		print t0

		Oracle_Disconnect()

forge(sys.argv[1])