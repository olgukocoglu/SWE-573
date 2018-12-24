from django.test import TestCase
from .classes.report import AnalysisReport
from .classes.twitterApi import TwitterAPI
from .classes.analysis import SentimentAnalysis

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
    sentimentAnalysis = SentimentAnalysis()
    analysisReport = AnalysisReport()
    
    def testTwitterAPIInstance(self):
        self.assertTrue(isinstance(self.twitterAPI, TwitterAPI))

    def testGetTweetsCorrectly(self):
        tweets = self.twitterAPI.GetTweets(self.testQuery)
        self.assertEquals(len(tweets), 10)

        for tweet in tweets:
            self.assertTrue(self.testQuery in tweet.full_text)
    
    def testTweetCountDoesNotSatisfyMinimumTweetCount(self):
        error = self.twitterAPI.CheckTweetCount()
        self.assertEquals(error, "There are not enough tweets to get accurate results from the analysis for this query.")

    def testTweetCountSatisfiesMinimumTweetCount(self):
        self.twitterAPI.minimumTweetCount = 10
        error = self.twitterAPI.CheckTweetCount()
        self.assertEquals(error, "")

    def testSentimentAnalysisInstance(self):
        self.assertTrue(isinstance(self.sentimentAnalysis, SentimentAnalysis))

    def testAnalysisResults(self):
        analysisResults = self.sentimentAnalysis.MakeAnalysisOnArray(self.testTweetArray)
        self.assertEquals(analysisResults[0], self.testNumOfGoodTweets)
        self.assertEquals(analysisResults[1], self.testNumOfNeutralTweets)
        self.assertEquals(analysisResults[2], self.testNumOfBadTweets)

    def testPercentageCalculation(self):
        sumOfValues = self.testNumOfGoodTweets + self.testNumOfNeutralTweets + self.testNumOfBadTweets
        results = self.sentimentAnalysis.CalculatePercentages()

        if (sumOfValues == 0):
            self.assertEquals(results, [])
            return

        self.assertEquals(results[0], int(self.testNumOfGoodTweets / sumOfValues * 100))
        self.assertEquals(results[1], int(self.testNumOfNeutralTweets / sumOfValues * 100))
        self.assertEquals(results[2], int(self.testNumOfBadTweets / sumOfValues * 100))
    
    def testPercentageCalculationIfNoValues(self):
        tempData = self.sentimentAnalysis.data
        self.sentimentAnalysis.data = []

        results = self.sentimentAnalysis.CalculatePercentages()
        self.assertEquals(results, [])

        self.sentimentAnalysis.data = tempData

    def testAnalysisReportInstance(self):
        self.assertTrue(isinstance(self.analysisReport, AnalysisReport))

    def testAnalysisReportCorrectness(self):
        error = "There are not enough tweets to get accurate results from the analysis for this query."
        self.analysisReport.CreateReport(self.testQuery)
        self.assertEquals(self.analysisReport.query, self.testQuery)
        self.assertEquals(self.analysisReport.error, error)
        self.assertEquals(self.analysisReport.data,[0,10,0])
        self.assertEquals(self.analysisReport.percentages,[0,100,0])