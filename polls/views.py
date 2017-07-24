from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
from django.template import loader
import requests
import json
from urllib.parse import urlparse
from .models import Temp
import re
import math



def index(request):
    template = loader.get_template('polls/index.html')
    context = {
        "words": "Here are some words for you"
    }
    return HttpResponse(template.render(context, request))


def main(request):
    template = loader.get_template('polls/main.html')
    context = {}
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
        if "cpuload" in host:
            myKey["cpuload"] = int(host["cpuload"])
        else:
            myKey["cpuload"] = False

        for key, value in wireless.items():
            if key == "distance":
                dis = value /1609.34 
                myKey[key] = "About " + str(round(dis, 2)) + " miles"
            elif key == "signal":
                if abs(int(value)) > 70:
                    myKey[key] = str(value) + " (Weak signal) "
                    myKey["signalint"] = abs(int(value))
                elif 70 >= abs(int(value)) > 65:
                    myKey[key] = str(value) + " (Decent signal) "
                    myKey["signalint"] = abs(int(value))
                elif abs(int(value)) < 65:
                    myKey[key] = str(value) + " (Strong signal) "
                    myKey["signalint"] = abs(int(value))

        for key, value in host.items():
            if key == "hostname":
                myKey["hostname"]  = value.split("[", 1)[0]
                if "SL" in value:
                    myKey["package"] = "Smart Link"
                elif "EL" in value:
                    myKey["package"] = "Elite Link"

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
        myKey["uptime"] = str(round(float(host["uptime"]) /120, 2)) 
        myKey["upsec"] = str(round(float(host["uptime"]), 2))
        seconds = int(host["uptime"])
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        myKey["uptime"] = ("%d:%02d:%02d" % (h, m, s))
        if (seconds / 120) < 120:
       #     myKey["uptime"] = str(round(float(host["uptime"]) /60 /60)) + " minutes"
            myKey["color"] = True
        elif (seconds / 120) >= 120:
       #     myKey["uptime"] = str(round(float(host["uptime"]) /60 /60, 2)) + " hours"
             myKey["color"] = False
        dlspeed = round(int(interfaces[1]["stats"]["tx_bytes"]), 2)
        print(dlspeed)
        myKey["RX"] = dlspeed
        myKey["TX"] = dlspeed #int(interfaces[1]["stats"]["tx_bytes"]) * 8 /100000
    #check the uptime and return a bool and/or a string (add that to myKey)

        return JsonResponse(myKey)
     else:
        return HttpResponse("The page has died")

def lan(request):
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

        txspeed = round(float(wireless["txrate"]), 2)
        print(txspeed)
        myKey["TX"] = txspeed
        return JsonResponse(myKey) 

