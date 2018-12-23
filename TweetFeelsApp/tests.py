from django.test import TestCase
from .classes.twitterApi import TwitterAPI
from .classes.analysis import SentimentalAnalysis

class tweetModel:
    full_text = ""
    def __init__(self, tweetText):
        self.full_text = tweetText

class TweetFeelsTest(TestCase):
    testQuery = "dksjfdakjskladjfkjldsfhkjhdfskjhadfsklafdk"
    testTweetArray = [tweetModel("good"), tweetModel("good"), tweetModel("good"), tweetModel("neutral"), tweetModel("neutral"), tweetModel("bad")]
    testNumOfGoodTweets = 3
    testNumOfNeutralTweets = 2
    testNumOfBadTweets = 1
    twitterAPI = TwitterAPI()
    sentimentalAnalysis = SentimentalAnalysis()
    
    def testTwitterAPIInstance(self):
        self.assertTrue(isinstance(self.twitterAPI, TwitterAPI))

    def testGetTweetsCorrectly(self):
        tweets = self.twitterAPI.getTweets(self.testQuery)
        self.assertEquals(len(tweets), 10)

        for tweet in tweets:
            self.assertTrue(self.testQuery in tweet.full_text)
    
    def testTweetCountDoesNotSatisfyMinimumTweetCount(self):
        error = self.twitterAPI.checkTweetCount()
        self.assertEquals(error, "There are not enough tweets to get accurate results from the analysis for this query.")

    def testTweetCountSatisfiesMinimumTweetCount(self):
        self.twitterAPI.minimumTweetCount = 10
        error = self.twitterAPI.checkTweetCount()
        self.assertEquals(error, "")

    def testSentimentalAnalysisInstance(self):
        self.assertTrue(isinstance(self.sentimentalAnalysis, SentimentalAnalysis))

    def testAnalysisResults(self):
        analysisResults = self.sentimentalAnalysis.makeAnalysisOnArray(self.testTweetArray)
        self.assertEquals(analysisResults[0], self.testNumOfGoodTweets)
        self.assertEquals(analysisResults[1], self.testNumOfNeutralTweets)
        self.assertEquals(analysisResults[2], self.testNumOfBadTweets)

    def testPercentageCalculation(self):
        sumOfValues = self.testNumOfGoodTweets + self.testNumOfNeutralTweets + self.testNumOfBadTweets
        results = self.sentimentalAnalysis.calculatePercentages()

        if (sumOfValues == 0):
            self.assertEquals(results, [])
            return

        self.assertEquals(results[0], int(self.testNumOfGoodTweets / sumOfValues * 100))
        self.assertEquals(results[1], int(self.testNumOfNeutralTweets / sumOfValues * 100))
        self.assertEquals(results[2], int(self.testNumOfBadTweets / sumOfValues * 100))
    
    def testPercentageCalculationIfNoValues(self):
        tempData = self.sentimentalAnalysis.data
        self.sentimentalAnalysis.data = []

        results = self.sentimentalAnalysis.calculatePercentages()
        self.assertEquals(results, [])

        self.sentimentalAnalysis.data = tempData