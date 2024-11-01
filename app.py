import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Set wide page layout
st.set_page_config(layout='wide')

# Load data
df = pd.read_csv('india.csv')

# Prepare sidebar options
list_of_states = list(df['State'].unique())
list_of_states.insert(0, 'Overall India')
map_styles = ["carto-positron", "open-street-map", "stamen-terrain", "stamen-watercolor"]

# Sidebar controls
st.sidebar.title("India's Data Visualization")
selected_state = st.sidebar.selectbox('Select a state', list_of_states)
primary = st.sidebar.selectbox('Select Primary Parameter', sorted(df.columns[5:]))
secondary = st.sidebar.selectbox('Select Secondary Parameter', sorted(df.columns[5:]))
zoom_level = st.sidebar.slider('Select Map Zoom Level', 4, 10, 5)
map_style = st.sidebar.selectbox("Select Map Style", map_styles)
plot = st.sidebar.button('Plot your Graph')

# Display data preview
st.write("### Data Preview")
st.dataframe(df.head())

# Plotting logic
if plot:
    if primary == secondary:
        st.error("Primary and Secondary parameters must be different.")
    else:
        st.text('Size represents primary parameter')
        st.text('Color represents secondary parameter')

        if selected_state == 'Overall India':
            # Plot for entire India
            fig = px.scatter_mapbox(
                df, lat="Latitude", lon="Longitude", size=primary, size_max=35, color=secondary,
                zoom=zoom_level, mapbox_style=map_style, width=1200, height=700, hover_name='District'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Plot for selected state
            state_df = df[df['State'] == selected_state]
            fig = px.scatter_mapbox(
                state_df, lat="Latitude", lon="Longitude", size=primary, size_max=35, color=secondary,
                zoom=zoom_level, mapbox_style=map_style, width=1200, height=700, hover_name='District'
            )
            st.plotly_chart(fig, use_container_width=True)
