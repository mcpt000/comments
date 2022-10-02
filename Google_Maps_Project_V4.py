import json
import requests
import pandas as pd
from pandas import json_normalize

#API KEY
API_KEY = "AIzaSyDmS0vzyNoL3QqN-SKxw6322HV2HgzJeUA"

def search_my_place(place):
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
        'location' : place['location'],
        'radius' : place['radius'],
        'name' : place['name'],
        'key' : API_KEY
    }
    
    #Request
    response = requests.get(endpoint_url, params = params)
    
    #Results
    results = json.loads(response.content)
    
    return results


def nearby_places(place):
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
        'location' : place['location'],
        'radius' : place['radius'],
        'types' : place['types'],
        'key' : API_KEY
    }
    
    #Request
    response = requests.get(endpoint_url, params = params)
    
    #Results
    results = json.loads(response.content)
    
    return results
