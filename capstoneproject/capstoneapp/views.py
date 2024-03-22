import string

from django.shortcuts import render
from django.db.models import Count
from .models import WebResource, Keyword, Message
import re
import simplejson as json
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from .serializers import MessageSerializer

from rest_framework.response import Response

from django.http import JsonResponse
from django.http import HttpResponse
import requests

globalChat = []

# RUN FROM http://127.0.0.1:3000

def index(request):
    #render
    return render(request, 'index.html')

def askQuestion(request):

    reso = parseText(request)
    chatLogTracker(reso, "query")

    #return render(request, 'index.html', {"itemList" : reso, "chatLog" : globalChat})
    return render(request, 'index.html', {"itemList": reso})

def parseText(request):
    chatLogTracker(request.POST.get('submitField'), "text")
    queryset = request.POST.get('submitField', '').split(" ")
    combinedQuery = WebResource.objects.none()

    #remove punctuation
    for i in range(len(queryset)):
        queryset[i] = re.sub(r'[^\w\s]', '', queryset[i])

    #getting all sites with associated keywords
    for query in queryset:
        f = Keyword.objects.filter(name=query)
        if f:
            a = WebResource.objects.filter(siteKeywords__in = f)
            combinedQuery = combinedQuery | a

    #get list of all queries and how many times they have a keyword
    updatedQuery = combinedQuery.values("siteName", "siteURL").annotate(Count("siteID")).order_by("siteID__count").distinct()

    #top 3 queries by keyword frequency
    updatedQuery = updatedQuery.reverse().order_by("siteID__count")[:3]

    #print(list(updatedQuery))
    listQuery = list(updatedQuery)

    singleMessage = Message(sender="bot", description=listQuery)#, myDescription=json.dumps(listQuery))
    singleMessage.save()

    #jsonDec = json.decoder.JSONDecoder()
    #myPythonList = jsonDec.decode(Message.myDescription)

    f = Message.objects.filter(sender="bot")
    print("maaaaaaa", f)

    return list(updatedQuery)

def apiAskQuestion(request):
    #request_json = json.loads(request.body)
    #print(request_json, " hi")

    f = Message.objects.all()
    print(f)

    serializer = MessageSerializer(f, many=True)
    print(serializer)
    return JsonResponse(serializer.data, safe=False)

    #return JsonResponse({"text": f})


def chatLogTracker(reso, type):
    if type == "text":
        globalChat.append(reso)
    if type == "query":
        for query in reso:
            text = (query['siteName'] + " " + query['siteURL'])
            globalChat.append(text)

    #if len(globalChat) > 9:
        #np.resize(globalChat,(0,9))
