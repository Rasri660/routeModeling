import math

def getRouteShares(routes):
    nmbrRoutes = len(routes)

    utilities = getUtilityFunctions(routes)
    shares = calculateRouteShares(utilities)
    return shares

def getUtilityFunctions(routes):
    beta = [0.5, 0.5]
    utilities = []
    beta
    for route in routes:
        travel_time = route[4]/3600
        distance = route[5]/1000
        utilities.append((beta[0] * travel_time) + (beta[1] * distance))

    return(utilities)

def calculateRouteShares(utilities):
    exp = []
    shares = []
    den = 0
    math.exp(0.828)
    for i in utilities:
        exp.append(math.exp(i))
        den = den + math.exp(i)

    for e in exp:
         shares.append(e/den)

    return shares
