from django.shortcuts import render
import tweepy

def home(request):
    return render(request, 'home.html', {})

def results(request):
    accountName = request.POST['accountName']

    consumerKey = '5KEHxKw8MNAUi7tLG0wzcGBzn'
    consumerSecret = '2bbOhPU202QmzwWIoF5RaAlyhskK5jmMXr6Acsa2lbd4VrGVz6'
    accessKey = 	'2887799968-RwINMC25oQ2a888BNdgZZAgQKPowo68BfIstq7i'
    accessSecret = 'FXJFIcTbSRLdb3aLPWpFDKI5nHbETHvYyQimZXvs1FHfZ'

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessKey, accessSecret)
    api = tweepy.API(auth)

    searchedTweets = []
    lastId = -1
    maxTweets = 1000

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

    print(len(searchedTweets))

    return render(request, 'results.html', {'accountName':accountName})