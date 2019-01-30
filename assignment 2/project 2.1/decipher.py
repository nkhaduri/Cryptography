import sys
import copy
from oracle import *

block_size = 16
char_ords = [32] + range(97, 123) + range(65, 91) + [44, 46, 33, 63, 40, 41, 39, 34] + range(58, 63) + range(48, 58) +\
			range(35, 39) + [42, 43, 45, 47, 64] + range(91, 97) + range(123, 127)

def pad_block(block, pad_len, g, prev_g):
	block[block_size - pad_len] = prev_g ^ g ^ pad_len ^ block[block_size - pad_len] ^ (pad_len if prev_g != 0 else 0)
	if prev_g == 0:
		for i in range(block_size - pad_len + 1, block_size):
			block[i] = pad_len ^ block[i] ^ (pad_len - 1)

def decipher_block(cipher, ind):
	message_block = ''
	for i in range(block_size-1, -1, -1):
		prev_g = 0
		for g in char_ords:
			pad_block(cipher[ind-1], block_size - i, g, prev_g)
			if Oracle_Send([a for subl in cipher[:ind+1] for a in subl], ind+1):
				message_block = chr(g) + message_block
				break
			prev_g = g
	return message_block

def decipher_last_block(cipher):
	real_pad = 0
	for pad_len in range(block_size, 0, -1):
		cipher[-2][-1] ^= pad_len ^ ((pad_len+1) if pad_len != block_size else 1)
		if Oracle_Send([a for subl in cipher for a in subl], len(cipher)):
			cipher[-2][-1] ^= pad_len ^ 1
			real_pad = pad_len
			break
	for i in range(real_pad):
		cipher[-2][block_size - i - 1] ^= real_pad
	message_block = ''
	for i in range(block_size - real_pad - 1, -1, -1):
		prev_g = 0
		pad_len = block_size - i
		for g in char_ords:
			cipher[-2][i] ^= prev_g ^ g ^ pad_len ^ (pad_len if prev_g != 0 else 0)
			if prev_g == 0:
				for j in range(i + 1, block_size):
					cipher[-2][j] ^= pad_len ^ (pad_len - 1 if pad_len != real_pad+1 else 0)
			if Oracle_Send([a for subl in cipher for a in subl], len(cipher)):
				message_block = chr(g) + message_block
				break
			prev_g = g
	return message_block

def decipher(cipher_file):
	with open(cipher_file, 'r') as file:
		data = bytearray(file.read().decode('hex'))
		cipher = [data[i*block_size: (i+1)*block_size] for i in range(len(data)/block_size)]
		full_message = ''
		for i in range(1, len(cipher)-1):
			full_message += decipher_block(copy.deepcopy(cipher), i)
		full_message += decipher_last_block(copy.deepcopy(cipher))
		print full_message

Oracle_Connect()
decipher(sys.argv[1])
Oracle_Disconnect()