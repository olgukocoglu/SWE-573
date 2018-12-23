from django.shortcuts import render
from django.http import JsonResponse
from .classes.twitterApi import TwitterAPI
from .classes.analysis import SentimentalAnalysis

def home(request):
    return render(request, 'home.html', {})

def results(request):
    if (request.method == 'GET'):
        error = 'You did not type a query. Please type a query in the homepage.'
        return render(request, 'results.html', {'error':error})
    
    query = request.POST['query']
    twitterAPI = TwitterAPI()
    sentimentalAnalysis = SentimentalAnalysis()

    searchedTweets = twitterAPI.getTweets(query)
    error = twitterAPI.checkTweetCount()
    data = sentimentalAnalysis.makeAnalysisOnArray(searchedTweets)
    percentages = sentimentalAnalysis.calculatePercentages()

    return render(request, 'results.html', {'query':query, 'data':data, 'percentages':percentages, 'error':error})