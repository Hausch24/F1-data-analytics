# %%
import json
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt 
from urllib.request import urlopen

URL_MAIN    = "https://api.openf1.org/v1/"

def get_session_key(year, country_name, session_name):
    
    session_url = URL_MAIN + f'sessions?country_name={country_name}&session_name={session_name}&year={year}'
    response    = urlopen(session_url)
    data        = json.loads(response.read().decode('utf-8'))
    
    if len(data) == 0:
        
        print('No data available !')
    
    return data[0]['session_key']


def get_laptimes(session_key, driver_number):
    
    lap_url  = URL_MAIN + f'laps?&session_key={session_key}&driver_number={driver_number}'
    response = urlopen(lap_url)
    data     = json.loads(response.read().decode('utf-8'))
    
    lap_times = []
    
    for i, lapdata in enumerate(data):
        
        s1_time = lapdata['duration_sector_1']
        s2_time = lapdata['duration_sector_2']
        s3_time = lapdata['duration_sector_3']
        
        # Check for None values
        if s1_time is None or s2_time is None or s3_time is None:
            
            print(f"Skipping lap {i} due to missing data.")
            
            continue
        
        # Convert to float after ensuring values are not None
        s1_time = float(s1_time)
        s2_time = float(s2_time)
        s3_time = float(s3_time)
        
        # Calculate total lap time
        total_time = s1_time + s2_time + s3_time
        lap_times.append(total_time)
    
    return lap_times

def get_lap_telemetry(session_key, driver_number, lap_number, type):
    
    lap_url  = URL_MAIN + f'laps?&session_key={session_key}&driver_number={driver_number}&lap_number={lap_number}'
    response = urlopen(lap_url)
    data     = json.loads(response.read().decode('utf-8'))
    
    current_lap_start    = data[0]['date_start']
    current_lap_duration = data[0]['lap_duration']
    
    lap_start_time = datetime.fromisoformat(current_lap_start)
    lap_end_time   = lap_start_time + timedelta(seconds=current_lap_duration)
    
    
    car_url  = URL_MAIN + f'car_data?&session_key={session_key}&driver_number={driver_number}'
    response = urlopen(car_url)
    car_data = json.loads(response.read().decode('utf-8'))
    
    
    filtered_car_data = []
    
    for entry in car_data:
        
        entry_date = datetime.fromisoformat(entry["date"])
        
        if lap_start_time <= entry_date <= lap_end_time:
            
            filtered_car_data.append(entry)
    
    data_list = []
    
    for sample in filtered_car_data:
        
        data_list.append(sample[type])
    
    time = np.linspace(0, float(current_lap_duration), len(data_list))
    
    return time, data_list







#Year
year          = 2024
country_name  = 'Belgium'
session_name  = 'Race'
session_key   = get_session_key(year, country_name, session_name)
driver_number = 11
lap_number    = 30

lap_times     = get_laptimes(session_key, driver_number)
time, data    = get_lap_telemetry(session_key, driver_number, lap_number, 'speed')


# plt.plot(lap_times)



plt.plot(time, data)
# %%
