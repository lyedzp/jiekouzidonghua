#encoding=utf-8
from Crypto.Cipher import AES
# 加密，第一个参数是key,第二个参数是AES下的模式，第三个参数是IV
obj = AES.new('This is a key123',AES.MODE_CBC,'This is an IV456')
# message = "{'eid':'1','phone':'17380578335'}"
message = 'This is a key123'
#对message加密
ciphertext=obj.encrypt(message.encode('utf-8'))
print(ciphertext)