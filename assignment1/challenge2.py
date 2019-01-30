hex1 = input().strip()
hex2 = input().strip()

print( bytes(x^y for x,y in zip(bytes.fromhex(hex1), bytes.fromhex(hex2)) ).hex())