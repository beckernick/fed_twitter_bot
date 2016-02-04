# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 20:23:52 2016

@author: nickbecker
"""

# Twitter Bot that tweets the most recent Federal Reserve Economic Discussion Series Working Paper

import tweepy

class TwitterAPI:
    def __init__(self):
        consumer_key = ''
        consumer_secret = ''
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = ''
        access_token_secret = ''
        auth.set_access_token(access_token, access_token_secret)
        
        self.api = tweepy.API(auth)
    
    def tweet(self, message):
        self.api.update_status(status = message)

    def search_tweets(self, string, count = 15):
        tweet_list = self.api.search(string, count)
        return tweet_list

    def get_last_tweet(self):
        tweet = self.api.user_timeline(id = self.api, count = 1)[0]
        return tweet.text
        


from bs4 import BeautifulSoup
import requests
import re

html_tags_re = re.compile(r'<[^>]+>')
def remove_html_tags(text):
    return html_tags_re.sub('', text)


# Get the latest FRB Working Papers List
x = requests.get('http://www.federalreserve.gov/econresdata/feds/2016/index.htm')
papers_soup = BeautifulSoup(x.text)

working_paper_numbers = [remove_html_tags(str(a)).strip() for a in papers_soup.findAll(style="font-weight:normal; font-size:.875em; line-height:1em;")]
papers_list = [str(a) for a in papers_soup.findAll("h3") if "href" in str(a)]
papers_titles = [remove_html_tags(paper).strip() for paper in papers_list]

paper_links = []
for a in papers_list:
    if "files/" in a:    
        start = a.find("/files/")
        end = a.find("pdf") + 3
        full_link = "www.federalreserve.gov/econresdata/feds/2016" + a[start:end]
        paper_links.append(full_link)

papers_dictionary = {z[0]: list(z[1:]) for z in zip(working_paper_numbers, papers_titles, paper_links)}






if __name__ == "__main__":
    twitter = TwitterAPI()
    most_recent_paper = twitter.get_last_tweet().split(":")[0]
    #print most_recent_paper
    if most_recent_paper != "New Working Paper " + working_paper_numbers[0]:
        twitter.tweet("New Working Paper " + working_paper_numbers[0] + ": " + paper_links[0])




