import base64
import codecs

def hamming(s1, s2):
    s1 = bytes(s1, 'utf-8')
    s2 = bytes(s2, 'utf-8')
    data1, data2 = '', ''
    for byte in s1:
            data1 += ''.join([str(1 if (1<<x)&byte>0 else 0) for x in range(7,-1,-1)])
    for byte in s2:
            data2 += ''.join([str(1 if (1<<x)&byte>0 else 0) for x in range(7,-1,-1)])
            
    return sum([data1[i] != data2[i] for i in range(len(data1))])

b64_decoded = codecs.decode(base64.b64decode(input().strip()), 'utf-8')
distances = {}
for key_size in range(2, 41):
    distances[hamming(b64_decoded[:key_size], b64_decoded[key_size: 2*key_size]) / key_size] = key_size
key_sizes = [distances[key] for key in sorted(distances)][:18]

keys = []
score_sums = []
for key_size in key_sizes:
    blocks = [b64_decoded[key_size*i: key_size*(i+1)] for i in range(len(b64_decoded)//key_size)]
    rem_block = b64_decoded[key_size * (len(b64_decoded)//key_size):]

    transposed_blocks = [''.join([blocks[i][j] for i in range(len(blocks))]) for j in range(key_size)]
    for i in range(len(rem_block)):
        transposed_blocks[i] += rem_block[i]

    key = ''
    score = 0
    for txt in transposed_blocks:
        possible = []
        
        for a in range(0, 128): 
            k = chr(a) * len(txt)
            possible.append(codecs.decode(bytes(x^y for x,y in zip(bytes(k, 'utf-8'), bytes(txt, 'utf-8')) ), 'utf-8') )

        english_freq = [8.17, 1.29, 2.78, 4.25, 12.7, 2.23, 2.02, 6.09, 6.97, 0.15, 0.77, 4.03, 2.41, 6.75, 7.51, 1.93, 0.1, 5.99, 6.33, 9.06, 2.76, 0.98, 2.36, 0.15, 1.97, 0.07]
        scores = []
        for text in possible: 
            text = text.lower()
            freq = [0.0] * 26
            penalty = 0
            for i in range(len(text)):
                symb = text[i]
                ind = ord(symb) - ord('a')
                if 0 <= ind < 26:
                    freq[ind] += 1.0/len(text)
                elif symb != ' ':
                    penalty += 100
                else:
                    penalty -= 10
            scores.append(sum([(a-b)**2 for a,b in zip(english_freq, freq)]) + penalty)
        key += chr(scores.index(min(scores)))
        score += min(scores)
    
    keys.append(key)
    score_sums.append(score)
# print(score_sums)
key = keys[score_sums.index(min(score_sums))]
key = (key * (len(b64_decoded) // len(key) + 1))[:len(b64_decoded)]
print ( ''.join(chr(x^y) for x,y in zip(bytes(key, 'utf-8'), bytes(b64_decoded, 'utf-8') ) ) )