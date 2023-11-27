import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

#position stack for lat long


st.title("NYT Top Stories")

#adjust parameters
date = "current" #YYYY-MM-DD

#request
api_key = 'eGuDfZ7wBWskKTJeBnZqI0UCQCYApB3i'
api_url = 'https://api.nytimes.com/svc/topstories/v2/world.json'
params = {'api-key': api_key}



def create_show_table():
    #make dict from json data for table
    results = data.get("num_results")
    stories_list = data.get("results")
    #build table
    rank_list = []
    title_list = []
    author_list = []
    for story in stories_list:
        story_details_dict = story
        book_rank = book_details_dict.get("rank")
        book_title = book_details_dict.get("title")
        book_author = book_details_dict.get("author")

        rank_list.append(book_rank)
        title_list.append(book_title)
        author_list.append(book_author)
    #show table    
   
    st.dataframe(df, hide_index=True)


if st.button("GO"):
   # make the API request
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        #create_show_table()
        st.write(data)

    else:
        st.write("Error: Unable to fetch data from the New York Times Top Stories API")
        st.write("Possible: Not enough time between requests")
        st.write("Max 500/day 5/min")