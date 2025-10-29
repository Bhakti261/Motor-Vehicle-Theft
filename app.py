import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------- Load Data ----------------------
stolen_df = pd.read_csv("stolen_vehicles.csv")
locations_df = pd.read_csv("locations.csv")
make_df = pd.read_csv("make_details.csv")

# ---------------------- App Title ----------------------
st.title("🚗 Motor Vehicle Theft Analysis Dashboard")

# ---------------------- Sidebar Navigation ----------------------
st.sidebar.title("Dashboard Menu")
dashboard = st.sidebar.radio(
    "Select a Dashboard",
    ["Overview", "By Location", "By Vehicle Make"]
)

# ---------------------- Dashboard 1: Overview ----------------------
if dashboard == "Overview":
    st.header("🔍 Overall Summary")
    st.metric("Total Stolen Vehicles", len(stolen_df))
    st.metric("Unique Makes", stolen_df["make_id"].nunique())
    st.metric("Unique Locations", stolen_df["location_id"].nunique())

    # Visualization of vehicles stolen by year
    if "model_year" in stolen_df.columns:
        fig1 = px.histogram(
            stolen_df, x="model_year", nbins=20,
            title="Vehicles Stolen by Model Year",
            color_discrete_sequence=["#636EFA"]
        )
        st.plotly_chart(fig1)
    else:
        st.warning("Column 'model_year' not found in stolen_vehicles.csv")

# ---------------------- Dashboard 2: By Location ----------------------
elif dashboard == "By Location":
    st.header("📍 Location-Based Analysis")

    # Merge stolen vehicles with location details
    merged = stolen_df.merge(locations_df, on="location_id", how="left")

    # Detect a suitable column for location name
    possible_cols = [col for col in merged.columns if any(x in col.lower() for x in ["city", "location", "area", "state"])]
    if possible_cols:
        loc_col = possible_cols[0]  # use first matching column
        top_locations = merged[loc_col].value_counts().head(10)
        fig2 = px.bar(
            top_locations,
            x=top_locations.index,
            y=top_locations.values,
            title=f"Top 10 Locations for Vehicle Theft ({loc_col})",
            labels={"x": loc_col.capitalize(), "y": "Number of Vehicles Stolen"},
            color_discrete_sequence=["#EF553B"]
        )
        st.plotly_chart(fig2)
    else:
        st.warning("No location-related column found in locations.csv")

# ---------------------- Dashboard 3: By Vehicle Make ----------------------
elif dashboard == "By Vehicle Make":
    st.header("🚘 Vehicle Make Insights")

    # Merge stolen vehicles with make details
    merged = stolen_df.merge(make_df, on="make_id", how="left")

    # Detect a column for make name
    possible_make_cols = [col for col in merged.columns if any(x in col.lower() for x in ["make", "brand", "manufacturer"])]
    if possible_make_cols:
        make_col = possible_make_cols[0]
        top_makes = merged[make_col].value_counts().head(10)

        # Bar chart
        fig3 = px.bar(
            top_makes,
            x=top_makes.index,
            y=top_makes.values,
            title=f"Top 10 Most Stolen Vehicle Makes ({make_col})",
            labels={"x": make_col.capitalize(), "y": "Number of Vehicles Stolen"},
            color_discrete_sequence=["#00CC96"]
        )
        st.plotly_chart(fig3)

        # Pie chart
        fig4 = px.pie(
            merged,
            names=make_col,
            title="Distribution of Stolen Vehicles by Make",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig4)
    else:
        st.warning("No make-related column found in make_details.csv")

# ---------------------- Footer ----------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, Pandas & Plotly")
