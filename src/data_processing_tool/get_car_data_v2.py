# %%
import json
from datetime import datetime, timedelta
from urllib.request import urlopen

URL_MAIN    = "https://api.openf1.org/v1/"

def get_session_key(year, country_name, session_name):
    
    session_url = URL_MAIN + f'sessions?country_name={country_name}&session_name={session_name}&year={year}'
    response    = urlopen(session_url)
    data        = json.loads(response.read().decode('utf-8'))
    
    if len(data) == 0:
        
        print('No data available for this session !')
    
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

def get_lap_telemetry(session_key, driver_number, type):
    """
    Retrieve telemetry data for a specific lap of a driver in a racing session.
    
    This function fetches lap telemetry data based on the provided session key,
    driver number, and lap number, and filters the car data to include only the 
    telemetry data relevant to that lap.
    
    Parameters
    ----------
    session_key : str
        The key identifying the session from which telemetry data is requested.
    driver_number : int
        The number assigned to the driver for whom the telemetry data is requested.
    lap_number : int
        The number of the lap for which telemetry data is being retrieved.
    type : str
        The type of telemetry data to extract from the filtered car data (e.g., 'speed', 'throttle').
    
    Returns
    -------
    time : numpy.ndarray
        An array of time values corresponding to the telemetry data samples, 
        normalized to the duration of the lap.
    data_list : list
        A list of telemetry data points filtered by the specified type for the 
        given lap.
    
    Examples
    --------
    >>> time, speeds = get_lap_telemetry('1123', 11, 3, 'speed')
    >>> print(time)
    [0.0, 0.1, 0.2, ..., 60.0]
    >>> print(speeds)
    [12.0, 34.5, 56.3, ..., 78.0]
    
    Notes
    -----
    This function makes HTTP requests to a telemetry data service, and 
    assumes that the service returns data in a specific JSON format. Ensure 
    that the `URL_MAIN` variable is defined and points to the correct API endpoint.
    """
    
    lap_url  = URL_MAIN + f'laps?&session_key={session_key}&driver_number={driver_number}'
    response = urlopen(lap_url)
    data     = json.loads(response.read().decode('utf-8'))
    
    total_laps = max(item["lap_number"] for item in data)
    
    lap_telemetry = {}
    
    for lap_number in range(total_laps + 1):
        
        print(f'Sorting data : lap {lap_number}')
        
        try:
            
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
            
            
            lap_telemetry[lap_number] = filtered_car_data
            print('    - Success !')
        
        except:
            
            print('    - Error !')
    
    return lap_telemetry


#Year
year          = 2024
country_name  = 'Belgium'
session_name  = 'Race'
session_key   = get_session_key(year, country_name, session_name)
driver_number = 11

lap_times     = get_laptimes(session_key, driver_number)
data          = get_lap_telemetry(session_key, driver_number, 'speed')


# %%
