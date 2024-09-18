import streamlit as st
from urllib.request import urlopen
import json
import numpy as np
import matplotlib.pyplot as plt 


st.title("F1 Data analytics")
year = st.selectbox("Select a year", [2023,2024])
country_name = st.selectbox("Select a GP",["Bahrain","Spain","Hungary"])
session_name = st.selectbox("Select a session",["Race","Qualifying"])
if year == 2023:
    driver_numbers = st.multiselect("Select driver(s)", [1,16,81])
else:
    driver_numbers = st.multiselect("Select driver(s)", [44,11,63])

response = urlopen(f'https://api.openf1.org/v1/sessions?country_name={country_name}&session_name={session_name}&year={year}')
data = json.loads(response.read().decode('utf-8'))

st.write(data[0]["session_key"])
session_key = data[0]["session_key"]

def lap_time_compare(driver_number):
    response = urlopen(f'https://api.openf1.org/v1/laps?session_key={session_key}&driver_number={driver_number}')
    data = json.loads(response.read().decode('utf-8'))
    lap_time_1 = [data[n]["lap_duration"] for n in range(len(data))]
    return (lap_time_1)

def tire_data(driver_number):
    response = urlopen(f'https://api.openf1.org/v1/stints?session_key={session_key}&driver_number={driver_number}')
    data = json.loads(response.read().decode('utf-8'))
    tires = [data[n]["compound"] for n in range(len(data))]
    lap_end = [data[n]["lap_end"] for n in range(len(data))]
    return (tires, lap_end)

def get_marker(tires):
    if tires == "SOFT":
        return "r"
    elif tires == "MEDIUM":
        return 'y'
    elif tires == "HARD":
        return 'w'
    elif tires == "INTERMEDIATE":
        return 'g'
    elif tires == "WET":
        return 'b'
    
#Lap time compare
index = 0
fig, ax = plt.subplots()


while index < len(driver_numbers):
    print(driver_numbers[index])
    lap_time_1 = lap_time_compare(driver_numbers[index])
    tires, lap_end = tire_data(driver_numbers[index])
    lap_time_1[0]=lap_time_1[1]
    lap_end = [n-1 for n in lap_end]

    n = 0
    laps = [n+1 for n in range(len(lap_time_1))]
    ax.plot( laps , lap_time_1, linestyle = "-" )

    for i in range(len(lap_time_1)):
        if i <= lap_end[n]:
            mfc = get_marker(tires[n])
            print(tires)
        else:
            n += 1
        plt.plot(i+1, lap_time_1[i], marker= "o", mfc = mfc, mec = "k")
    index += 1



ax.set(xlabel = "Laps", ylabel = "Laptime [s]", title = f"{country_name} Grand Prix, {session_name}, {year}")
plt.legend(driver_numbers)
ax.grid()

st.pyplot(fig)
    