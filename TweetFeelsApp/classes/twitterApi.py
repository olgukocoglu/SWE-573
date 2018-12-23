import tweepy
import os

class TwitterAPI:
    searchedTweets = []
    minimumTweetCount = 500
    maxTweets = 1000

    def getTweets(self, query):
        consumerKey = os.environ['consumerKey']
        consumerSecret = os.environ['consumerSecret']
        accessKey = os.environ['accessKey']
        accessSecret = os.environ['accessSecret']

        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessKey, accessSecret)
        api = tweepy.API(auth)

        searchedTweets = []
        lastId = -1

        while len(searchedTweets) < self.maxTweets:
            count = self.maxTweets - len(searchedTweets)
            try:
                newTweets = api.search(q=query, count=count, tweet_mode="extended", max_id=str(lastId - 1))
                if not newTweets:
                    break
                searchedTweets.extend(newTweets)
                lastId = newTweets[-1].id
            except tweepy.TweepError as e:
                break
                
        self.searchedTweets = searchedTweets
        for tweet in searchedTweets:
            print(tweet.full_text)
        return searchedTweets
    
    def checkTweetCount(self):
        if (len(self.searchedTweets) < self.minimumTweetCount):
            return "There are not enough tweets to get accurate results from the analysis for this query."
        else:
            return ""