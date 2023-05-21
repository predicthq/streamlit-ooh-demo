import streamlit as st
import datetime
import pytz
from utils.predicthq import get_api_key, get_predicthq_client


def show_sidebar_options():
    # Sample data sourced from https://explore.geopath.io/explore
    locations = [
        {
            "id": 50443422,
            "name": "Market St NS 177ft E/O Hyde St",
            "address": "San Francisco County",
            "lat": 37.7791636517,
            "lon": -122.414388506,
            "tz": "America/Los_Angeles",
            "units": "imperial",
        },
        {
            "id": 50352763,
            "name": "Van Ness Ave",
            "address": "San Francisco County",
            "lat": 37.782581,
            "lon": -122.420719,
            "tz": "America/Los_Angeles",
            "units": "imperial",
        },
        {
            "id": 50352745,
            "name": "McAllister St",
            "address": "San Francisco County",
            "lat": 37.78004,
            "lon": -122.41994,
            "tz": "America/Los_Angeles",
            "units": "imperial",
        },
        {
            "id": 50352743,
            "name": "Sacramento St.",
            "address": "San Francisco County",
            "lat": 37.79057,
            "lon": -122.42889,
            "tz": "America/Los_Angeles",
            "units": "imperial",
        },
        {
            "id": 50419442,
            "name": "State College ES 100ft No Birch",
            "address": "Orange County",
            "lat": 33.9183694,
            "lon": -117.8828194,
            "tz": "America/Los_Angeles",
            "units": "imperial",
        },
        {
            "id": 50001951,
            "name": "Irvine Station - ITC (Amtrk Station) Bus Bay Shelter #3",
            "address": "Orange County",
            "lat": 33.657078,
            "lon": -117.73301,
            "tz": "America/Los_Angeles",
            "units": "imperial",
        },
    ]

    # Work out which location is currently selected
    index = 0

    if "location" in st.session_state:
        for idx, location in enumerate(locations):
            if st.session_state["location"]["id"] == location["id"]:
                index = idx
                break

    location = st.sidebar.selectbox(
        "OOH Locations",
        locations,
        index=index,
        format_func=lambda x: x["name"],
        help="Select the OOH location.",
        disabled=get_api_key() is None,
        key="location",
    )

    # Prepare the date range (today + 30d as the default)
    tz = pytz.timezone(location["tz"])
    today = datetime.datetime.now(tz).date()
    date_options = [
        {
            "id": "next_7_days",
            "name": "Next 7 days",
            "date_from": today,
            "date_to": today + datetime.timedelta(days=7),
        },
        {
            "id": "next_30_days",
            "name": "Next 30 days",
            "date_from": today,
            "date_to": today + datetime.timedelta(days=30),
        },
        {
            "id": "next_90_days",
            "name": "Next 90 days",
            "date_from": today,
            "date_to": today + datetime.timedelta(days=90),
        },
    ]

    # Work out which date is currently selected
    index = 2  # Default to next 90 days

    if "daterange" in st.session_state:
        for idx, date_option in enumerate(date_options):
            if st.session_state["daterange"]["id"] == date_option["id"]:
                index = idx
                break

    st.sidebar.selectbox(
        "Date Range",
        date_options,
        index=index,
        format_func=lambda x: x["name"],
        help="Select the date range for fetching event data.",
        disabled=get_api_key() is None,
        key="daterange",
    )

    # Use an appropriate radius unit depending on location
    radius_unit = (
        "mi" if "units" in location and location["units"] == "imperial" else "km"
    )

    st.session_state.suggested_radius = fetch_suggested_radius(
        location["lat"], location["lon"], radius_unit=radius_unit, industry="parking"
    )

    # Allow changing the radius if needed (default to suggested radius)
    # The Suggested Radius API is used to determine the best radius to use for the given location and industry
    st.sidebar.slider(
        f"Suggested Radius around OOH location ({radius_unit})",
        0.0,
        10.0,
        st.session_state.suggested_radius.get("radius", 2.0),
        0.1,
        help="[Suggested Radius Docs](https://docs.predicthq.com/resources/suggested-radius)",
        key="radius",
    )


@st.cache_data
def fetch_suggested_radius(lat, lon, radius_unit="mi", industry=None):
    phq = get_predicthq_client()
    suggested_radius = phq.radius.search(
        location__origin=f"{lat},{lon}", radius_unit=radius_unit, industry=industry
    )

    return suggested_radius.to_dict()
