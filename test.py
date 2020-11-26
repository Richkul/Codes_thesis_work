'''
*Version: 1.0 Published: 2020/02/11* Source: [NASA POWER](https://power.larc.nasa.gov/)
POWER API Multipoint Download (CSV)
This is an overview of the process to request data from multiple data points from the POWER API.
'''

import os, sys, time, json, urllib3, requests, multiprocessing

urllib3.disable_warnings()

import numpy as np
import pandas as pd

def Downloading(Collection):

    query_url, file_path = Collection

    main_response = requests.get(url=query_url, verify=False)
    json_response = json.loads(main_response.text)

    df = pd.DataFrame.from_dict(json_response['features'][0]['properties']['parameter'])
    df.to_csv(file_path)

class Process():

    def __init__(self):

        self.processes = 10 # Please do not go more than 10 concurrent requests.

        self.query_url = r"https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py?request=execute&identifier=SinglePoint&tempAverage=DAILY&parameters=T2M,RH2M&startDate=19810101&endDate=20191231&lat={latitude}&lon={longitude}&outputList=JSON&userCommunity=SSE"
        self.file_path = "File_Lat_{latitude}_Lon_{longitude}.csv"

        self.messages = []
        self.times = {}

    def execute(self):

        Start_Time = time.time()

        Latitudes = np.arange(3.67184, 27.00479,2) # Update your download extent.
        Longitudes = np.arange(-25.39395, 14.81601,2) # Update your download extent.

        print ("Longitudes:", len(Longitudes))
        print ("Latitudes:", len(Latitudes))
        print ("Points:", len(Longitudes) * len(Latitudes))

        Points = []
        for Longitude in Longitudes:
            for Latitude in Latitudes:
                each_query_url = self.query_url.format(longitude=Longitude, latitude=Latitude)
                each_file_path = self.file_path.format(longitude=Longitude, latitude=Latitude)
                Points.append((each_query_url, each_file_path))

        pool = multiprocessing.Pool(self.processes)
        x = pool.imap_unordered(Downloading, Points)
        dfs = []
        for i, df in enumerate(x, 1):
            dfs.append(df)
            sys.stderr.write('\rExporting {0:%}'.format(i/len(Points)))

        self.times["Total Script"] = round((time.time() - Start_Time), 2)

        print ("\n")
        print ("Total Script Time:", self.times["Total Script"])

if __name__ == '__main__':
    Process().execute()