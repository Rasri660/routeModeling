import time
from django.contrib.gis.geos import Point
from googlemaps import Client
from datetime import datetime

mapService = Client('AIzaSyCy-F7kcigXdHaaAIFSH8DlfKe1Dl-aJOM')

#Loop through locations and fetch routes between all OD-pairs
def getGoogleRoutes(vmidList, locationList, time_period):

    test_time = datetime(2016,9,6,6,30,0)
    routes = []
    for odPair in vmidList:
        for zone in locationList:
            if odPair[1] == zone[0]:
                #start = zone[0]
                x = [zone[1], zone[2]]
            if odPair[2] == zone[0]:
                #end = zone[0]
                y = [zone[1], zone[2]]


        directions = mapService.directions(x, y, 'driving', None, True, None, None, None, None, test_time)

    #Add Each step of each route of each OD-pair
        for routeIndex, route in enumerate(directions):
            for stepIndex, step in enumerate(route['legs'][0]['steps']):
                data = {'od_id': odPair[0],
                        'route_id': str(odPair[0]) + ':' + str(routeIndex + 1) + ':' + str(time_period),
                        'start_point': Point(step['start_location']['lng'], step['start_location']['lat']).wkt,
                        'end_point': Point(step['end_location']['lng'], step['end_location']['lat']).wkt,
                        'route_index': routeIndex + 1,
                        'step_index': stepIndex + 1,
                        'travel_time': step['duration']['value'],
                        'distance': step['distance']['value'],
                        'time_period': time_period,
                        'start_time': test_time,
                        'date_inserted': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }

                routes.append(data)

    return routes
