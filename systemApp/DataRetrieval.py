import pandas as pd
import numpy as np
import tweepy
import requests
from bs4 import BeautifulSoup
import regex as re
from datetime import datetime
from . import TwitterAuthenticator as ta
from . import CleanData as clean
#import spacy

import datetime

class DataRetrieval():
    def Tweets(self, text_query):
        tokens = [
        ['1543340234-DiumxFX5EPidgouxEEcwgPVl6IyqmoGm9RdetMW', 'RlWtOZYEGh6KfZOtiMlTENlnYc0T8JV3mjqxuiYlKcaHp', 'N1YeJ8GvhC1UIGCMvv4o4lN0L', '4JDWwTSbqrof97twCycZbP8lWVmzi9SQjVnuMEO5ksz54zPy4s'],
        ['8PySM1LgDueYnaFW51xt3gOfW', 'e6mky5E83sZV9uignGOUBK1GB2b9kY2yEtBhabRPjyHOnnTDju', '2729534668-S7y1vHHCSiiaSxjqzHspTNfTPu4bvJjal2gBbtS', 'Pkpqy6jBAsB13ZONusLpzbAwDFNX6SPPfFt0oBxVkdOln'],
        ['1186930861905731584-ifmlTFCRCm7uDl7o1asu84e3oZDbEh', 'LJUSI0zktLSWY2DKkoeR5Wq0D8q6AJFt4hZ3dbovRrnTi', 'OQtphgYvJ6KB9DtqswmFjFYtR', 'FgMenMABWeJL3NKvYzkWHx9QDdCcVJr4TaKRZBNGrtz1kr6qlH']
            ]
        flag = 0

        for i, token in enumerate(tokens):
        #Means that we got the 1000 tweets successfuly
            if flag==1:
                break
            search_filter =  text_query + " -filter:retweets"
            tweet_details = []
            ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET_KEY = tokens[i]
            auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            tweets = tweepy.Cursor(api.search, q = search_filter, lang = 'en', tweet_mode = "extended").items(1000)
            while True:
                try:
                    tweet = tweets.next()
                    print(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET_KEY)
                    tweet_details.append([tweet.created_at, tweet.full_text, tweet.user.screen_name, tweet.user.location])
                except tweepy.TweepError:
                    print('Rate Limit Exceeded')
                    break
                except StopIteration:
                    flag = 1
                    break

            
            tweet_df = pd.DataFrame(data = tweet_details, columns=['date', 'review', 'name', 'location'])
            tweet_df['date'] = pd.to_datetime(tweet_df['date']).dt.date

        return tweet_df

    def amazon_reviews(self , text_query):
        headers = {
            'authority': 'scrapeme.live',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        search_query = text_query
        search = search_query.split(' ')
        last_search = '+'.join(search)
        last = '-'.join(search)

        #print(last_search)
        #print(last)
        ###----------------------------------Get All Products in page--------------------------###
        def get_soup(url):
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')
            return soup

        query = 'https://www.amazon.com/s?k=' + last_search
        soup = get_soup(query)
        print(soup)
        search_results = soup.find_all('div', {'data-component-type': 's-search-result'})
        links = []

        for search in search_results:
            low = search.find('span', {'class': 'a-text-normal'}).text.lower()
            if search_query.lower() in low:
                links.append(search.find('a')['href'])

        links = ["https://www.amazon.com" + link for link in links]

        r = re.compile(r'^(?!https://www.amazon.com/gp)')
        links = list(filter(r.match, links))
        # links = links.remove(remove)

        print(links)
        ###-------------------------Get All Reviews From Each Page of Each Product------------------------###
        reviewlist = []

        def get_reviews(soup):
            flag = 0
            reviews = soup.find_all('div', {'data-hook': 'review'})
            for item in reviews:
                try:
                    review = {
                        'name': item.find('div', {'class': 'a-profile-content'}).text,
                        'review': item.find('span', {'data-hook': 'review-body'}).text.rstrip('\n'),
                        'date': item.find('span', {'data-hook': 'review-date'}).text.strip(),
                    }
                    #Control the empty pages
                    if (len(review) == 0):
                        flag = 0
                        break
                    else:
                        flag = 1
                        reviewlist.append(review)
                except:
                    pass
            return flag

        page_count = 100

        flag_stop = True
        for link in links:
            # Check if we reached our 1,000 review and we want to stop
            if (flag_stop == False):
                break
            print('Now we are in link: ' + link)
            name = re.search(r'.com/(.+)/dp', link)
            id = re.search(r'/dp/(.+)/r', link)
            for x in range(1, page_count):
                review_link = 'https://www.amazon.com/' + name.group(1) + '/product-reviews/' + id.group(
                    1) + '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(x)
                soup = get_soup(review_link)
                print(f'Getting page: {x}')
                x = get_reviews(soup)
                # Check if we reached our 1,000 review and we want to stop
                if len(reviewlist) >= 1000:
                    flag_stop = False
                    break
                if not soup.find('li', {'class': 'a-disabled a-last'}) and not x == 0:
                    pass
                else:
                    break
        #Get the Dataframe of data
        df = pd.DataFrame(reviewlist)

        df['date'] = df['date'].str.extract(r'on (\w+ \d+, \d+)')
        df['date'] = pd.to_datetime(df['date']).dt.date

        return df

    def get_all_reviews(self, text_query):
        tweets = self.Tweets(text_query)
        amazon = self.amazon_reviews(text_query)
        tweets['platform'] = 'twitter'
        amazon['platform'] = 'amazon'
        all_reviews = amazon.append(tweets)
        # all_reviews = tweets.append([])
        all_reviews["review"] = all_reviews["review"].map(clean.CleanData.remove_urls)
        all_reviews["review"] = all_reviews["review"].map(clean.CleanData.clean_html)
        all_reviews["review"] = all_reviews["review"].map(clean.CleanData.clean_mentions_and_endline)

        return all_reviews


