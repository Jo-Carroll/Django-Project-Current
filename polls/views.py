from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
from django.template import loader
import requests
import json
from urllib.parse import urlparse

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
    urlvar = "10.1.85.29" #insert variable gotten from js here
    loginurl = "http://{0}/login.cgi".format(urlvar)
    statusurl = "http://{0}/status.cgi".format(urlvar)
    auth = {'username': (None, 'ubnt'), 'password': (None, 'access')} #authenticate page
    get1 = requests.get(loginurl)
    post = requests.post(loginurl, files = auth, cookies = get1.cookies)
    get2 = requests.get(statusurl, cookies = get1.cookies)
    cont = get2.content # return the contents of the page (json)
    co = get2.cookies #irrelevant
    json2Dict = json.loads(cont) #format the contents as a json object
    wireless = json2Dict["wireless"] #get specific elements from the json 
    host = json2Dict["host"]
    myKey = {}

    for key, value in wireless.items():
        if key == "distance":
            myKey[key] = value
        elif key == "signal":
            myKey[key] = value


    for key, value in host.items():
        if key == "hostname":
            myKey[key] = value

    print(myKey)

    return JsonResponse(myKey)


