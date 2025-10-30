import requests
import socket


def getPublicIp():
    try:
        # Get hostname and local IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Hostname: {hostname}")
        print(f"Local IP Address: {local_ip}")

        # Get public IP
        response = requests.get("https://api.ipify.org?format=json")
        public_ip = response.json()["ip"]
        print(f"Public IP Address: {public_ip}")
        return public_ip
    except Exception as e:
        print("Error getting IP:", e)
        return None

def getGeoData(ip):
    try:
        # Use a free IP geolocation API
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            print(f"Country: {data['country']}")
            print(f"Region: {data['regionName']}")
            print(f"City: {data['city']}")
            print(f"ZIP: {data['zip']}")
            print(f"Latitude: {data['lat']}, Longitude: {data['lon']}")
            print(f"ISP: {data['isp']}")
        else:
            print("Could not fetch geolocation data.")
    except Exception as e:
        print("Error fetching geolocation:", e)

publicIP = getPublicIp()
GeoData = getGeoData(publicIP)

def getPhoneIP():
    url = "https://api.iplocation.net/?ip=" + publicIP ##idk
    ##gotta test this, not sure how to make work without wifi connection
    ##logically I think it does


    # Send GET request
    response = requests.get(url)

    # Convert the response to JSON
    data = response.json()

    # Print the JSON data
    print(data)
    return data["ip"]

PhoneIP = getPhoneIP()
acquirePhoneIP = getGeoData(PhoneIP)
