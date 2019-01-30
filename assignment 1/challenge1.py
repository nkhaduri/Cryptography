import codecs
import binascii

hex_text = input()
print(binascii.b2a_base64(codecs.decode(hex_text.strip(), 'hex')).decode() )