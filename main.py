# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import GetOldTweets3 as got

import tweepy
import snscrape.modules.twitter as sntwitter
import numpy
import csv
import twitterscraper
import datetime as dt

auth = tweepy.OAuthHandler("LbFtVrIhom3VvxKJvxZ7r7i7R", "ZEyjiU9tVnxhGPjcktdNR3MJPoZWVcB6DHB9CfoQAfSITa1Dqu")
auth.set_access_token("1321890546592501761-QHftta7lerBzMyeAQIRAVF9tgymEpP", "59guj1UkamBCqefaYoCVHCjdZQ9UNbl6JqtkN7Z0vzkP2")



class Tweet:
    def __init__(self,id,date,content):
        self.id = id
        self.date = date
        self.content = content

def countCountries(ids, countriesDict):
    api = tweepy.API(auth)
    tweets = api.statuses_lookup(ids)
    for tweet in tweets:
        #in some very rare cases, the tweet does not have a country entry
        if hasattr(tweet.place, 'country'):
            countryName = tweet.place.country
            if countryName in countriesDict:
                countriesDict[countryName] +=1
            else:
                countriesDict[countryName] = 1
    return countriesDict

def test():

    #query = twitterscraper.query_tweets('query', limit=None, poolsize=20, lang='')
    #list_of_tweets = twitterscraper.query_tweets("Trump OR Clinton", 10)

    #sntwitter.TwitterSearchScraper
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
            "#hurricane OR #sandy OR #hurricanesandy since:2012-10-22 until:2012-11-02" + """ near:"San Francisco" within:15mi""").get_items()):
        print(tweet.id)
        print(tweet.date)
        print(tweet.content)


def getEarliestTweet(hashtags, startDate, endDate, location):



    #build query
    counter = 0
    hashString=''
    for hashtag in hashtags:
        counter+=1
        hashString=hashString+'#'+hashtag
        if counter < len(hashtags):
            hashString+=" OR "
    #print(hashString)

    query = hashString + " since:" + startDate + " until:" + endDate+''' near:"''' + location+'''" within:15mi'''
    print(query)

    frequencycounter = 0

    ids = []
    results=[]
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
            query).get_items()):
        frequencycounter+=1
        results.append(Tweet(tweet.id,tweet.date,tweet.content))
        ids.append(tweet.id)
        #print(tweet.id)
        #print(tweet.date)
        #print(tweet.content+"\n")

    print(str(frequencycounter) + " tweets found")
    for i in reversed(results):
        print(i.date)
        print(i.id)
        print(i.content+"\n")
    return ids






def getTweets(keyword):
    tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama") \
        .setTopTweets(True) \
        .setMaxTweets(10)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
    print(tweet.text)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


#function to split a given list (list) into lists of length (length)
def splitList(list,length):
    splittedLists= []
    counter = 0
    tempList = []
    while counter<len(list):
        tempList.append(list[counter])
        counter+=1
        if len(tempList) == length or counter == len(list):
            splittedLists.append(tempList)
            tempList = []
    return splittedLists



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    ids = (getEarliestTweet(["hurricane","sandy","hurricanesandy"],"2012-10-22","2020-10-28","San Francisco"))
    #split array because tweepy.statuslookup only accepts 100 ids for each call
    #splits = numpy.array_split(ids, len(ids)/100)
    splits = splitList(ids,100)

    # pass empty array to start with
    countriesDict = {}
    #print(splits)

    #print(countCountries(splits[0],countriesDict))
    #print(countCountries(splits[1], countriesDict))
    #print(countCountries(splits[2], countriesDict))
    for subList in splits:
        #print(subList)
        countCountries(subList,countriesDict)


    print(countriesDict)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
