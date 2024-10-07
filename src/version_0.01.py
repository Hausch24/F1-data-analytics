# %%
import json
import numpy as np
import matplotlib.pyplot as plt 
from urllib.request import urlopen


#Year
year     = 2024





response = urlopen(f"https://api.openf1.org/v1/sessions?year={year}")
data     = json.loads(response.read().decode('utf-8'))

#Circuit
circuit = [ data[n]["circuit_short_name"] for n in range(len(data))]

def keep_unique_w_order(list):
    
    seen     = set()
    new_list = []
    
    for item in list:
        
        if item not in seen:
            
            new_list.append(item)
            seen.add(item)
    
    return new_list

circuit_lst = keep_unique_w_order(circuit)


circuit_name = circuit_lst[0]
circuit_name_api = circuit_name.replace(" ","+")

#Session
response = urlopen(f"https://api.openf1.org/v1/sessions?circuit_short_name={circuit_name_api}&year={year}")
data = json.loads(response.read().decode('utf-8'))

session_api = [data[n]["session_name"] for n in range(len(data))]

session_api = keep_unique_w_order(session_api)
session_name = session_api[-1]

for n in range(len(data)):
    
    if data[n]["session_name"] == session_name:
        
        session_key = data[n]["session_key"]  

session_name_api = session_name.replace(" ", "+")
response = urlopen(f'https://api.openf1.org/v1/sessions?circuit_short_name={circuit_name_api}&session_name={session_name_api}&year={year}')
data = json.loads(response.read().decode('utf-8'))

#Driver number
response = urlopen(f"https://api.openf1.org/v1/drivers?session_key={session_key}")
data = json.loads(response.read().decode('utf-8'))
driver_numbers_api = [ data[n]["driver_number"] for n in range(len(data))]
driver_numbers = driver_numbers_api[0:3]



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


while index < len(driver_numbers):
    
    print(driver_numbers[index])
    
    lap_time       = lap_time_compare(driver_numbers[index])
    tires, lap_end = tire_data(driver_numbers[index])
    lap_time[0]    = lap_time[1]
    
    lap_end        = [n-1 for n in lap_end]
    
    n = 0
    laps = [n+1 for n in range(len(lap_time))]
    plt.plot( laps , lap_time, linestyle = "-" )
    
    for i in range(len(lap_time)):
        
        if i <= lap_end[n]:
            
            mfc = get_marker(tires[n])
        
        else:
            n += 1
        
        plt.plot(i+1, lap_time[i], marker= "o", mfc = mfc, mec = "k")
    
    index += 1



#plt.set(xlabel = "Laps", ylabel = "Laptime [s]", title = f"{circuit_name} Grand Prix, {session_name}, {year}")
plt.legend(driver_numbers)
plt.grid()
plt.show()



# %%
