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
#pre declare
article_list = []
article_tuple = ()
article_results = []

if "article_list" not in st.session_state:
    st.session_state.article_list = []
if "article_tuple" not in st.session_state:
    st.session_state.article_tuple = ()

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
    else:
        st.write("Error: Unable to fetch data from the New York Times Top Stories API")
        st.write("Possible: Not enough time between requests")
        st.write("Max 500/day 5/min")

    article_num_results = article_data.get("num_results")
    article_results = article_data.get("results")
    if "article_data" not in st.session_state:
        st.session_state.article_results = ""
    st.session_state["article_results"] = article_results

    for result in article_results:
        title = result.get("title")
        if title != "":
            article_list.append(title)
            article_tuple += (title,)
        #if st.session_state["article_selected"] != "":
            #st.session_state["image_url"] = ""
    st.session_state["article_list"] = article_list

if "article_selected" not in st.session_state:
    st.session_state.article_selected = ""
if "image_url" not in st.session_state:
    st.session_state.image_url = ""
if "latitude" not in st.session_state:
    st.session_state.latitude = ""
if "longitude" not in st.session_state:
    st.session_state.longitude = ""

st.write("session state")
st.session_state

article_selected = st.selectbox(
    "Articles",
    key="article_selected",
    options=st.session_state["article_list"],
    index=None,
    placeholder="Select an article",
    disabled=False
    )


#displaying selected article information
if st.session_state["article_selected"] != "":
    print("test")
    for article in st.session_state["article_results"]:
        if article.get("title") == st.session_state["article_selected"]:
            st.header(article.get("title"))
            st.image(
                #image link
                article.get("multimedia")[1].get("url"),
                width=400, # Manually Adjust the width of the image as per requirement
            )
            if len(article.get("geo_facet")) > 0:
                latlon = get_lat_long(article.get("geo_facet")[0])
                #st.write(latlon)
                map_dict = {"LAT":[latlon[0]], "LON":[latlon[1]]}
                map_data = pd.DataFrame(data=map_dict)
                st.map(data=map_data, zoom=7)

                
            else:
                st.write("No location data")
            



    
    
    
