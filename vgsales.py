import streamlit as st
import numpy as np, pandas as pd 
import altair as alt 
from urllib.error import URLError

@st.cache_data
def get_data():
    path_ = "datasets/vgsales.csv"
    df = pd.read_csv(path_)
    # drop NAN on Year & Publisher
    df.dropna(inplace=True)
    # cleaning Year column
    df.Year = df.Year.astype('str')
    df.Year = df.Year.str.replace('.0','')
    return df

try:
    df = get_data()
    st.title(""" Video games sales analysis """)
    
    # total sales metrics
    " # Sales Metrics"
    global_sales = np.round(np.sum(df.Global_Sales),2)
    eu_sales = np.round(np.sum(df.EU_Sales),2)
    na_sales = np.round(np.sum(df.NA_Sales),2)
    jp_sales = np.round(np.sum(df.JP_Sales),2)
    other_sales = np.round(np.sum(df.Other_Sales),2)

    # create a series of columns 
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    # card
    col1.metric("Global Sales Total",global_sales,"USD")
    col2.metric("North America Sales",na_sales,"USD")
    col3.metric("European Union Sales",eu_sales,"USD")
    col4.metric("Japan Sales Total",jp_sales,"USD")
    col5.metric("Other Sales",other_sales,"USD")

    # filters (platforms)
    st.write(" # Select a Platform and Genre")
    col6, col7 = st.columns(2)
    platforms = df.Platform.unique()
    selected_platform = col6.multiselect(
        "Platforms",platforms,[platforms[0],
                               platforms[1]]
    )

    # filter (genre)
    genre = df.Genre.unique()
    selected_genre = col7.multiselect(
        "Genre", genre,[genre[0], genre[1]]
    )

    filtered_data = df[df["Platform"].isin(selected_platform) &
                       df["Genre"].isin(selected_genre)]

    # table
    if not selected_platform and selected_genre:
        st.error("Please select both filters from platform and genre")
    else:
        st.write(""" Filtered result obtained""")

    # table end

    # plots 
    # bar charts
    # Top 10
    st.write("# Top Platforms Chart") 
    bar0 = df.groupby(['Platform'])['Global_Sales'].sum().nlargest(n=10).sort_values(ascending=False)
    st.bar_chart(bar0, y='Global_Sales',
                 color="#d4af37")

    st.write(" # Bar chart from filtered result")
    st.write(""" ## Global sales per genre & platform """)
    bar1 = filtered_data.groupby(['Platform'])['Global_Sales'].sum().sort_values(ascending=True)
    st.bar_chart(bar1, color="#d4af37", width=200, height=400)

    # line chart 
    st.write(""" ## Global Sales over Time """)
    chart = (
            alt.Chart(filtered_data)
            .mark_line()
            .encode(
                x="Year",
                y=alt.Y("Global_Sales", stack=None),
            )
        )
    st.altair_chart(chart, use_container_width=True)
    
        # area chart 
    st.write(""" ## Global Sales over Time """)
    chart = (
            alt.Chart(filtered_data)
            .mark_area(opacity=0.3)
            .encode(
                x="Year",
                y=alt.Y("Global_Sales", stack=None),
                
            )
        )
    st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )