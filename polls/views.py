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
    myKey = {}
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
    if "cpuload" in host:
        myKey["cpuload"] = int(host["cpuload"])
    else:
        myKey["cpuload"] = False
    for key, value in wireless.items():
        if key == "distance":
            dis = value /1609.34 #convert to miles from meters
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
    return JsonResponse(myKey) 

def package(request):
    myKey = {}
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
    for key, value in host.items():
        if key == "hostname":
            if "SL" in value:
                myKey["package"] = "Smart Link"
            elif "EL" in value:
                myKey["package"] = "Elite Link"
            elif "PL" in value:
                myKey["package"] = "Power Link"
            myKey["hostname"]  = value.split("[", 1)[0]
    return JsonResponse(myKey) 

def rates(request):
    myKey = {}
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
        myKey["uptime"] = str(round(float(host["uptime"]) /120, 2)) 
        myKey["upsec"] = str(round(float(host["uptime"]), 2))
        seconds = int(host["uptime"])
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        myKey["uptime"] = ("%d hours, %2d minutes, aaaannnddd %2d seconds" % (h, m, s))
        if (seconds / 120) < 120:
            myKey["color"] = True
        elif (seconds / 120) >= 120:
             myKey["color"] = False
        indy = len(interfaces) - 1
        dlspeed = round(int(interfaces[indy]["stats"]["tx_bytes"]), 2)
        myKey["RX"] = dlspeed
        myKey["TX"] = dlspeed
        return JsonResponse(myKey)


def lan(request):
    myKey = {}
    if request.method == 'GET':
        global IP
        IP = request.GET.get('IP')
        loginurl = "http://{0}/login.cgi".format(IP)
        statusurl = "http://{0}/status.cgi".format(IP)
        auth = {'username': (None, 'ubnt'), 'password': (None, 'access')} #authenticate page
        get1 = requests.get(loginurl)
        post = requests.post(loginurl, files = auth, cookies = get1.cookies)
        json2Dict = json.loads(requests.get(statusurl, cookies = get1.cookies).content) #format the contents as a json object
        eth0 = json2Dict["interfaces"][0]["status"]["plugged"]
        myKey["eth"] = eth0

        return JsonResponse(myKey)

def lanabled(request):
    myKey = {}
    if request.method == 'GET':
        global IP
        IP = request.GET.get('IP')
    loginurl = "http://{0}/login.cgi".format(IP)
    statusurl = "http://{0}/status.cgi".format(IP)
    auth = {'username': (None, 'ubnt'), 'password': (None, 'access')} #authenticate page
    get1 = requests.get(loginurl)
    post = requests.post(loginurl, files = auth, cookies = get1.cookies)
    json2Dict = json.loads(requests.get(statusurl, cookies = get1.cookies).content) #format the contents as a json object
    if json2Dict["interfaces"][1]["enabled"] == True:
        myKey["enabled"] = True #json2Dict["interfaces"][1]["enabled"]
        return JsonResponse(myKey)
    else:
        badkey = {}
        badkey["enabled"] = False
        return JsonResponse(badkey)

def plex(request):
    myKey = {}
    if request.method == 'GET':
        global IP
        IP = request.GET.get('IP')
    loginurl = "http://{0}/login.cgi".format(IP)
    statusurl = "http://{0}/status.cgi".format(IP)
    auth = {'username': (None, 'ubnt'), 'password': (None, 'access')} #authenticate page
    get1 = requests.get(loginurl)
    post = requests.post(loginurl, files = auth, cookies = get1.cookies)
    json2Dict = json.loads(requests.get(statusurl, cookies = get1.cookies).content) #format the contents as a json object
    if json2Dict["interfaces"][1]["status"]["duplex"] == 1:
        myKey["plex"] = True
    elif json2Dict["interfaces"][1]["status"]["duplex"] == 0:
        myKey["plex"] = False
    return JsonResponse(myKey)



