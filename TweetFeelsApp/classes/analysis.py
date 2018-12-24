from textblob import TextBlob

class SentimentAnalysis:

    def MakeAnalysisOnArray(self, searchedTweets):
        self.data = [0, 0, 0]
        
        for tweet in searchedTweets:
            blob = TextBlob(tweet.full_text)
            polarity = blob.sentiment.polarity
            print(tweet.full_text, polarity)

            if polarity == 0:
                self.data[1] += 1
            elif polarity > 0:
                self.data[0] += 1
            elif polarity < 0:
                self.data[2] += 1
        
        return self.data
    
    def CalculatePercentages(self):
        self.percentages = []
        sumOfValues = sum(self.data)

        if (sumOfValues == 0):
            return self.percentages

        for i in range(len(self.data)):
            self.percentages.append(int(self.data[i] / sumOfValues * 100))
        
        return self.percentages