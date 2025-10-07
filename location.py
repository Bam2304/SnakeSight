#Get location using IP Address
#NOTE: use of VPN or iCloud private relay results in manupilation of IP Address
#Users are requested to disable any processes that do the above

import requests

ip_request = requests.get('https://get.geojs.io/v1/ip.json')
ipAdd = ip_request.json()['ip']

url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
geo_request = requests.get(url)
geo_data = geo_request.json()

print('longitude:', geo_data['longitude'])
print('latitude:', geo_data['latitude'])

print('city:', geo_data['city'])
print('region:', geo_data['region'])
print('country:', geo_data['country'])