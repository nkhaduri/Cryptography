key = input().strip()
text = input().strip()

key = (key * (len(text) // len(key) + 1))[:len(text)]

print ( bytes(x^y for x,y in zip(bytes(key, 'utf-8'), bytes(text, 'utf-8')) ).hex() )