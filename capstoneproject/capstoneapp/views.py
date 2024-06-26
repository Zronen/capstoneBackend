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
    #chatLogTracker(request.POST.get('submitField'), "text")
    #queryset = request.POST.get('submitField', '').split(" ")
    queryset = request.split(" ")
    print(queryset, " values")
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
    #listQuery = list(updatedQuery)
    listQuery = []

    if updatedQuery:
        for item in updatedQuery:
            listQuery.append(item["siteName"])
            listQuery.append(item["siteURL"])

        if len(listQuery) == 2:
            singleMessage = Message(sender="bot", description=listQuery, res1=listQuery[0], link1=listQuery[1])#, myDescription=json.dumps(listQuery))
        if len(listQuery) == 4:
            singleMessage = Message(sender="bot", description=listQuery, res1=listQuery[0], link1=listQuery[1], res2=listQuery[2], link2=listQuery[3])  # , myDescription=json.dumps(listQuery))
        if len(listQuery) == 6:
            singleMessage = Message(sender="bot", description=listQuery, res1=listQuery[0], link1=listQuery[1], res2=listQuery[2], link2=listQuery[3], res3=listQuery[4], link3=listQuery[5])  # , myDescription=json.dumps(listQuery))

        singleMessage.save()
        return True

    #jsonDec = json.decoder.JSONDecoder()
    #myPythonList = jsonDec.decode(Message.myDescription)

    f = Message.objects.filter(sender="bot")
    #print("maaaaaaa", f)

    return False
    #return list(updatedQuery)

@csrf_exempt
def apiAskQuestion(request):
    #return back the message after str storing 1 in the database

    request_json = json.loads(request.body)
    #print(request_json, " hi")

    singleMessage = Message(sender="user", description=request_json["description"])  # , myDescription=json.dumps(listQuery))
    singleMessage.save()
    #print(request_json["description"])

    rText = request_json["description"]

    if parseText(rText) == False:
        rText = re.sub(r'[^\w\s]', '',rText)
        rText = rText.lower()
        if rText == "reset":
            resetMessages()
        elif rText == "hi" or rText == "hello":
            singleMessage3 = Message(sender="bot", description="Hello! Please enter a query so I can help you find what you're looking for.")
            singleMessage3.save()
        else:
            singleMessage2 = Message(sender="bot", description="Sorry, I couldn't find a recource based on your query, please try again.")
            singleMessage2.save()

    f = Message.objects.filter(description = request_json, sender="user")
    f.distinct()
    #print(f)

    serializer = MessageSerializer(f, many=True)
    print(serializer)
    return JsonResponse(serializer.data, safe=False)

    #return JsonResponse({"text": f})

def resetMessages():
    allMessages = Message.objects.all()
    allMessages.delete()
    singleMessage = Message(sender="bot", description="Hello, I'm NORA! I'm an application that functions a little like google, and can help you find resources relating to navigating online risks as a journalist.")  # , myDescription=json.dumps(listQuery))
    singleMessage.save()
    singleMessage2 = Message(sender="bot",description="Make sure to keep your queries straightforward, this will help me direct you to what you're looking for better. If the resources I provide aren't what you're trying to find, feel free to browse the app and look at all our resources there!")  # , myDescription=json.dumps(listQuery))
    singleMessage2.save()
    singleMessage3 = Message(sender="bot", description="Here are some sample questions a user can ask: ")
    singleMessage3.save()
    singleMessage4 = Message(sender="user", description="What steps can I take to make sure my social media accounts are secure?")
    singleMessage4.save()
    singleMessage5 = Message(sender="user", description="How can I protect my privacy and prevent myself from getting doxed?")
    singleMessage5.save()
    singleMessage6 = Message(sender="user", description="What can I do if I'm getting online harassment? What steps should I take?")
    singleMessage6.save()

def apiSendData(request):
    f = Message.objects.all()
    #print(f)

    serializer = MessageSerializer(f, many=True)
    return JsonResponse(serializer.data, safe=False)

def chatLogTracker(reso, type):
    if type == "text":
        globalChat.append(reso)
    if type == "query":
        for query in reso:
            text = (query['siteName'] + " " + query['siteURL'])
            globalChat.append(text)

    #if len(globalChat) > 9:
        #np.resize(globalChat,(0,9))
