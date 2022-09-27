import json
import requests
import pandas as pd
from pandas import json_normalize

def search_my_place(location, radius, name, key):
    """
    Function to search places nearvy given the location and radius using nearby_places from places API
    
    Inputs:
    -
    
    Outputs:
    -
    """
    
    #Endpoint
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    #Parameters
    params = {
        'location' : location,
        'radius' : radius,
        'name' : name,
        'key' : key
    }
    
    #Request
    response = requests.get(endpoint_url, params = params)
    
    #Results
    results = json.loads(response.content)
    
    return results


def nearby_places(location, radius, types, key):
    """
    Function to search places nearvy given the location and radius using nearby_places from places API
    
    Inputs:
    -
    
    Outputs:
    -
    """
    
    #Endpoint
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    #Parameters
    params = {
        'location' : location,
        'radius' : radius,
        'types' : types,
        'key' : key
    }
    
    #Request
    response = requests.get(endpoint_url, params = params)
    
    #Results
    results = json.loads(response.content)
    
    return results

#API KEY
API_KEY = "AIzaSyDmS0vzyNoL3QqN-SKxw6322HV2HgzJeUA"

#Query
name = "Chili\'s"

#Location
latitude = "21.039850900933683"
longitude = "-89.63091958246127"
location = f'{latitude}, {longitude}'
print(location)

#Radius
radius = "3"  #Please don't move the radius

#get the tags for our location and save them in 'types_my_place'
types_my_place = []
for result in my_data['results']:
    if result['name'] == name:
        types_my_place.append(result['types'])


#This tag is going to change by the user selection
tag = 'restaurant'

#API KEY
API_KEY = "AIzaSyDmS0vzyNoL3QqN-SKxw6322HV2HgzJeUA"
#Query
types = "restaurant"
#Location
latitude = "21.039850900933683"
longitude = "-89.63091958246127"
location = f'{latitude}, {longitude}'
#Radius
radius = "5000"



rival_data = nearby_places(location, radius, types, API_KEY)
#rival_data.keys()
#len(rival_data['results'])
#rival_data['results'][4]    #Galerías
riv_data = rival_data['results']
#len(riv_data)

df = json_normalize(riv_data)

#display datafram
#df

row_numbers = df[df['name'] == 'Chili\'s'].index
#print(row_numbers)

my_place = df.iloc[row_numbers]
#my_place


#types_my_place

#get the address of our location and save it in 'address_my_place'
for result in rival_data['results']:
    if result['name'] == name:
        address_my_place = result['vicinity']
        #print(address_my_place)


#get the rating of our location and save it in 'rate_my_place'
for result in rival_data['results']:
    if result['name'] == name:
        rate_my_place = result['rating']
        #print(rate_my_place)


'''
Get the cathegorical price range of our location and save it in 'price_leve_my_place' and rank it as:

0 Free
1 Inexpensive
2 Moderate
3 Expensive
4 Very Expensive
'''

for result in rival_data['results']:
    if result['name'] == name:
        price_level_my_place = result['price_level']
        #print(price_level_my_place)


## get the total number of people that rate the location
for result in rival_data['results']:
    if result['name'] == name:
        rate_total_my_place = result['user_ratings_total']
        #print(rate_total_my_place)


#get the latitude (lat_my_place) and longitude(lng_my_place) of our location and store them together in loc_my_place 
for result in rival_data['results']:
    if result['name'] == name:
        lat_my_place = result['geometry']['location']['lat']
        lng_my_place = result['geometry']['location']['lng']
        loc_my_place = (lat_my_place, lng_my_place)
        #print(loc_my_place)


#get the latitude and longitude of our competitors and store them together(as pairs) in the list "rival_lat_long"

rival_lat_long = []

for result in rival_data['results']:
    if result['name'] == name:
        continue
    else:       
        rival_lat_long.append((result['geometry']['location']['lat'], result['geometry']['location']['lng']))
        

#rival_lat_long
df_rival_lat_long = pd.DataFrame(rival_lat_long)
df_rival_lat_long.columns = ['lat', 'long']
#df_rival_lat_long


#get the individual rates from all extracted places and store them in all_rates(list)
all_rates = []
for result in rival_data['results']:
    rates = result['rating']
    all_rates.append(rates)
    
##all_rates

#sorting from highest to lowest all individual rates 
all_rates.sort(reverse=True)
#all_rates_result = len(all_rates)
#all_rates

#Ranking all rates and get ours in order to know the position over all others 
count = 1
for rate in all_rates:
    if rate == rate_my_place:
        position = count
        #print(count)
        break
    else:
        count += 1
#position

#Percentange of my rate location regarding the highest rated competitor

percentage_rating_my_place = ((max(all_rates) - rate_my_place) * 100) / (max(all_rates))
#percentage_rating_my_place


#get all locations that accomplish the input and store them in rival_names
rival_names = []
for result in rival_data['results']:
    for typs in result['types']:    
        if result['name'] == name:
            continue
        elif typs != tag:
            continue
        else:
            rival_names.append(result['name'])
#rival_names
#len(rival_names)


#Get all rates but ours
rival_rates = []
for result in rival_data['results']:
    if result['name'] == name:
        continue
    else:
        rival_rates.append(result['rating'])
#len(rival_rates)


#get the average rate of our competition
average_rate_rivals = round(sum(rival_rates) / len(rival_rates), 1)
#average_rate_rivals


#Get all comments but ours (and the average quantity of them)

rival_comments = []
for result in rival_data['results']:
    if result['name'] == name:
        continue
    else:
        rival_comments.append(result['user_ratings_total'])

average_comments_rivals = round(sum(rival_comments) / len(rival_comments))
#rival_comments

