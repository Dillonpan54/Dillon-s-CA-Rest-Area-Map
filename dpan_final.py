import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
import pandas as pd
import seaborn as sns
import json
from PIL import Image

"""Dillon Pan, 
Cs230 Section 5, 
Dataset: California Rest Areas, 
URL: 
  Description: this streamlit app visualizes all rest areas in California, there are three main sections,
   first there is a main page with a pivot table showing vending machines by county, 
   then there is the descriptive statistics where the number of rest areas per county and route can be shown
   there are various user friendly adjustments to view the data(have fun!)
   Lastly, there is the Map section which maps out each rest area in the state, you can also filter by specific county
   and choose from a few different map styles, hovering over each point will give additional details. Enjoy!"""

def count_and_sort(df, col_criteria, order = 'descending'):

    counting_df = df[col_criteria].value_counts()
    if order == 'descending':
        sorted_dat = counting_df.sort_values(ascending = False)
    if order == 'ascending':
        sorted_dat = counting_df.sort_values(ascending = True)

    return sorted_dat
#[PY1] this function takes dataframe(df), criteria, and order,counts the # of rows in the column matching "criteria"
#[PY2][DA2] this function returns the sorted data as a series (multiple values) frequency and sorts by ascending or descending order
#[PY3]returns series, called in Rest Area Distribution, and Rest Area Map
#[DA7] takes frequency count of the rows in the column with a unique value
#[DA4] filters by criteria input(condition) ex:county, returning series

def graph_by_type(sorted_dat, graph, x_col):
#takes data and graphs it using seaborne
    if graph == "Bar Graph": #[VIZ1]seaborne barplot
        ax = sns.barplot(x = sorted_dat.index, y = sorted_dat.values,
                         palette = sns.color_palette("crest"))
        ax.set_title(f'# of Rest Areas by {x_col}') #title by criteria
        st.pyplot()
    if graph == "Pie Chart":#[VIZ2] seaborne pie chart
        ax = plt.pie(sorted_dat, labels=sorted_dat.index,
                     palette = sns.color_palette("crest"),
                     autopct='%.0f%%')
        ax.set_title(f'Proportion of Rest Areas by {x_col}') #title by criteria
        st.pyplot()
    if graph == "Horizontal Bar Graph": #[VIZ3] seaborne horizontal barplot
        ax = sns.barplot(x=sorted_dat.values, y=sorted_dat.index, #switches axis from bar graph
                         palette = sns.color_palette("crest"))
        ax.set_title(f'# of Rest Areas by {x_col}')
        st.pyplot()
#color palettes: https://seaborn.pydata.org/tutorial/color_palettes.html


st.set_option('deprecation.showPyplotGlobalUse', False) #kept giving me warnings, turned it off

path = "C:/Users/dillo/Downloads/Python_Final/" #my folder path

df_cali = pd.read_csv(path + "Rest_Areas.csv") #reads the dataset csv file

df_cali.set_index('OBJECTID')

map_style = {
            'Mapbox Outdoors': 'mapbox://styles/mapbox/outdoors-v12',
             'Navigation Day': 'mapbox://styles/mapbox/navigation-day-v1',
             'Navigation Night': 'mapbox://styles/mapbox/navigation-night-v1',
            'Satellite Streets':'mapbox://styles/mapbox/satellite-streets-v12',
             }  #[PY5] Dictionary stores different map style URLS, called in the map later on and in selectbox
#https://docs.mapbox.com/api/maps/styles/
df_cali.columns = ['X_coordinate', 'Y_coordinate','ObjectID','County Number', 'Rest Name', 'Address',
                   'City', 'Zipcode', 'useless1','useless2','useless3', 'lat', 'lon',
                   'District','County Code', 'County', 'Route', 'RestArea', 'Location',
                   'TrafficDir','Restroom','Water', 'PicnicTables',
                   'Phone', 'Handicap', 'RV','Vending', 'PetArea'] #[DA1]Renamed columns for better readability and calling

df_cali = df_cali.drop( columns= ['useless1',#[DA7] dropped postmile columns, werent useful to me
                                  'useless2',
                                  'useless3']) #[DA1] renamed columns and removed postmile_p, postmile, and postmile_p




#Navigation and vistualization
st.sidebar.header("California Rest Stops")
selected_feature = st.sidebar.radio("Please select a feature:", ["Main Page", "Rest Area Distribution", "Rest Area Map"])
#[ST1][ST4] sidebar for navigation
if selected_feature == "Main Page":
    st.title("California Rest Stops")
    img = Image.open("C:/Users/dillo/Downloads/Python_Final/Rest_Area.jpg")
    st.image(img, width= 500)  #[ST4]Displaying image on front page
    st.write("Vending Machines available at Rest Areas by County:")
    st.dataframe(pd.pivot_table(df_cali, index='County', #county column set as row index
                   columns='Vending', #vending column set as column index
                   aggfunc='size').fillna(0)) #'size' counts the number of non-null values in county and vending
    #.fillna(0) just replaces missing values with 0, so I can count the vending machines in each county
    #noticed that vending was not in all counties, added pivot table to show it
if selected_feature == "Rest Area Distribution": #when rest area distribution is selected
    st.title("California Rest Stops Distribution") #sets title
    col_criteria = st.selectbox("Please select a criteria:", ["County", "Route"]) #selectbox for criteria 'route' or county
    order = st.selectbox("Sort order:", ["descending", "ascending"]) #[ST2] selectbox for order
    graph = st.selectbox("Please select a graph type:", ["Bar Graph", "Pie Chart", "Horizontal Bar Graph"])
    #[ST2] selectbox for graph type (vizualization)
    selected_data = df_cali #uses df_cali as selected data holds filtered data base on user choices
    if col_criteria == "County": #when county selected
        selected_counties = st.multiselect('Select County:', df_cali.County.unique()) #[ST3]multiselect using unique values from county column
        #selected_counties stores list of chosen counties
        selected_data = df_cali[df_cali['County'].isin(selected_counties)]
        #filters df_cali, only takes rows where the county value is also in the selected counties list
        #makes sure selected data only has rows from selected counties
    elif col_criteria == "Route": #when route is selected
        selected_routes = st.multiselect('Select Route', df_cali.Route.unique())#[ST3]multiselect using unqiue route values
        #selected_routes holds list of selected routes
        selected_data = df_cali[df_cali['Route'].isin(selected_routes)]
        # filters df_cali, only takes rows where the route value is also in the selected routes list
        # makes sure selected data only has rows from selected routes
        selected_data['Route'] = selected_data['Route'].astype(str)
        #converts route column(integer by defult) into string
        #sorting function was sorting route values previously so had to change to string
    sorted_dat = count_and_sort(selected_data, col_criteria, order) # calls count and sort to count number of rows for each unique value in selected data
    graph_by_type(sorted_dat, graph, x_col=col_criteria) #calls graphing function x-axis set to col_criteria either county or route
    max_val = sorted_dat.max() #calculates max value
    min_val = sorted_dat.min()#calaculates min value
    sorted_dat = pd.DataFrame(sorted_dat) #converts sorted_dat series to DF

    st.write(f" The max and min value for '{col_criteria}' selected are: {max_val} and {min_val}")
    # [DA3] max and min values calculated and printed

if selected_feature == "Rest Area Map": #when map is selected

    # Create a unique list of counties (assuming 'County' column exists)
    county_list = list(df_cali['County'].unique()) #creates and stores list of unique county values
    county_list.insert(0, "All") #inserts all at beginning allowing users to view all rest areas or filter by county

    selected_county = st.selectbox("Please select a county:", county_list) #[ST2]makes selectbox of county lists

    map_selection = st.selectbox("Select a map style:", map_style.keys()) #[ST2]calls map_styles dictionary to allow user to choose a style


    if selected_county == "All": #if all chosen
        sub_df = df_cali.copy()  # .copy() copies new verison of df_cali
        zooming = 6 #sets zoom further out
        point_size = 5000 #marker size larger so they are visible
    else:
        sub_df = df_cali[df_cali["County"] == selected_county] #filters df_cali for only areas in the selected county
        zooming = 10 #zooms into county
        point_size = 1500  # makes point smaller so its not the size of a city
    layer = pdk.Layer( #defines a pydeck scatterplot layer, displays markers for each rest area
        type='ScatterplotLayer', #layer type
        data=sub_df, #uses filtered sub_df of cali for markers
        get_position='[lon, lat]',  # retries marker positions from longitude and latitude
        get_radius=point_size,  # Adjust radius if needed, sets point size from selectbox
        get_fill_color=[180, 0, 200, 140], # sets marker color
        pickable=True #allows tooltips to appear on hover
    )

    # Tooltip configuration
    tool_tip = {
        "html": "Rest Area Name:<br/> <b>{RestArea}</b> <br/> <b>{County}</b> <br/> Route: <b>{Route}</b> <br/> "
                "Water: <b>{Water}</b> <br/> Picnic: <b>{PicnicTables}</b> <br/> Phone <b>{Phone}</b> <br/>  "
                "Handicap: <b>{Handicap}</b> <br/> RV: <b>{RV}</b> <br/> Vending: <b>{Vending}</b> <br/> "
                "Pet Area: <b>{PetArea}</b>", #tooltip showing county, route, facilities details
        "style": {"backgroundColor": 'black', #background color
                  "color": "white"} #text color
        }

    # Set initial view state when all is selected
    view_state = pdk.ViewState(
        latitude=sub_df["lat"].mean(), #initial latitude to average of the data
        longitude=sub_df["lon"].mean(), #^^^
        zoom=zooming,  # Adjust zoom level if needed
        pitch=0
    )

    # creates pydeck based on selected county
    map = pdk.Deck(
        map_style= map_style[map_selection],#calls the value of the key from map selection
        initial_view_state=view_state, #sets initial view
        layers=layer, #specifies layer displayed on map
        tooltip=tool_tip #shows tooltip as made earlier
    )

    st.pydeck_chart(map) #[VIZ4] Detailed Scatterplot Map
