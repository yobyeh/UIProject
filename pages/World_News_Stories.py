import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

#position stack for lat long

#adjust parameters
date = "current" #YYYY-MM-DD

#request
api_key = 'eGuDfZ7wBWskKTJeBnZqI0UCQCYApB3i'

def get_lat_long(location):
    import http.client, urllib.parse

    conn = http.client.HTTPConnection('api.positionstack.com')

    params = urllib.parse.urlencode({
        'access_key': 'f204082c4dff73ceeabbf05d5c4eaf83',
        'query': location,
        'limit': 1,
    })

    conn.request('GET', '/v1/forward?{}'.format(params))

    res = conn.getresponse()
    location_data = res.read()
    location_json = json.loads(location_data.decode('utf-8'))

    #st.write(location_json)
    location1 = location_json.get("data")
    location2 = location1[0]
    latitude = location2.get("latitude")
    longitude = location2.get("longitude")
    return (latitude, longitude)

#start of page
st.title("NYT World Top Stories")

#radio button for selection world vs us
radio_selection = st.radio(
    "Set label",
    ["US", "World"],
    label_visibility="collapsed",
    horizontal=True
)



if st.button("Retrieve Data"):
    # make the API request
    location_selection = "us"
    if radio_selection == "World":
        location_selection = "world"

    api_url = 'https://api.nytimes.com/svc/topstories/v2/{}.json'.format(location_selection)
    params = {'api-key': api_key}
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        article_data = response.json()
        st.write(article_data)
        article_num_results = article_data.get("num_results")
        article_results = article_data.get("results")



        article_list = []
        article_tuple = ()
        article_selected = st.selectbox(
            "Articles",
            article_tuple,
            index=None,
            placeholder="Select an article",
        )

        st.write('You selected:', option)

        #get data
        data = response.json()

        #load titles in multiselect

        #show title

        #show link

        #get location

        #get lat long

        #plot map

        get_lat_long("Uttarakhand (India)")
        st.write(data)
    else:
        st.write("Error: Unable to fetch data from the New York Times Top Stories API")
        st.write("Possible: Not enough time between requests")
        st.write("Max 500/day 5/min")
    
    latlong = get_lat_long("Uttarakhand (India)")
    if latlong:
        print(latlong)
    else:
        st.write("No location data given")

    
    
    
