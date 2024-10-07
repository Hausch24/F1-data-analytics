 #%%
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

def keep_unique_w_order(list):
    seen = set()
    new_list = []
    for item in list:
        if item not in seen:
            new_list.append(item)
            seen.add(item)
    return new_list

circuit_lst = keep_unique_w_order(circuit)


circuit_name = st.selectbox("Select a GP", circuit_lst)
circuit_name_api = circuit_name.replace(" ","+")

#Session
response = urlopen(f"https://api.openf1.org/v1/sessions?circuit_short_name={circuit_name_api}&year={year}")
data = json.loads(response.read().decode('utf-8'))

session_api = [data[n]["session_name"] for n in range(len(data))]

session_api = keep_unique_w_order(session_api)
session_name = st.selectbox("Select a session",session_api)

for n in range(len(data)):
    if data[n]["session_name"] == session_name:
        session_key = data[n]["session_key"]  
st.write(session_key)

outliers = st.checkbox("Remove outliers")

#Driver number
response = urlopen(f"https://api.openf1.org/v1/drivers?session_key={session_key}")
data = json.loads(response.read().decode('utf-8'))
driver_numbers_api = [ data[n]["driver_number"] for n in range(len(data))]
driver_numbers =  st.multiselect("Select driver(s)",driver_numbers_api)


def lap_time_compare(driver_number):
    response = urlopen(f'https://api.openf1.org/v1/laps?session_key={session_key}&driver_number={driver_number}')
    data = json.loads(response.read().decode('utf-8'))
    lap_time = [data[n]["lap_duration"] for n in range(len(data))]
    lap_time = [0 if item is None else item for item in lap_time]
    return (lap_time)

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

#%%
while index < len(driver_numbers):
    print(driver_numbers[index])
    lap_time = lap_time_compare(driver_numbers[index])
    tires, lap_end = tire_data(driver_numbers[index])
    lap_time[0]=lap_time[1]
    lap_end = [n-1 for n in lap_end]
    
    if outliers:
        for n in range(1, len(lap_time)):
            if lap_time[n] >= ((sum(lap_time[0:n])/n) * 1.2):
                lap_time[n] = 0


    filtered_lap_time = []
    filtered_laps = []
    lap_counter = 1

    for time in lap_time:
        # If it's not an outlier, append the lap time and lap counter for plotting
        if time != 0:
            filtered_lap_time.append(time)
            filtered_laps.append(lap_counter)
        
        # Always increment the lap counter regardless of whether it's an outlier
        if time == 0:
            lap_counter += 2  # Increment by 2 when there's an outlier
        else:
            lap_counter += 1
    
    

    print("laptime :",len(lap_time), lap_time, "\nlaps :", len(filtered_laps), filtered_laps)


    #Plot lines
    ax.plot( filtered_laps , filtered_lap_time, linestyle = "-" )

    lap_end.insert(0,1)

    n = 0
    for i in range(lap_end[n],lap_end[n+2]):
        print("i:" , i , "\n lap end: ", range(lap_end[n],lap_end[n+2]))
        if i == filtered_laps[i-1]:
            print("megy")
            mfc = get_marker(tires[n])

        else:
            n += 1
    
        plt.plot(i, filtered_lap_time[i], marker= "o", mfc = "mfc", mec = "k")

    index +=1   



ax.set(xlabel = "Laps", ylabel = "Laptime [s]", title = f"{circuit_name} Grand Prix, {session_name}, {year}")
plt.legend(driver_numbers)
ax.grid()

st.pyplot(fig)
    
# %%
