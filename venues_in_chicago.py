# -*- coding: utf-8 -*-
"""
checking how many venues are in Chicago

note that it is is only an estimate and probably an under estimate, 
since we are only counting if in the "box" created by the max/min of the location of 
the zip codes... 

Created on Mon Feb 29 20:27:28 2016

@author: yuval
"""

import pandas as pd

# reading venues data set:
venues =  pd.read_csv('venues.dat', sep='|', header=None, skiprows=2)
venues.columns = ["id", "latitude", "longitude"]
venues.shape
venues.dtypes

zips = pd.read_csv("C:\\Projects\\MSCA_AYAR\\zips.csv")
zips.head()

min_lat = min(zips.latitude)
max_lat = max(zips.latitude)
min_lon = min(zips.longitude)
max_lon = max(zips.longitude)

def in_chicago(row):
    '''
    return 1 if location is in the Chicago "box"
    '''    
    try:
        lat = float(row[0])
        lon = float(row[1])
    except ValueError:
        return 0
    if lat >= min_lat and lat <= max_lat and lon >= min_lon and lon <= max_lon: 
        return 1
    else:
        return 0
        
in_chicago([42,-87.7]) # checking function
# in_chicago = 1 if in chicago, 0 otherwise:
venues['in_chicago'] = venues[['latitude','longitude']].apply(in_chicago , axis = 1)
# number of venues in chicago, and % of all venues:
sum(venues.in_chicago)
sum(venues.in_chicago) / float(len(venues.in_chicago))

# ids of venues in chicago:
only_chicago_venues = venues[venues.in_chicago ==1]
only_chicago_venues.id

# reading checkins data set:
checkins =  pd.read_csv('checkins.dat', sep='|', header=None, skiprows=2)
checkins.columns = ["id","user_id" , "venue_id", "latitude", "longitude","created_at"]
checkins.shape

### trying to convert both IDs columns to string
# first try:
only_chicago_venues['id_str'] = only_chicago_venues['id'].astype('str')#.values
checkins['venue_id_str'] = checkins['venue_id'].map('{:.0f}'.format)
#checkins['venue_id'] = checkins['venue_id'].astype(basestring)
match = pd.merge(only_chicago_venues, checkins, left_on='id_str', right_on='venue_id_str')
match.shape

# second try:
def clean_and_str(x):
    try:
        x = str(int(x))
        x = x.strip()
    except ValueError:
        x = x
    return x
    
only_chicago_venues['id_str'] = only_chicago_venues['id'].apply(clean_and_str)
checkins['venue_id_str'] = checkins['venue_id'].apply(clean_and_str)

match = pd.merge(only_chicago_venues, checkins, left_on='id_str', right_on='venue_id_str')
match.shape


