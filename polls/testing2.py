from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
import requests
import json


auth = {'username': (None, 'ubnt'), 'password': (None, 'access')}
get1 = requests.get('http://10.1.85.29/login.cgi')
post = requests.post('http://10.1.85.29/login.cgi', files=auth, cookies = get1.cookies)
get2 = requests.get('http://10.1.85.29/161111.1236/status.cgi', cookies = get1.cookies)
cont = get2.content
co = get2.cookies
    #c = cont.json()
json2Dict = json.loads(cont)
myKey = json2Dict["host"]

#c = json2Dict.json()

stringkey = str(myKey)

myKey2 = json.dumps(myKey)

#c = myKey2.json()

print(myKey)


    for key, value in myKey2.items():
        myKey.update({key:value}
        