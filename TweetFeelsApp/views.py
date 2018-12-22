from django.shortcuts import render
from django.http import JsonResponse
from textblob import TextBlob
import tweepy
import os

def home(request):
    return render(request, 'home.html', {})

def results(request):
    accountName = request.POST['accountName']

    consumerKey = os.environ['consumerKey']
    consumerSecret = os.environ['consumerSecret']
    accessKey = os.environ['accessKey']
    accessSecret = os.environ['accessSecret']

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessKey, accessSecret)
    api = tweepy.API(auth)

    searchedTweets = []
    lastId = -1
    maxTweets = 1000
    data = [0, 0, 0]

    while len(searchedTweets) < maxTweets:
        count = maxTweets - len(searchedTweets)
        try:
            newTweets = api.search(q=accountName, count=count, max_id=str(lastId - 1))
            if not newTweets:
                break
            searchedTweets.extend(newTweets)
            lastId = newTweets[-1].id
        except tweepy.TweepError as e:
            break
    
    for tweet in searchedTweets:
        blob = TextBlob(tweet.text)
        polarity = blob.sentiment.polarity
        print(tweet.text, polarity)

        if polarity == 0:
            data[1] += 1
        elif polarity > 0:
            data[0] += 1
        elif polarity < 0:
            data[2] += 1

    return render(request, 'results.html', {'accountName':accountName, 'data':data})