import pandas as pd
import numpy as np 
import streamlit as st
import plotly.express as px
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

st.title('IE6600 COMPUTATION AND VISUALIZATION PROJECT 2')
data = pd.read_csv('C:/Users/GIGABITE/Downloads/ida_voting_power_of_member_countries_19-10-2024_edited.csv')

columns_to_keep = [
    'Member', 
    'Member Classification', 
    'Number of Votes', 
    'Percentage of Total Voting Power', 
    'As of Date'
]
cleaned_data = data[columns_to_keep].dropna()

# Save the cleaned dataset
cleaned_data.to_csv('cleaned_ida_voting_power.csv', index=False)

print("File saved as 'cleaned_ida_voting_power.csv' in the current directory.")

# Load cleaned data
cleaned_data = pd.read_csv('cleaned_ida_voting_power.csv')

# Sidebar layout
st.sidebar.title("IDA Voting Power Dashboard")
st.sidebar.subheader("Filters & Options")

# Option 1: Show Raw Data
view_data = st.sidebar.checkbox("Show Raw Data")
if view_data:
    st.write("### Raw Dataset")
    st.dataframe(cleaned_data)

# Option 2: Select Visualization
visualization = st.sidebar.selectbox(
    "Select Visualization",
    [
        "Distribution by Member Classification",
        "Top 10 Members by Voting Power",
        "Cumulative Distribution of Votes",
        "Votes vs. Voting Power",
        "Geographical Distribution",
    ]
)

# Option 3: Filter by Member Classification
member_classification = st.sidebar.multiselect(
    "Filter by Member Classification",
    options=cleaned_data["Member Classification"].unique(),
    default=cleaned_data["Member Classification"].unique(),
)

# Option 4: Filter by Voting Power Percentage
voting_power_range = st.sidebar.slider(
    "Filter by Voting Power Percentage",
    min_value=float(cleaned_data["Percentage of Total Voting Power"].min()),
    max_value=float(cleaned_data["Percentage of Total Voting Power"].max()),
    value=(
        float(cleaned_data["Percentage of Total Voting Power"].min()),
        float(cleaned_data["Percentage of Total Voting Power"].max()),
    ),
)

# Option 5: Search for a Specific Country
search_country = st.sidebar.text_input("Search for a Specific Country")

# Apply Filters
filtered_data = cleaned_data[
    (cleaned_data["Member Classification"].isin(member_classification)) &
    (cleaned_data["Percentage of Total Voting Power"] >= voting_power_range[0]) &
    (cleaned_data["Percentage of Total Voting Power"] <= voting_power_range[1])
]

if search_country:
    filtered_data = filtered_data[filtered_data["Member"].str.contains(search_country, case=False)]

# Main visualization section
st.title("IDA Voting Power Analysis")
st.write("### Filtered Dataset")
st.dataframe(filtered_data)

# Display summary statistics below the dataset
st.write("### Summary Statistics")
st.write("""
The following table provides key statistical insights into the filtered data:
""")
st.write(filtered_data.describe())

# Generate visualizations based on selection
if visualization == "Distribution by Member Classification":
    st.subheader("Distribution of Voting Power by Member Classification")
    
    st.markdown("""
This dashboard provides insights into the Voting Power distribution among IDA member countries. 
Use the filters in the sidebar to customize your view.
""")

    classification_votes = filtered_data.groupby("Member Classification")[
        "Percentage of Total Voting Power"
    ].sum().reset_index()
    fig1 = px.bar(
        classification_votes,
        x="Member Classification",
        y="Percentage of Total Voting Power",
        title="Voting Power by Classification",
        color="Member Classification",
        labels={"Percentage of Total Voting Power": "Total Voting Power (%)"},
        hover_data={"Percentage of Total Voting Power": ":.2f"}  
    )

    st.plotly_chart(fig1)

elif visualization == "Top 10 Members by Voting Power":
    st.subheader("Top 10 Members by Voting Power")
    st.markdown("""
This dashboard provides insights into the Top 10 Member Countries by Voting Power among IDA member countries. 
Use the filters in the sidebar to customize your view.
""")

    top_10_members = filtered_data.nlargest(10, "Percentage of Total Voting Power")
    fig2 = px.bar(
        top_10_members,
        x="Percentage of Total Voting Power",
        y="Member",
        orientation="h",
        title="Top 10 Countries by Voting Power",
        color="Member",
        labels={"Percentage of Total Voting Power": "Voting Power (%)", "Member": "Country"},
    )
    st.plotly_chart(fig2)

elif visualization == "Cumulative Distribution of Votes":
    st.subheader("Cumulative Distribution of Votes")
    st.markdown("""
This dashboard provides insights into the Cumulative Distribution of Votes among IDA member countries. 
Use the filters in the sidebar to customize your view.
""")
    
    filtered_data_sorted = filtered_data.sort_values("Number of Votes")
    filtered_data_sorted["Cumulative Votes"] = filtered_data_sorted["Number of Votes"].cumsum()
    fig3 = px.line(
        filtered_data_sorted,
        x="Member",
        y="Cumulative Votes",
        title="Cumulative Distribution of Votes",
        labels={"Cumulative Votes": "Cumulative Number of Votes", "Member": "Country"},
    )
    st.plotly_chart(fig3)

elif visualization == "Votes vs. Voting Power":
    st.subheader("Votes vs. Voting Power Percentage")
    st.markdown("""
This dashboard provides insights into how the Votes allocated to a Member Country influences its Voting Power (Percentge of Voting Power) among IDA member countries. 
Use the filters in the sidebar to customize your view.
""")
    fig4 = px.scatter(
        filtered_data,
        x="Number of Votes",
        y="Percentage of Total Voting Power",
        title="Votes vs. Voting Power Percentage",
        labels={"Number of Votes": "Number of Votes", "Percentage of Total Voting Power": "Voting Power (%)"},
        color="Member Classification",
    )
    st.plotly_chart(fig4)

elif visualization == "Geographical Distribution":
    st.subheader("Geographical Distribution of Voting Power")
    st.markdown("""
This dashboard provides insights into the Geographical Distribution of Member Countries by Voting Power among IDA member countries. 
Use the filters in the sidebar to customize your view.
""")
    fig5 = px.choropleth(
        filtered_data,
        locations="Member",
        locationmode="country names",
        color="Percentage of Total Voting Power",
        title="Geographical Distribution of Voting Power",
        labels={"Percentage of Total Voting Power": "Voting Power (%)"},
        color_continuous_scale=px.colors.sequential.Plasma,
    )
    st.plotly_chart(fig5)










