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

#creates client for supabase so can read and input to supabase
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)
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

        # Country: United States
        # Region: New York
        # City: Syracuse
        # ZIP: 13244
        # Latitude: 43.0316, Longitude: -76.1353
        # ISP: Syracuse University
        return data




#time stamp

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
    #??????/ huh
    publicIP = getPublicIp()
    GeoData = getGeoData(publicIP)

    ###why is this a list
    tempTuple = (GeoData['lat'] , GeoData['lon'])
    print(GeoData['lat'], GeoData['lon'])

    points = [
    ]

    points.append(tempTuple)
    ##I think this is supposed to be the current lon and lat of the most recently gotten Location
    ##not a list, might need to restructure or just, add a single value to a list. 


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
def addToDatabase():  
    
    publicIP = getPublicIp()
    GeoData = getGeoData(publicIP)

    ###why is this a list
    tempTuple = (GeoData['lat'] , GeoData['lon'])
    print(GeoData['lat'], GeoData['lon'])

    points = [
    ]

    points.append(tempTuple)
    ##
    

    joined = sortLongLatToLocation(points)
    templist = []
    for state in joined["STATEFP"]:
            templist.append(state)
           # print(state)

    CountyCode = str(joined["COUNTYFP"].iloc[0])  # first county code as string
    StateCode = str(templist[0])                  # first state code

    ##Get Longitude,Latitutde from IP


    #time
    #print(GeoData)


    
    #print(publicIP) #ip
    #print(GeoData) # assocatied data with ip, state, city, isp, long, lat
    CurrentTimestamp = time.time() #time stamp in form of seconds since 
    #print(CurrentTimestamp) # format(Unix Timestamp): 1761968303.5559223 , seconds since January 1, 1970, 00:00:00 UTC


    #Assocaite snake ranked one with "snake bite"
    #only need results, format is for me to look at
    AssocaitedSnakes = GetFormattedSnakeInfo(result)
    #print(AssocaitedSnakes[0])

    #print(result) dict{ID:score}
    FirstKey = list(result.keys())[0]
    #print(FirstKey)

    #permission again
    #need to make it so its more auth users not just one
    
    response = (supabase.from_("SnakeBiteInArea")    .insert({"ID": FirstKey, "CountyID": StateCode+CountyCode, "TimeStamp":CurrentTimestamp, "Longitude": GeoData["lon"], "Latitude": GeoData["lat"], "FIPS":templist[0] })    .execute())
    return (GeoData["lat"], GeoData["lon"]), CurrentTimestamp
    
#to here --------------------------------------------------------------------------------------------------


#addToDatabase()

#Calcuate latest time, the calculate within a 20 mile radius

#JustGotLatLon, JustGotTimeStamp = addToDatabase()
#print(JustGotLatLon)
#(43.0481, -76.1474)
#(43.0316, -76.1353)

#(lon, lat)
JustGotLatLon = (43.0481, -76.1474)
JustGotTimeStamp = 1762009200.56349

#testing section -----------------------------------------
#to find within ten days subtract 864,000 seconds  z = current - (864000) and then do  z<= (anything in between) <= current
def testFunc1(): 
    LastTenDays = JustGotTimeStamp - 864000
    response = (    supabase.table("SnakeBiteInArea")    .select("ID","Longitude", "Latitude","TimeStamp","BiteID") .gte("TimeStamp", LastTenDays) .execute())
    #[{'ID': 1, 'Longitude': -76.1353, 'Latitude': 43.0316, 'TimeStamp': 1762009200.56349}, {'ID': 1, 'Longitude': -76.1353, 'Latitude': 43.0316, 'TimeStamp': 1762010934.52464}]
    data = response.data
    print(response.data)

    coordsListAndBiteID = [(item['Longitude'], item['Latitude'],item['BiteID']) for item in data]
    print(coordsListAndBiteID)
    coordsList = [(lon, lat) for lon, lat, biteID in coordsListAndBiteID]
    #[(-76.1353, 43.0316, 5), (-76.1353, 43.0316, 6), (-76.1353, 43.0316, 7)]
    #print(coordsListAndBiteID[0])
    print(coordsList)
    #[(-76.1353, 43.0316), (-76.1353, 43.0316), (-76.1353, 43.0316)]
#testing section----------------------------------------------

#testFunc1()



#calcaulte location section ---------------------------------------------
# messy version no biteID output
# def calculateLocation(JustGotLatLon):
#     #point1 will need to be a call from supabase, or will need to define it as the long and lat we just got
#     point1 = JustGotLatLon
#     #(43.0481, -76.1474) #syracuse new york

#     LastTenDays = JustGotTimeStamp - 864000
#     response = (    supabase.table("SnakeBiteInArea")    .select("ID","Longitude", "Latitude","TimeStamp", "BiteID") .gte("TimeStamp", LastTenDays) .execute())
#     #[{'ID': 1, 'Longitude': -76.1353, 'Latitude': 43.0316, 'TimeStamp': 1762009200.56349, 'BiteID': 5}, {'ID': 1, 'Longitude': -76.1353, 'Latitude': 43.0316, 'TimeStamp': 1762010934.52464, 'BiteID': 6}, {'ID': 1, 'Longitude': -76.1353, 'Latitude': 43.0316, 'TimeStamp': 1762011193.01539, 'BiteID': 7}]
    

#     data = response.data
  

#     coordsListAndBiteID = [(item['Longitude'], item['Latitude'],item['BiteID']) for item in data]
#     #[(-76.1353, 43.0316, 5), (-76.1353, 43.0316, 6), (-76.1353, 43.0316, 7)]
#     coordsList = [(lat, lon) for lon, lat, biteID in coordsListAndBiteID]
#     #[(-76.1353, 43.0316), (-76.1353, 43.0316), (-76.1353, 43.0316)]
#     print(coordsList)



#     #all Lat,Long within 1-20 miles
#     #will eventually be replaced with points off of database
    
#     # points = [
#     #     (43.0621, -76.1305),
#     #     (43.0358, -76.1609),
#     #     (43.0702, -76.1756),
#     #     (43.0415, -76.1103),
#     #     (43.0549, -76.1401),
#     #     (43.0298, -76.1252),
#     #     (43.0805, -76.1509),
#     #     (43.0502, -76.1708),
#     #     (43.0651, -76.1354),
#     #     (43.0401, -76.1555),
#     #     (35.6764, 139.6500)
#     # ]

#     #lat0, lon0 = 43.0481, -76.1474
#     #JustGotLatLon = (43.0481, -76.1474)
#     lat0, lon0 = JustGotLatLon
#     print(JustGotLatLon)
#     # Create a DataFrame
#     #coordsList = points
#     df = pd.DataFrame(coordsList, columns=['lat', 'lon'])

#     # Vectorized Haversine formula
#     lat_rad = np.radians(df['lat'])
#     lon_rad = np.radians(df['lon'])
#     lat0_rad = np.radians(lat0)
#     lon0_rad = np.radians(lon0)

#     dlat = lat_rad - lat0_rad
#     dlon = lon_rad - lon0_rad
#     a = np.sin(dlat/2)**2 + np.cos(lat0_rad) * np.cos(lat_rad) * np.sin(dlon/2)**2
#     c = 2 * np.arcsin(np.sqrt(a))
#     r = 3956  # Radius of Earth in miles

#     df['distance_miles'] = c * r
#     within_10_miles = df[df['distance_miles'] <= 10]

#     # Filter points within 10 miles (lat,long)
#     coords_within_10 = list(within_10_miles[['lat', 'lon', 'distance_miles']].itertuples(index=False, name=None))
#     #[(43.0621, -76.1305, 1.2889331802821515), (43.0358, -76.1609, 1.088723970948761), (43.0702, -76.1756, 2.0862029497126264), (43.0415, -76.1103, 1.9267182082888692), (43.0549, -76.1401, 0.5967356184350802), (43.0298, -76.1252, 1.6886677225141724), (43.0805, -76.1509, 2.2440213823841115), (43.0502, -76.1708, 1.1895418881573994), (43.0651, -76.1354, 1.3206973663654962), (43.0401, -76.1555, 0.6871404326298617)]
#    # print(coords_within_10)


#     #print(within_10_miles)
#     return coords_within_10



# coords_within_10 = calculateLocation(JustGotLatLon)
# print(coords_within_10)


#output biteID as well
def calculateLocationClean(JustGotLatLon):
    """
    Given a location (lat, lon), find all snake bites in the last 10 days
    within 10 miles. Returns a list of tuples:
    (lat, lon, distance_miles, BiteID)
    """
    lat0, lon0 = JustGotLatLon

    # 10 days ago in Unix timestamp
    LastTenDays = JustGotTimeStamp - 864000

    # Query Supabase for bites in the last 10 days
    response = supabase.table("SnakeBiteInArea")\
        .select("ID", "Longitude", "Latitude", "TimeStamp", "BiteID")\
        .gte("TimeStamp", LastTenDays)\
        .execute()

    data = response.data
    if not data:
        return []

    # Convert to consistent (lat, lon) format
    coordsListAndBiteID = [(item['Latitude'], item['Longitude'], item['BiteID']) for item in data]

    # Create DataFrame
    df = pd.DataFrame(coordsListAndBiteID, columns=['lat', 'lon', 'BiteID'])

    # Haversine formula
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

    # Filter points within 10 miles
    within_10_miles = df[df['distance_miles'] <= 10]

    # Return (lat, lon, distance_miles, BiteID)
    results = list(within_10_miles[['lat', 'lon', 'distance_miles', 'BiteID']].itertuples(index=False, name=None))
    return results


#JustGotLatLon = (43.0481, -76.1474)
#JustGotTimeStamp = 1762009200.56349


#make a function to display the snake county information. 
DataToDisplay = calculateLocationClean(JustGotLatLon)
SnakesToDisplay = [(bite,miles)for lat,lon,miles,bite in DataToDisplay]
#print(SnakesToDisplay)
#[(5, 1.2925663265480423), (6, 1.2925663265480423), (7, 1.2925663265480423), (8, 1.2925663265480423), (9, 1.2925663265480423), (10, 1.2925663265480423)]

def formatSnakeLocationInfo(SnakesToDisplay):
   templist = [(bite)for (bite,miles) in SnakesToDisplay]
  # print(templist)
   for item in templist:
    response = (supabase.table("SnakeBiteInArea")
                .select("*") #, "NewYorkCounties(CountyID, CountyName)")
                .eq("BiteID",item)
                .execute())
    data1 = response.data
    print(data1)
    


formatSnakeLocationInfo(SnakesToDisplay)
#end location area ----------------------------------------------------------------------------------------
