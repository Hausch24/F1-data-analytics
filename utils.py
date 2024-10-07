import json
from urllib.request import urlopen
import plotly.express as px
from datetime import datetime
import pandas as pd

URL_MAIN    = "https://api.openf1.org/v1/"



class GrandPrix:
    def __init__(self, year):
        self.year = year

    def get_circuits(self):

        session_url = URL_MAIN + f"sessions?year={self.year}"
        try:
            response    = urlopen(session_url)
            self.session_data        = json.loads(response.read().decode('utf-8'))

            if len(self.session_data) == 0:
                print(f"No data available for this season: {self.year}")

        except Exception as e:
            print(f"Error fetching data for {self.year}: {e}")

        #Circuits
        circuits = [self.session_data[n]["circuit_short_name"] for n in range(len(self.session_data))]

        #Remove duplicates
        circuits = list(dict.fromkeys(circuits))
        self.circuits_api = [ n.replace(" ","+") for n in circuits]
        return self.circuits_api

    def get_sessions(self,circuit):
        
        session_api = [self.session_data[n]["session_name"] for n in range(len(self.session_data)) if self.session_data[n]["circuit_short_name"] == circuit]
        session_api = list(dict.fromkeys(session_api))

        print(session_api)
        return(session_api)
    
    def get_session_key(self, circuit, session_api):

        for n in range(len(self.session_data)):
            if self.session_data[n]["session_name"] == session_api and self.session_data[n]["circuit_short_name"] == circuit:
                self.session_key = self.session_data[n]["session_key"]

        print("Session key: " ,self.session_key)
        return self.session_key
    
    def get_drivers(self):

        url = URL_MAIN + f"drivers?session_key={self.session_key}"
        try:
            response    = urlopen(url)
            data        = json.loads(response.read().decode('utf-8'))

            if len(data) == 0:
                print(f"No data available for this session: {self.session_key}")

        except Exception as e:
            print(f"Error fetching data for {self.session_key}: {e}")

        driver_number = [ data[n]["driver_number"] for n in range(len(data))]
        print(driver_number)
        return driver_number

class Session(GrandPrix):

    def __init__(self, year):
        super().__init__(year)
        

    def get_lap_data(self,driver_number):

        self.driver_number = driver_number[0]
        print(self.driver_number)
        lap_url  = URL_MAIN + f'laps?&session_key={self.session_key}&driver_number={self.driver_number}'
        try:
            response    = urlopen(lap_url)
            data        = json.loads(response.read().decode('utf-8'))

            if len(data) == 0:
                print(f"No data available for this session: {self.session_key}")

        except Exception as e:
            print(f"Error fetching data for {self.session_key}: {e}")

        s1 = [data[n]["duration_sector_1"] for n in range(len(data))]
        s2 = [data[n]["duration_sector_2"] for n in range(len(data))]
        s3 = [data[n]["duration_sector_3"] for n in range(len(data))]

        lap_time = [data[n]["lap_duration"] for n in range(len(data))]
        lap_time[0] = lap_time[1]
        print("lap time", lap_time)
        print(f"length of laptime:{len(lap_time)} ")
        
        laps = list(range(1,len(lap_time)+1))
        
        outlier = True
    
        if outlier:
            for n in range(1, len(lap_time)):
                if lap_time[n] >= ((sum(lap_time[0:n])/n) * 1.2):
                    lap_time[n] = 0

        for n in range(len(lap_time) - 1, -1, -1):
            if lap_time[n] == 0:
                del lap_time[n]
                del laps[n]

        print(len(lap_time), "\n", len(laps))
        print(laps)
        
        df = pd.DataFrame({"laps" : laps, "lap_time" : lap_time})
        fig = px.line(df, x = "laps", y="lap_time")
        fig.show()

        segment_s1 = [data[n]["segments_sector_1"] for n in range(len(data))]
        segment_s2 = [data[n]["segments_sector_2"] for n in range(len(data))]
        segment_s3 = [data[n]["segments_sector_3"] for n in range(len(data))]

        

    def get_race_control(self):

        race_control_url  = URL_MAIN + f'race_control?&session_key={self.session_key}'
        try:
            response    = urlopen(race_control_url)
            data        = json.loads(response.read().decode('utf-8'))

            if len(data) == 0:
                print(f"No data available for this session: {self.session_name}")

        except Exception as e:
            print(f"Error fetching data for {self.session_name}: {e}")

        print(data)

    def get_weather_data(self):

        weather_url  = URL_MAIN + f'weather?&session_key={self.session_key}'
        try:
            response    = urlopen(weather_url)
            data        = json.loads(response.read().decode('utf-8'))

            if len(data) == 0:
                print(f"No data available for this session: {self.session_name}")

        except Exception as e:
            print(f"Error fetching data for {self.session_name}: {e}")

        self.times = [datetime.fromisoformat(n['date']) for n in data]
        self.air_temp = [n['air_temperature'] for n in data]
        self.track_temp = [n['track_temperature'] for n in data]
        self.humidity = [n['humidity'] for n in data]
        self.rainfall  = [n['rainfall'] for n in data]
        self.wind_direction = [n['wind_direction'] for n in data]
        self.wind_speed = [n['wind_speed'] for n in data]
        print("megérkezet")
