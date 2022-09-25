#import libraries

import streamlit as st
import pandas as pd
import numpy as np
import time 
from datetime import date
import matplotlib.pyplot as plt
import requests
import pydeck as pdk
import base64
from fpdf import FPDF

from tempfile import NamedTemporaryFile
from sklearn.datasets import load_iris

st.set_page_config(page_title = "Google Maps Dashboard",
    page_icon = "🗺️",
    layout = "wide")

#page 1

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
    with col1:
        pass
    with col2:
        st.markdown("<h6 style='text-align: center;'> GUPY MAPS is a web app that will help you to know the position of your business in the digital market, know your metrics and those of the competition with just a few steps.  </h6>", unsafe_allow_html=True)
        business_name = st.text_input("Enter your business name")
        latitude = st.text_input("Enter your business latitude")
        longitude = st.text_input("Enter your business longitude")
        #modifie according to the preprocessing
        competitor_type = st.selectbox("Select your competitor type", ["Restaurants", "Hotels", "Shopping", "Entertainment", "Other"])
        radius = st.text_input("Enter your business radius in meters",'10000 m')
        st.markdown("*If you don't know the latitude and longitude of your business, click [here](https://www.google.com/maps).*")
    with col3:
        pass
    
    def check(radius, latitude, longitude, competitor_type, business_name):
        radius = radius.split(' ')[0]
        if business_name == "" or latitude == "" or longitude == "" or radius == "":
            st.warning("Please fill in all the fields")
        #check if the radius is a number
        elif radius.isdigit() == False or int(radius) == 0 or int(radius)< 0:
            st.warning("Please enter a valid radius")
        #check if the latitude and longitude are in the correct range
        elif float(latitude) < -90 or float(latitude) > 90 or float(longitude) < -180 or float(longitude) > 180:
            st.warning("Please enter a valid latitude and longitude")
        #check if a selection has been made
        elif competitor_type == "Select your competitor type":
            st.warning("Please select a competitor type")
        else:
            return True

    if st.button("Submit"):
        if check(radius, latitude, longitude, competitor_type, business_name):
            dashboard(business_name, radius, latitude, longitude, competitor_type)


def dashboard(business_name, radius, latitude, longitude, competitor_type):
    #two columns
    col1, col2 = st.columns([1,9])

    with col1:
        st.markdown("""
        <style>
        img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        }
        </style>
        """, unsafe_allow_html=True)
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
    points=4

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
    #business hours
    #business hours from the API
        hours = ['Monday: 10:00 - 20:00', 'Tuesday: 10:00 - 20:00', 'Wednesday: 10:00 - 20:00', 'Thursday: 10:00 - 20:00', 'Friday: 10:00 - 20:00', 'Saturday: 10:00 - 20:00', 'Sunday: 10:00 - 20:00']
        st.markdown("### Business Hours")
        for i in hours:
            st.markdown('- {}'.format(i))

    with col4:
        #type of business
        #type of business from the API
        type_of_business = ['restaurant', 'cafe', 'bar', 'bakery', 'meal_takeaway', 'meal_delivery']
        st.markdown("### Type of Business")
        for i in type_of_business:
            st.markdown("- {}" .format(i))
    
    #business address
    #business address from the API
    address = "Calle de la Cruz, 1, 28012 Madrid, Spain"
    st.markdown("<h4  style='color :darkcyan;'> Address: {} </h4r>".format(address), unsafe_allow_html=True)

 

    #map
    #map from the API
    df = pd.DataFrame(
    np.random.randn(10, 2) / [50, 50] + [float(latitude), float(longitude)],
    columns=['lat', 'lon'])
    #add the business location to the dataframe
    df = df.append({'lat': float(latitude), 'lon': float(longitude)}, ignore_index=True)
    print(df)

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
        your_reviews = 100
        st.markdown('''
        <div class="container">
        ''', unsafe_allow_html=True)
        st.metric("Reviews", "{}" .format(your_reviews))
    
    with col8:
        your_comments = 100
        st.markdown('''
        <div class="container">
        ''', unsafe_allow_html=True)
        st.metric("Comments", "{}" .format(your_comments))

    with col9:
        competitors_reviews = 100
        st.markdown('''
        <div class="container">
        ''', unsafe_allow_html=True)
        st.metric("Reviews", "{}" .format(competitors_reviews))
    
    with col10:
        competitors_comments = 100
        st.markdown('''
        <div class="container">
        ''', unsafe_allow_html=True)
        st.metric("Comments", "{}" .format(competitors_comments))


    ranking = 1
    st.markdown("### Your business is \#{} in the ranking in a radius of {}" .format(ranking, radius))


requirements()
