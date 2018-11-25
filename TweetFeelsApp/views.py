from django.shortcuts import render
import tweepy

def home(request):
    return render(request, 'home.html', {})

def results(request):
    accountName = request.POST['accountName']

    return render(request, 'results.html', {'accountName':accountName})