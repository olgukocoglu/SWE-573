from django.shortcuts import render
from django.http import JsonResponse
from .twitterApi import TwitterAPI
from .analysis import SentimentAnalysis

class AnalysisReport():

    def CreateReport(self,query):
        twitterAPI = TwitterAPI()
        sentimentAnalysis = SentimentAnalysis()

        self.query = query
        self.searchedTweets = twitterAPI.GetTweets(query)
        self.error = twitterAPI.CheckTweetCount()
        self.data = sentimentAnalysis.MakeAnalysisOnArray(self.searchedTweets)
        self.positiveTweets = sentimentAnalysis.positiveTweets
        self.neutralTweets = sentimentAnalysis.neutralTweets
        self.negativeTweets = sentimentAnalysis.negativeTweets
        self.percentages = sentimentAnalysis.CalculatePercentages()