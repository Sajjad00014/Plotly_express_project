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

# Add range filter for primary parameter if it's numeric
if np.issubdtype(df[primary].dtype, np.number):
    min_val, max_val = st.sidebar.slider(
        f"Select {primary} Range",
        float(df[primary].min()),
        float(df[primary].max()),
        (float(df[primary].min()), float(df[primary].max()))
    )
    df = df[(df[primary] >= min_val) & (df[primary] <= max_val)]

# Display data preview
st.write("### Data Preview")
st.dataframe(df.head())

# Show summary statistics for the selected state
if selected_state != 'Overall India':
    state_df = df[df['State'] == selected_state]
    st.write(f"### Summary Statistics for {selected_state}")
    st.write(state_df.describe())
else:
    st.write("### Summary Statistics for Overall India")
    st.write(df.describe())

# Plotting logic
if plot:
    if primary == secondary:
        st.error("Primary and Secondary parameters must be different.")
    else:
        with st.spinner('Generating plot...'):
            st.text('Size represents primary parameter')
            st.text('Color represents secondary parameter')

            title_text = f"{selected_state} - {primary} vs {secondary}"

            if selected_state == 'Overall India':
                # Plot for entire India
                fig = px.scatter_mapbox(
                    df, lat="Latitude", lon="Longitude", size=primary, size_max=35, color=secondary,
                    zoom=zoom_level, mapbox_style=map_style, width=1200, height=700, hover_name='District',
                    title=title_text
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Plot for selected state
                state_df = df[df['State'] == selected_state]
                fig = px.scatter_mapbox(
                    state_df, lat="Latitude", lon="Longitude", size=primary, size_max=35, color=secondary,
                    zoom=zoom_level, mapbox_style=map_style, width=1200, height=700, hover_name='District',
                    title=title_text
                )
                st.plotly_chart(fig, use_container_width=True)
