import codecs

n = int(input().strip())

strings = [input().strip() for i in range(n)]

decoded_scores = {} 
for txt in strings:
    possible = []

    for a in range(1, 128): 
        key = chr(a) * len(txt)
        possible.append(codecs.decode(bytes(x^y for x,y in zip(bytes(key, 'latin-1'), bytes.fromhex(txt)) ), 'latin-1') )

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
                penalty += 10
            else:
                penalty -= 1
        scores.append(sum([(a-b)**2 for a,b in zip(english_freq, freq)]) + penalty)

    decoded_scores[min(scores)] = possible[scores.index(min(scores))]
print(decoded_scores[sorted(decoded_scores)[0]])