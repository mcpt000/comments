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

st.set_page_config(page_title = "Google Maps Dashboard",
    page_icon = "🗺️",
    layout = "wide")

#page 1

def requirements():
    st.title("Google Maps Dashboard")
    st.subheader("Get insights about your business & competitors")

    business_name = st.text_input("Enter your business name")
    latitude = st.text_input("Enter your business latitude")
    longitude = st.text_input("Enter your business longitude")
    #modifie according to the preprocessing
    competitor_type = st.selectbox("Select your competitor type", ["Restaurants", "Hotels", "Shopping", "Entertainment", "Other"])
    radius = st.text_input("Enter your business radius",'10 km')

    st.markdown("*If you don't know the latitude and longitude of your business, click [here](https://www.google.com/maps).*")
    
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

    if st.button("Submit"):
        #remove the 'Km' from the radius
        
        dashboard(business_name, radius, latitude, longitude, competitor_type)

def dashboard(business_name, radius, latitude, longitude, competitor_type):
    #two columns
    col1, col2 = st.columns([1,5])

    with col1:
        #image has to be the icon in the API
        imagen = requests.get('https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png').content
        st.image(imagen, width = 100)
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
    st.markdown("#### Address: {}" .format(address))

 

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
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
            #add the business location to the map in a different color
            pdk.Layer(
                'ScatterplotLayer',
                data=df.tail(1),
                get_position='[lon, lat]',
                get_color='[0, 170, 228, 160]',
                get_radius=200,
            )
        ],
    ))

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("### Your business")

    with col6:  
        st.markdown("### Competitors Average")
    
    col7, col8, col9, col10 = st.columns(4)
    with col7:
        your_reviews = 100
        st.metric("Reviews", "{}" .format(your_reviews))
    
    with col8:
        your_comments = 100
        st.metric("Comments", "{}" .format(your_comments))

    with col9:
        competitors_reviews = 100
        st.metric("Reviews", "{}" .format(competitors_reviews))
    
    with col10:
        competitors_comments = 100
        st.metric("Comments", "{}" .format(competitors_comments))


    ranking = 1
    st.markdown("### Your business is \#{} in the ranking in a radius of {} km" .format(ranking, radius))

    #button to download the page as a pdf

    report_text = st.text_input("Report Text")

    export_as_pdf = st.button("Export Report")

    def create_download_link(val, filename):
        b64 = base64.b64encode(val)  # val looks like b'...'
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

    if export_as_pdf:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, report_text)
        
        html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

        st.markdown(html, unsafe_allow_html=True)

requirements()
