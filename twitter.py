'''
search and store twitts related to Foursquare in the Chicago area

using twitter package to access Twitter's API
based on keyword (currently  4sq.com) and geo-location
code is based on examples from "Mining the Social Web" and :
https://github.com/ideoforms/python-twitter-examples/blob/master/twitter-search-geo.py
for definitions of the API, see:
https://dev.twitter.com/rest/reference/get/search/tweets

worth checking this:
https://github.com/jalbertbowden/foursquare-user-dataset
'''

import twitter
import json
import pandas as pd
import datetime

def oauth_login(consumer_key, consumer_secret, oauth_token, oauth_token_secret):
    '''
    given set of credentials, set up connection to Twitter's API

    '''

    auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret,
    consumer_key, consumer_secret)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


def search_by_location_and_word(twitter_api,latitude,longitude,max_range,keyword, num_results=100):
        '''
        returns tweets including keywotdby users located within the given radius of
        latitude/longitude


        inputs:
        twitter_api: Twitter class object
        latitude and longitude: geographical centre of search
        max_range: in KM, only include tweets in this range from center
        keyword: search keyword of tweets
        num_results: maximum number of results returned. To achieve it we needed to not exceed Twitter API rules...

        output: pandas dataframe of data from twitts, row per twitt
        '''

        result_count = 0
        last_id = None
        results_list = []
        while result_count <  num_results:
                # building the query based on keyword and location:
                query = twitter_api.search.tweets(q = keyword, geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), count = 100, max_id = last_id)


                for result in query["statuses"]:
                            # only process a result if it has a geolocation ("geo" not empty)
                            if result["geo"]:
                                    user = result["user"]["screen_name"]
                                    user_id = result["user"]["id_str"]
                                    text = result["text"].encode('ascii', 'replace')
                                    # need to convert from unicode to ascii
                                    #text = text.encode('ascii', 'replace')
                                    # couldn't find any 4sq ID of the location linked to the tweet...
                                    # but, some twitts have the location name stored:
                                    try:                                    
                                        location_name = result["entities"]["name"].encode('ascii', 'replace')
                                        location_screen_name = result["entities"]["screen_name"].encode('ascii', 'replace')
                                    except KeyError:
                                        location_name = "NOT FOUND"
                                        location_screen_name  = "NOT FOUND"
                                    # we can also try to collect the url to 4sq checkin:
                                    try:
                                        foursqr_url = result["entities"]["urls"][0]["expanded_url"].encode('ascii', 'replace') 
                                    except KeyError:
                                        foursqr_url = "NOT FOUND"
                                    
                                    g_lat = result["geo"]["coordinates"][0]
                                    g_long = result["geo"]["coordinates"][1]
                                    # additional data that might be worth collecting:
                                    user_location = result["user"]["location"].encode('ascii', 'replace') # to check that it is Chicago
                                    user_desc = result["user"]["description"].encode('ascii', 'replace') # if we want to analyze the users
                                    created_at = result["created_at"].encode('ascii', 'replace') # for time of checkin
                                    # store twitt data in a list object (new_twt)
                                    new_twt = [ user, user_id, text, location_name, location_screen_name,foursqr_url,
                                                g_lat, g_long, user_location, user_desc, created_at]
                                    # append new_twt to list of all results
                                    results_list.append(new_twt)
                                    result_count += 1
                            last_id = result["id"]

        return results_list


if __name__=='__main__':
    # first, setting twitter_api object your API credentials: (change to your  keys and secrets...)
    consumer_key = ""
    consumer_secret = ""
    oauth_token = ""
    oauth_token_secret = ""
    twitter_api = oauth_login(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    # next, setting the parameters for search:
    # read zip code data:
    zips = pd.read_csv("C:\\Projects\\MSCA_AYAR\\zips.csv")
    '''    
    # taking the latitude and longitude of the first zip code in our list as inputs for search:
    latitude , longitude = zips.ix[0,['latitude','longitude']]
    max_range = 50 # 50 km from center
    keyword = '"4sq.com"' # it seems like we need dobule quates '"..."' otherwise search returned empty
    
    # search API:
    twt_list = search_by_location_and_word(twitter_api,latitude,longitude,
                                           max_range,keyword, num_results=2)
    
    '''
    # converting list-of-lists to dataframe:
    col_names = [ "user", "user_id", "text", "location_name","location_screen_name",
                 "foursqr_url","g_lat", "g_long", "user_location", "user_desc", "created_at"]
    '''
    df = pd.DataFrame(twt_list, columns = col_names) 
    
    # looking at some of the data:    
    df.head()
    df.tail()
    # if we want to write to .csv file:
    df.to_csv("first_q_feb_29.csv") # will write in cwd if no path is given
    '''
    # searching all zipcodes:
    twt_per_zip = []
    for zip_number in xrange(zips.shape[0]):
        latitude , longitude = zips.ix[zip_number,['latitude','longitude']]
        twt_list = search_by_location_and_word(twitter_api,latitude,longitude,
                                           max_range,keyword, num_results=100)
        df = pd.DataFrame(twt_list, columns = col_names)
        df['Zip_searched'] = str(zips.ix[zip_number, 'zip_code'])
        twt_per_zip.append(df)
    
    all_zips_df = pd.concat(twt_per_zip, axis = 0)
    csv_name = str(datetime.datetime.now()).replace(" ", "_")[:16] + '.csv'
    all_zips_df.to_csv(csv_name)