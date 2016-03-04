
from googlemaps import Client
from pygeocoder import Geocoder
import json

mapService = Client('AIzaSyCy-F7kcigXdHaaAIFSH8DlfKe1Dl-aJOM')
geocoder = Geocoder()

lnglat_start = geocoder.reverse_geocode(59.3831483, 18.0303761)
lnglat_end = geocoder.reverse_geocode(59.3657481,18.0090901)

test1 = geocoder.geocode('Hjortstigen 1, 170 71 Solna')
test2 = geocoder.geocode('Terminalvägen 11, 171 73 Solna')

directions = mapService.directions(
    test1.coordinates,
    test2.coordinates,
    'driving', None, True
)

print('start:', test1.coordinates, ' end: ', test2.coordinates)
for routeIndex, route in enumerate(directions):
    print('Route: ', routeIndex + 1)

    for step in route['legs'][0]['steps']:
        print(step['start_location'], step['distance'], step['duration'])
