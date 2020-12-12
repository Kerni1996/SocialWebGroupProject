# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import GetOldTweets3 as got

import datetime
import tweepy
import snscrape.modules.twitter as sntwitter
import numpy
import csv
import twitterscraper
import datetime as dt

auth = tweepy.OAuthHandler("LbFtVrIhom3VvxKJvxZ7r7i7R", "ZEyjiU9tVnxhGPjcktdNR3MJPoZWVcB6DHB9CfoQAfSITa1Dqu")
auth.set_access_token("1321890546592501761-QHftta7lerBzMyeAQIRAVF9tgymEpP", "59guj1UkamBCqefaYoCVHCjdZQ9UNbl6JqtkN7Z0vzkP2")



class Tweet:
    def __init__(self,id,date,content,username):
        self.id = id
        self.date = date
        self.content = content
        self.username = username


    #define function to print tweet objects nicely
    def __str__(self):
        return 'Tweet(id=' + str(self.id) + ', date=' + str(self.date) + ', content='+ self.content+', username='+ self.username+')'

#takes list of twitter IDs as argument and returns a dictionary with the number of tweets in each country
def countCountries(ids):
    splittedList = splitList(ids,100)
    countriesDict = {}
    for list in splittedList:
        api = tweepy.API(auth)
        tweets = api.statuses_lookup(list)
        for tweet in tweets:

            #in some very rare cases, the tweet does not have a country entry
            if hasattr(tweet.place, 'country'):
                countryName = tweet.place.country
                if countryName in countriesDict:
                    countriesDict[countryName] +=1

                    #if country does not exist in dict create it with initial count value = 1
                else:
                    countriesDict[countryName] = 1
    return countriesDict



def getAuthorityData(startDate, endDate, user):
    query = "from:" + user + " since:" + startDate + " until:" + endDate
    #print (query)

    list = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
            query).get_items()):
        list.append(Tweet(tweet.id, tweet.date, tweet.content,tweet.username))
        #print(tweet.id)
    return list

def getFirstAppearance(keywords, startDate, endDate, location, printAllTweets):
    # build query
    counter = 0
    hashString = ''
    for keyword in keywords:
        counter += 1
        hashString = hashString + keyword
        if counter < len(keywords):
            hashString += " OR "
    # print(hashString)
    query = hashString + " since:" + startDate + " until:" + endDate
    if location is not None:
        query += ''' near:"''' + location + '''" within:30mi'''
    tweets = []


    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
            query).get_items()):
        t1 = Tweet(tweet.id,tweet.date,tweet.content,tweet.username)
        tweets.append(t1)
        if printAllTweets:
            print(t1)
        #frequencycounter+=1
        #results.append(Tweet(tweet.id,tweet.date,tweet.content))
        #id = tweet.id

    if len(tweets)==0:
        return "No tweets found between " + str(startDate) + " and "+ str(endDate)
    #return last element since it is the earliest
    return tweets[len(tweets)-1]

def getEarliestTweets(hashtags, startDate, endDate, location):
    #TODO: start ist immer das aktuelle Datum


    #convert strings to actual date elements
    start = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    end = datetime.datetime.strptime(endDate,"%Y-%m-%d")

    # build query
    counter = 0
    hashString = ''
    for hashtag in hashtags:
        counter += 1
        hashString = hashString + hashtag
        if counter < len(hashtags):
            hashString += " OR "
    # print(hashString)

    ids = []
    results = []

    dict = {}


    while (start<=end):



        query = hashString + " since:" + start.strftime("%Y-%m-%d") + " until:" + (start+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        if location is not None:
            query += ''' near:"''' + location+'''" within:50mi'''
        #print(query)

        frequencycounter = 0



        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
                query).get_items()):
            frequencycounter+=1
            results.append(Tweet(tweet.id,tweet.date,tweet.content,tweet.username))
            ids.append(tweet.id)
            #print(tweet.id)
            #print(tweet.date)
            #print(tweet.content+"\n")

        dict[start.strftime("%Y-%m-%d")]=frequencycounter
        start = start + datetime.timedelta(days=1)
        """for i in reversed(results):
            print(i.date)
            print(i.id)
            print(i.content+"\n")"""
    print(dict)
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
    #print(getAuthorityData("2020-10-11","2020-10-12","ORF"))
    #print (str(getFirstAppearance(["hurricane","sandy","hurricanesandy"],"2012-10-22","2020-10-28","San Francisco")) + " is the id of the first tweet in the given range at the given location with the given hastags")
    #ids = (getEarliestTweets(["hurricane","sandy","hurricanesandy"],"2012-10-22","2020-10-28","San Francisco"))
    #print(countCountries(ids))

    # hurricane sandy:
    #get first post at location with a radius of 30 miles
    print(getFirstAppearance(["#hurricanesandy","#sandy","#hurricane","#Sandy", "#HurricaneSandy","#RomneyStormTips","#FrankenStorm","#StaySafe","#ThanksSandy","#FuckYouSandy","#RedCross","#JerseyStrong","#RestoreTheShore","#SandyHelp", "sandy","hurricane","Sandy", "HurricaneSandy"],"2012-10-10","2012-10-30","Nicaragua",True))

    #get first post globaly
    print(getFirstAppearance(["#hurricanesandy","#sandy","#hurricane","#Sandy", "#HurricaneSandy","#RomneyStormTips","#FrankenStorm","#StaySafe","#ThanksSandy","#FuckYouSandy","#RedCross","#JerseyStrong","#RestoreTheShore","#SandyHelp"],"2012-10-20","2012-10-21",None,True))
    #we selected the tweet with the id: 259537544495112192 as initial tweet (relevant for later)



    #in order to get a comparable frequency we select 3 hashtags that are for us strongly related to the event and count the frequency of tweets for 24 hours. we cant avoid to count tweets that are not meant to be correlated to the incident
    ids = getEarliestTweets(["#hurricanesandy","#sandy","#hurricane"],"2012-10-28","2012-10-29","New York")

    #print(countCountries(ids))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
