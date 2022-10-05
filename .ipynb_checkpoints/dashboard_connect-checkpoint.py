#import libraries

import streamlit as st
import pandas as pd
import numpy as np
import requests
import pydeck as pdk
from Google_Maps_Project_V4 import search_my_place, nearby_places
from pandas import json_normalize
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64
import numpy as np
from tempfile import NamedTemporaryFile



st.set_page_config(page_title = "Google Maps Dashboard",
    page_icon = "🗺️",
    layout = "wide")

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

#page 1
def check(business_name='', latitude='', longitude='', radius=''):
    #radius = radius.split(' ')[0]
    if business_name == "" or latitude == "" or longitude == "" or radius == "":
        return "Please fill in all the fields"
    #check if the radius is a number
    elif radius.isdigit() == False or int(radius) == 0 or int(radius)< 0:
        return "Please enter a valid radius"
    #check if the latitude and longitude are in the correct range
    elif float(latitude) < -90 or float(latitude) > 90 or float(longitude) < -180 or float(longitude) > 180:
        return "Please enter a valid latitude and longitude"
    #check if a selection has been made
    #elif competitor_type == "Select your competitor type":
    #    st.warning("Please select a competitor type")
    else:
        return True

def requirements():
    col1, col2, col3 = st.columns(3)
    with col1:
        pass
    with col2:
        st.image('logo1.png')
    with col3:
        pass
    st.markdown("<h1 style='text-align: center;'>Google Maps Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'> Get insights about your business & competitors </h3>", unsafe_allow_html=True)
    
    col1,col2,col3 = st.columns([1,2,1])
    types = []
    with col1:
        pass
    with col2:
        st.markdown("<h6 style='text-align: center;'> GUPY MAPS is a web app that will help you to know the position of your business in the digital market, know your metrics and those of the competition with just a few steps.  </h6>", unsafe_allow_html=True)
        business_name = st.text_input("Enter your business name")
        latitude = st.text_input("Enter your business latitude")
        longitude = st.text_input("Enter your business longitude")
        #modifie according to the preprocessing
        #competitor_type = st.selectbox("Select your competitor type", ["Restaurants", "Hotels", "Shopping", "Entertainment", "Other"])
        radius = st.text_input("Enter your business radius in meters",'10000 m').replace(' m','')
        
        
        place = {
            "name": business_name,
            "location":f'{latitude}, {longitude}',
            #"types": competitor_type,
            "radius": radius
        }
        st.markdown("*If you don't know the latitude and longitude of your business, click [here](https://www.google.com/maps).*")
        validation = check(business_name, latitude, longitude, radius)
        if validation == True and len(types) == 0:
            data_nearby_places = search_my_place(place)
            place['general_data'] = data_nearby_places['results'][0]
            types = data_nearby_places['results'][0]['types']
        else:
            st.warning(validation)
        if validation == True and len(types) > 0:
            types_to_explore = st.multiselect("Select the types of places you want to compare", types, key='types')
            place['place_to_explore'] = types_to_explore
            button_submit = st.button("Submit", key='submit')

            if types_to_explore and validation == True and button_submit:
                place['nearby_places'] = nearby_places(place)['results']
                st.write(st.session_state)
                #st.write(place)
                
    with col3:
        pass

    
    if 'submit' in st.session_state and st.session_state['submit'] and 'nearby_places' in place.keys():
        dashboard(place)
        #st.write(place)
    # if types_to_explore and check(business_name, latitude, longitude, radius) and st.button("Submit"):
    #     dashboard(place)r
    
 #name = "Chili's"
 ##
 ###Location
 #latitude = "21.039850900933683"
 #longitude = "-89.63091958246127"



def dashboard(place):
    business_name = place['name']
    radius = place['radius']
    latitude, longitude = place['location'].split(', ')
    #competitor_type = place['place_to_explore']
    #radius = 5
    #two columns
    col1, col2 = st.columns([1,9])

    with col1:
        #image has to be the icon in the API
        nombre_local_imagen = "icon.png" # El nombre con el que queremos guardarla
        imagen = requests.get('https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png').content
        with open(nombre_local_imagen, 'wb') as handler:
            handler.write(imagen)

        #imagen = requests.get('https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png').content
        
        #rst.markdown("""<img src="icon.png" style="width:50%;">""", unsafe_allow_html=True)
        st.image('icon.png')

    with col2:
        st.markdown("# {}" .format(business_name))

    # print icon according to the points
    # poits from the API
    try:
        points = place['general_data']['rating']
    except:
        points = 0

    if float(points) >= 0 and float(points) <= 1.5:
        st.markdown("## ⭐️")
    elif float(points) > 1.5 and float(points) <= 2.5:
        st.markdown("## ⭐️ ⭐️")
    elif float(points) > 2.5 and float(points) <= 3.5:
        st.markdown("## ⭐️ ⭐️ ⭐️")
    elif float(points) > 3.5 and float(points) <= 4.5:
        st.markdown("## ⭐️ ⭐️ ⭐️ ⭐️")
    elif float(points) > 4.5 and float(points) <= 5:
        st.markdown("## ⭐️ ⭐️ ⭐️ ⭐️ ⭐️")
    
    col3, col4 = st.columns(2)

    with col3:
        #rating from the API
        try:
            rating = place['general_data']['rating']
        except:
            rating < 0

        #amount of reviews from the API
        try:
            reviews = place['general_data']['user_ratings_total']
        except:
            reviews < 0
        
        st.markdown("### Your rating is {}/5 based on {} reviews" .format(rating, reviews))

        #Categorical price level from the API
        try:
            price_level = place['general_data']['price_level']
        except:
            price_level < 0
        
        if price_level == 0:
            price_level = "Free 🥳"
        elif price_level == 1:
            price_level = "Inexpensive 💵"
        elif price_level == 2:
            price_level = "Moderate 💵"
        elif price_level == 3:
            price_level = "Expensive 💸"
        elif price_level == 4:
            price_level = "Very Expensive 💸"
        
        st.markdown("### The pricing here is {}" .format(price_level))
        

    with col4:
        #type of business
        #type of business from the API
        type_of_business = place['general_data']['types']
        st.markdown("### Type of Business")
        for i in type_of_business:
            st.markdown("- {}" .format(i))
    
    #business address
    #business address from the API
    aux = place['general_data']
    try:
        aux = aux['vicinity']
    except:
        aux = 'No address found'
    address = aux#"Calle de la Cruz, 1, 28012 Madrid, Spain"
    st.markdown("<h4  style='color :darkcyan;'> Address: {} </h4r>".format(address), unsafe_allow_html=True)
 

    #map with the business location of competitors from the API
    df = json_normalize(place['nearby_places'])
    #only the columns we need lat and lng
    df = df[['geometry.location.lat', 'geometry.location.lng']]
    #rename the columns
    df = df.rename(columns={'geometry.location.lat': 'lat', 'geometry.location.lng': 'lon'})
   

    # #map with random locations
    # df = pd.DataFrame(np.random.randn(100, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])

    #add the business location to the dataframe
    df = df.append({'lat': float(latitude), 'lon': float(longitude)}, ignore_index=True)

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=float(latitude),
            longitude=float(longitude),
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[lon, lat]',
                get_color='[221, 163, 178, 160]',
                get_radius=200,
            ),
            #add the business location to the map in a different color
            pdk.Layer(
                'ScatterplotLayer',
                data=df.tail(1),
                get_position='[lon, lat]',
                get_color='[69, 133, 145, 160]',
                get_radius=200,
            )
        ],
    ))

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("<h3 align='center' style='color :darkcyan;'> Your Business </h3>", unsafe_allow_html=True)

    with col6:  
        st.markdown("<h3 align='center' style='color :pink;'r> Competitors </h3>", unsafe_allow_html=True)
    
    col7, col8, col9, col10 = st.columns(4)
    with col7:
        your_reviews = place['general_data']['user_ratings_total']
        st.markdown('''
        <div class="container">
        ''', unsafe_allow_html=True)
        st.metric("Reviews", "{}" .format(your_reviews))
    
    with col8:
        pass

    with col9:
        #average rating of the business from the API
        try:
            rival_ratings = []
            for result in place['nearby_places']:
                if result['name'] == name:
                    continue
                else:
                    rival_ratings.append(result['rating'])
            average_rating = round(sum(rival_ratings) / len(rival_ratings), 1)
            st.write(rival_ratings)
        except:
            average_rating = 0

        st.markdown('''
        <div class="container">
        ''', unsafe_allow_html=True)
        st.metric("Reviews", "{}" .format(average_rating))
    
    with col10:
        pass
    
    export_as_pdf = st.button("Export Report")
    
    if export_as_pdf:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, txt = "Google Maps Dashboard", ln = "1", align = "C")
        pdf.image(logo1.png, 5, 5, 100, 50, align = "C")
        pdf.cell(40, 10, txt = business_name, ln = "10", align = "C")
        #pdf.add_page()
        #pdf.image(tmpfile.name, 10, 10, 200, 100)
        #pdf.add_page()
        #pdf.image(tmpfile2.name, 10, 10, 200, 100)
        #pdf.cell(200, 10, txt = "Grafica 2",
             #ln = 1, align = 'C')
        #pdf.add_page()
        #pdf.write(5, 'No quiero ser chivato pero...')
        #pdf.image(tmpfile.name, 5, 5, 100, 50)
        #pdf.image(tmpfile2.name, 5, 5, 100, 50)
        html = create_download_link(pdf.output(dest="S").encode("latin-1"), "testfile")
        st.markdown(html, unsafe_allow_html=True)

st.markdown('''
    <style>
        #google-maps-dashboard > div > span{
            color: #00006d;
        }

        
    </style>
''', unsafe_allow_html=True)
requirements()
