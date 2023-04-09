import datetime
import base64
import urllib.parse
import requests


url_base = 'https://apiarribos.sofse.gob.ar/v1'
auth_url = '/auth/authorize'

def generarToken():
  username = generateUsername()
  password = encodePass(username)
  getToken=requests.post(url_base+auth_url,data={ 'username' : username, 'password' : password})
  return getToken.json()['token']

def generateUsername():
    user=Encoder()
    return user.timestamp().base64().tostring()

def encodePass(username):
    password=Encoder(username)
    return password.base64().cipher(0).reverse().base64().cipher(1).reverse().url().tostring()


class Encoder():
    def __init__(self,string=''):
        self.str=string
    def timestamp(self):
        date = str(datetime.datetime.now())
        self.str = date.split(' ')[0].replace('-','')+'sofse'
        return self
    def base64(self):
        message = self.str
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_string = base64_bytes.decode('ascii')
        self.str = base64_string
        return self
    def tostring(self):
        return self.str
  
    def reverse(self):
        self.str = self.str[::-1]
        return self
    
    def cipher(self,step): 
        self.str = reduce(lambda acc, curr: acc.replace(curr['in'], curr['out'][step]), cipher,initializer=self.str)
        return self
    
    def url(self):
        self.str = urllib.parse.quote(self.str, safe='')
        return self

cipher= [
    { 'in': 'a', 'out': ['#t', '#t'] },
    { 'in': 'e', 'out': ['#x', '#p'] },
    { 'in': 'i', 'out': ['#f', '#w'] },
    { 'in': 'o', 'out': ['#l', '#8'] },
    { 'in': 'u', 'out': ['#7', '#0'] },
    { 'in': '=', 'out': ['#g', '#v'] }]


def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer
    for element in it:
        value = function(value, element)
    return value

token=generarToken()
print(token)
