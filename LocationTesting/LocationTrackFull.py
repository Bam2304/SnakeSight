
##EVERYONE BUT ME DO NOT RUN
##IT WILL ADD DUMMY DATA TO DATABASE
##DONT RUN IT
#Get ip 
##Get Timestamp
import requests
import socket
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import import_ipynb
from ResultsPageOutPutData import GetFormattedSnakeInfo, result
import supabase
import time
import os
from shapely.geometry import Point
import geopandas as gpd
from supabase import create_client, Client

#idk bruh leave it


def getPublicIp():
        # Get hostname and local IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
       # print(f"Hostname: {hostname}")
       # print(f"Local IP Address: {local_ip}")

        # Get public IP
        response = requests.get("https://api.ipify.org?format=json")
        public_ip = response.json()["ip"]
        #print(f"Public IP Address: {public_ip}")
        return public_ip
    

def getGeoData(ip):
        # Use a free IP geolocation API
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        # print()
        # print(f"Country: {data['country']}")
        # print(f"Region: {data['regionName']}")
        # print(f"City: {data['city']}")
        # print(f"ZIP: {data['zip']}")
        # print(f"Latitude: {data['lat']}, Longitude: {data['lon']}")
        # print(f"ISP: {data['isp']}")
        return data




#time stamp

#to find within ten days subtract 864,000 seconds  z = current - (864000) and then do  z<= (anything in between) <= current
#in progress for future...
def getPhoneIP():
    url = "https://jsonip.com/"


    # Send GET request
    response = requests.get(url)

    # Convert the response to JSON
    data = response.json()

    # Print the JSON data
    print(data)
    return data["ip"]

# PhoneIP = getPhoneIP()
# acquirePhoneIP = getGeoData(PhoneIP)

def sortLongLatToLocation(points):

    counties = gpd.read_file("tl_2025_us_county.zip")


    # Example list of lat/lon points
    # will be a list of long lat points from database in the future
    points = [
        (43.0621, -76.1305),
        (43.0358, -75.1609),
        (43.0702, -76.1756),
    ]

    # Create DataFrame
    df = pd.DataFrame(points, columns=["lat", "lon"])

    # Convert to GeoDataFrame
    gdf_points = gpd.GeoDataFrame(
        df,
        geometry=[Point(xy) for xy in zip(df.lon, df.lat)],
        crs="EPSG:4326"  # WGS84 coordinate system
    )

    counties = counties.to_crs("EPSG:4326")


    # Perform spatial join
    joined = gpd.sjoin(gdf_points, counties, how="left", predicate="within")
    return joined
    # Show results
    print(joined[["lat", "lon", "NAME", "STATEFP", "COUNTYFP"]])

    
#testing defining county and state codes to add to database
    
#Make into a function from here ------------------------------------------------------------
points = [
    (43.0621, -76.1305),
    (43.0358, -75.1609),
    (43.0702, -76.1756),
]
joined = sortLongLatToLocation(points)
templist = []
for state in joined["STATEFP"]:
        templist.append(state)
        print(state)



##Get Longitude,Latitutde from IP


#time
#print(GeoData)

publicIP = getPublicIp()
GeoData = getGeoData(publicIP)
print(publicIP) #ip
print(GeoData) # assocatied data with ip, state, city, isp, long, lat
CurrentTimestamp = time.time() #time stamp in form of seconds since 
print(CurrentTimestamp) # format(Unix Timestamp): 1761968303.5559223 , seconds since January 1, 1970, 00:00:00 UTC


#Assocaite snake ranked one with "snake bite"
#only need results, format is for me to look at
AssocaitedSnakes = GetFormattedSnakeInfo(result)
#print(AssocaitedSnakes[0])

#print(result)
FirstKey = list(result.keys())[0]
#print(FirstKey)

#permission again
#need to make it so its more auth users not just one
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

#response = (supabase.from_("SnakeBiteInArea")    .insert({"ID": FirstKey, "CountyID": "36045", "TimeStamp":CurrentTimestamp, "Longitude": GeoData["lon"], "Latitude": GeoData["lat"], "FIPS":templist[0] })    .execute())

#to here --------------------------------------------------------------------------------------------------
#have it return lon and lat of just sorted snake

##Return Snake bites in 20 mile radius?, return name of current county, 



def calculateLocation():
    #point1 will need to be a call from supabase, or will need to define it as the long and lat we just got
    point1 = (43.0481, -76.1474) #syracuse new york



    #all Lat,Long within 1-20 miles
    print()

    #will eventually be replaced with points off of database
    points = [
        (43.0621, -76.1305),
        (43.0358, -76.1609),
        (43.0702, -76.1756),
        (43.0415, -76.1103),
        (43.0549, -76.1401),
        (43.0298, -76.1252),
        (43.0805, -76.1509),
        (43.0502, -76.1708),
        (43.0651, -76.1354),
        (43.0401, -76.1555),
        (35.6764, 139.6500)
    ]

    lat0, lon0 = 43.0481, -76.1474
    # Create a DataFrame
    df = pd.DataFrame(points, columns=['lat', 'lon'])

    # Vectorized Haversine formula
    lat_rad = np.radians(df['lat'])
    lon_rad = np.radians(df['lon'])
    lat0_rad = np.radians(lat0)
    lon0_rad = np.radians(lon0)

    dlat = lat_rad - lat0_rad
    dlon = lon_rad - lon0_rad
    a = np.sin(dlat/2)**2 + np.cos(lat0_rad) * np.cos(lat_rad) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 3956  # Radius of Earth in miles

    df['distance_miles'] = c * r

    # Filter points within 10 miles (lat,long)
    within_10_miles = df[df['distance_miles'] <= 10]

    print(within_10_miles)



