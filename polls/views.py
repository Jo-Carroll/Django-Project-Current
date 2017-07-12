from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
from django.template import loader
import requests
import json
from urllib.parse import urlparse
from .models import Temp
import re



def index(request):
    template = loader.get_template('polls/index.html')
    context = {
        "words": "Here are some words for you"
    }
    return HttpResponse(template.render(context, request))


def main(request):
    template = loader.get_template('polls/main.html')
    context = {

    }
    return HttpResponse(template.render(context,request))
    

def status(request):
    if request.method == 'GET':
        global IP
        IP = request.GET.get('IP')

    loginurl = "http://{0}/login.cgi".format(IP)
    statusurl = "http://{0}/status.cgi".format(IP)
    auth = {'username': (None, 'ubnt'), 'password': (None, 'access')} #authenticate page
    get1 = requests.get(loginurl)
    post = requests.post(loginurl, files = auth, cookies = get1.cookies)
    json2Dict = json.loads(requests.get(statusurl, cookies = get1.cookies).content) #format the contents as a json object
    
    wireless = json2Dict["wireless"] #get specific elements from the json 
    host = json2Dict["host"]
    myKey = {}
    #get the cpu usage, check it, and if it is 100%, give an alert
    cputotal = int(host["cputotal"])
    cpubusy = int(host["cpubusy"])
    cpu = cpubusy / cputotal
    print(cpu)
  
    for key, value in wireless.items():
        if key == "distance":
            myKey[key] = str(value //5280) + " miles"
        elif key == "signal":
            if abs(int(value)) > 70:
                myKey[key] = str(value) + " (Bad signal) "
                myKey["signalint"] = abs(int(value))
            elif 70 >= abs(int(value)) > 65:
                myKey[key] = str(value) + " (Decent signal) "
                myKey["signalint"] = abs(int(value))
            elif abs(int(value)) < 65:
                myKey[key] = str(value) + " (Most excellent) "
                myKey["signalint"] = abs(int(value))

    for key, value in host.items():
        if key == "hostname":
            if "SL" in value:
             myKey[key] = value
             myKey["package"] = "Smart Link"

    return JsonResponse(myKey) 

def rates(request):
     if request.method == 'GET':
        global IP
        IP = request.GET.get('IP')

        loginurl = "http://{0}/login.cgi".format(IP)
        ratesurl =  "http://{0}/ifstats.cgi".format(IP)
        auth = {'username': (None, 'ubnt'), 'password': (None, 'access')} #authenticate page
        get1 = requests.get(loginurl)
        post = requests.post(loginurl, files = auth, cookies = get1.cookies)
        ratesDict = json.loads(requests.get(ratesurl, cookies = get1.cookies).content) #format the contents as a json object


        host = ratesDict["host"]
        interfaces = ratesDict["interfaces"]
        myKey = {}
        myKey["uptime"] = int(host["uptime"]) //120
        myKey["RX"] = int(interfaces[1]["stats"]["rx_bytes"]) * 8 /10000000
        myKey["TX"] = int(interfaces[1]["stats"]["tx_bytes"]) * 8 /10000000
    #check the uptime and return a bool and/or a string (add that to myKey)

        return JsonResponse(myKey)




