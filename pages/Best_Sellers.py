import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
from datetime import date

st.title("NYT Best Sellers Book List")

#adjust parameters
if "selected_list" not in st.session_state:
    st.session_state.selected_list = ""
if "selected_date" not in st.session_state:
    st.session_state.selected_date = datetime.today()


#current
date = "" #YYYY-MM-DD
options = []
author_list=[]
disable_date = False

#request
api_key = 'eGuDfZ7wBWskKTJeBnZqI0UCQCYApB3i'
params = {'api-key': api_key}

top_lists = ["hardcover-fiction", "trade-fiction-paperback", "hardcover-nonfiction", "paperback-nonfiction"]

def create_show_table():
    #make dict from json data for table
    results = data.get("num_results")
    results_dict = data.get("results")
    books_list = results_dict.get("books")
    #build table
    rank_list = []
    title_list = []
    for book in books_list:
        book_details_dict = book
        book_rank = book_details_dict.get("rank")
        book_title = book_details_dict.get("title")
        book_author = book_details_dict.get("author")

        rank_list.append(book_rank)
        title_list.append(book_title)
        author_list.append(book_author)
    #show table    
    new_books_dict = {"Rank":rank_list, "Title":title_list, "Author":author_list}
    df = pd.DataFrame(data = new_books_dict)
    st.dataframe(df, hide_index=True)

def create_show_chart():
    st.write("Authors vs number books on this list")
    series = pd.Series(author_list)
    counts = series.value_counts().reset_index()
    counts.columns = ["Element", "Count"]
    st.bar_chart(counts.set_index("Element"))
    st.line_chart(counts.set_index("Element"))


st.header("Filters")
#checkbox
check = st.checkbox("Today")
if check:
    disable_date = True

#list slider
st.session_state["selected_list"] = st.select_slider(
    'Select a top list',
    options=top_lists,
    )

#date slider
st.session_state["Selected_date"]= st.slider(
    "select a date",
    #yyy-mm-dd
    min_value=datetime(2010,1,1),
    max_value=datetime(2023,11,1),
    format="YYYY/MM/DD",
    disabled=disable_date
)

#st.write("session state")
#st.write(st.session_state)

if st.button("Load Best Sellers"):
    # make the API request
    if check:
        date_selected ="/" + datetime.today().strftime("%Y-%m-%d")
    else:
        date_selected = "/" + st.session_state["selected_date"].strftime("%Y-%m-%d")
    print(date_selected)
    
    list_selected = "/" + st.session_state["selected_list"]
    
    api_url = 'https://api.nytimes.com/svc/books/v3/lists{}{}.json'.format(date_selected, list_selected)
    #api_url = 'https://api.nytimes.com/svc/books/v3/lists/names.json'

    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        st.success('Data Loaded', icon="✅")
        #st.write(data)
        create_show_table()
        create_show_chart()

    else:
        st.warning('Unable to fetch data from the New York Times', icon="⚠️")
        st.write("Possible: Not enough time between requests")
        st.write("Max 500/day 5/min")