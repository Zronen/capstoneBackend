import string

from django.shortcuts import render
from django.db.models import Count
from .models import WebResource, Keyword
import re

globalChat = []

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

    return list(updatedQuery)

def chatLogTracker(reso, type):
    if type == "text":
        globalChat.append(reso)
    if type == "query":
        for query in reso:
            text = (query['siteName'] + " " + query['siteURL'])
            globalChat.append(text)

    #if len(globalChat) > 9:
        #np.resize(globalChat,(0,9))
