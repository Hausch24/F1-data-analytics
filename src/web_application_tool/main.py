import utils 

#Just for testing
import streamlit as st
import plotly.express as px

st.title("F1 Data Analytics")
st.text("V0.0.1")
st.divider()

year = st.selectbox("Select a year", [2023, 2024])

test = utils.Session(year)

circuit = st.selectbox("Select a Grand Prix", test.get_circuits())
session = st.selectbox("Select a session", test.get_sessions(circuit))
st.write(test.get_session_key(circuit, session))

outlier = st.toggle("Eclude over 120%")


driver_number = st.multiselect("Select a Driver", test.get_drivers())


df = test.get_race_data(driver_number,outlier)
fig = px.line(df, x = "laps", y="lap_time")
st.plotly_chart(fig)