from textblob import TextBlob

class SentimentalAnalysis:
    data = [0, 0, 0]

    def makeAnalysisOnArray(self, searchedTweets):
        for tweet in searchedTweets:
            blob = TextBlob(tweet.text)
            polarity = blob.sentiment.polarity
            print(tweet.text, polarity)

            if polarity == 0:
                self.data[1] += 1
            elif polarity > 0:
                self.data[0] += 1
            elif polarity < 0:
                self.data[2] += 1
        
        return self.data
    
    def calculatePercentages(self):
        percentages = []
        sumOfValues = sum(self.data)

        if (sumOfValues == 0):
            return percentages

        for i in range(len(self.data)):
            percentages.append(int(self.data[i] / sumOfValues * 100))
        
        return percentages