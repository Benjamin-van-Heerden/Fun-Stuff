import streamlit as st

st.set_page_config(
    page_title="Collisions App",
    layout="wide"
)

import pandas as pd
import numpy as np
from os.path import join, dirname
import pydeck as pdk
import plotly.express as px

data_location = join(dirname(__file__), "collisions_final.csv")


@st.cache(persist=True)
def load_data(n_rows=None):
    lowercase = lambda x: str(x).lower()
    dtypes = {
        "INJURED_PERSONS": int,
        "KILLED_PERSONS": int,
        "COLLISION_ID": int
    }
    if not n_rows:
        data = pd.read_csv(data_location, parse_dates=[["CRASH_DATE", "CRASH_TIME"]], dtype=dtypes)
    else:
        data = pd.read_csv(data_location, nrows=n_rows, parse_dates=[["CRASH_DATE", "CRASH_TIME"]], dtype=dtypes)

    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(columns={"crash_date_crash_time": "date_time"}, inplace=True)
    data["hour"] = data["date_time"].dt.hour
    return data


# %%
data = load_data(n_rows=100000)

st.title("Motor Vehicle Collisions in New York City")
st.subheader("Streamlit dashboard used to analyze vehicle collisions in New York City")
with st.expander("Show raw data"):
    st.dataframe(data)

midpoint = (data["latitude"].mean(), data["longitude"].mean())
st.header(f"Collisions by hour:")
hour_to_check = st.slider("Hour to look at:", 0, 23, 8)
hour_df = data[data["date_time"].dt.hour == hour_to_check][["date_time", "latitude", "longitude"]]
st.markdown(f"#### Vehicle collisions between {hour_to_check}:00 and {hour_to_check + 1}:00")

collision_layer = pdk.Layer(
    'HexagonLayer',
    hour_df,
    get_position=['longitude', 'latitude'],
    auto_highlight=True,
    radius=200,
    elevation_scale=8,
    pickable=True,
    elevation_range=[0, 1000],
    extruded=True,
    coverage=1
)

webGLMap = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 10,
        "pitch": 50
    },
    layers=[collision_layer],
)

st.write(webGLMap)

st.header("Breakdown of collisions - hour by hour:")
hour_to_hour = data.groupby("hour").size()
fig = px.bar(
    x=hour_to_hour.index,
    y=hour_to_hour.values,
    height=600,
    width=1200,
    title="Collisions By Hour"
)
fig.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title="Number of Collisions"
)
with st.expander("Bar Chart By Hour"):
    st.write(fig)



st.header("Collisions by number of persons injured:")
injured_people = st.slider("Number of Injured People", data["injured_persons"].min(), data["injured_persons"].max(), 2)
st.map(data[data["injured_persons"] == injured_people][["latitude", "longitude"]])



# %%
