import streamlit as st
from urllib.request import urlopen
import json
import numpy as np
import matplotlib.pyplot as plt 


st.title("F1 Data analytics")

#Year
year = st.selectbox("Select a year", [2023,2024])
response = urlopen(f"https://api.openf1.org/v1/sessions?year={year}")
data = json.loads(response.read().decode('utf-8'))

#Circuit
circuit = [ data[n]["circuit_short_name"] for n in range(len(data))]
seen = set()
specific_item_1 = "Sakhir"  # This item will be kept in two instances if duplicated

circuit_lst = []
for item in circuit:
    if item == specific_item_1:
        # Allow exactly two instances of this specific item
        if circuit_lst.count(item) < 2:
            circuit_lst.append(item)
    elif item not in seen:
        # General case: add the item if it hasn't been seen
        circuit_lst.append(item)
        seen.add(item)

circuit_name = st.selectbox("Select a GP", circuit_lst)
circuit_name_api = circuit_name.replace(" ","+")


#Session
print(circuit_name_api, "\n")
response = urlopen(f"https://api.openf1.org/v1/sessions?circuit_short_name={circuit_name_api}&year={year}")
data = json.loads(response.read().decode('utf-8'))

print("data", data)
session_api = [data[n]["session_name"] for n in range(len(data))]
print(session_api)
session_name = st.selectbox("Select a session",session_api)

for n in range(len(data)):
    if data[n]["session_name"] == session_name:
        session_key = data[n]["session_key"]
    
session_name_api = session_name.replace(" ", "+")
st.write(session_key)






response = urlopen(f'https://api.openf1.org/v1/sessions?circuit_short_name={circuit_name_api}&session_name={session_name_api}&year={year}')
data = json.loads(response.read().decode('utf-8'))


#Driver number
response = urlopen(f"https://api.openf1.org/v1/drivers?session_key={session_key}")
data = json.loads(response.read().decode('utf-8'))
driver_numbers_api = [ data[n]["driver_number"] for n in range(len(data))]
driver_numbers =  st.multiselect("Select driver(s)",driver_numbers_api)

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
            
        else:
            n += 1
        plt.plot(i+1, lap_time_1[i], marker= "o", mfc = mfc, mec = "k")
    index += 1



ax.set(xlabel = "Laps", ylabel = "Laptime [s]", title = f"{circuit_name} Grand Prix, {session_name}, {year}")
plt.legend(driver_numbers)
ax.grid()

st.pyplot(fig)
    