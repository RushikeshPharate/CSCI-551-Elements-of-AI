#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name IU ID
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
import math
from queue import PriorityQueue
from math import radians, cos, sin, asin, sqrt, pi, tanh
import numpy as np

#This Function is used to find latitude and longitude of given city
def pos(cityname3):
    f = open("city-gps.txt", 'r')
    for xa in f:
        city, lat, lon = xa.split(' ')
        if city == cityname3:

            lon1 = lon.split('\n')
            lonf = lon1[0]
            latf1 = float(lat)
            lonf1 = float(lonf)
            return latf1, lonf1
        # else:
        #     return 0,0



#This Function is used to find latitude and longitude of nodes not present in city_gps file
def notpos(cityname2, fileq):
    filex = fileq

    list5 = []
    list6 = []
    list5 = FindNeighbours(cityname2, filex)         #Here we are finding the Neighbours of the city
    for i in list5[0]:
        list6.append(pos(i))

    avglt = 0
    avgln = 0
    k = 0                                            #We are then assingning Average Values of lat and lon of neighbours to city
    for j in list6:
        if j != None:
            avglt = j[0]+avglt
            avgln = j[1]+avgln
        else:
            k = k+1
    if len(list6)-k != 0:
        avglt = avglt/(len(list6)-k)
        avgln = avgln/(len(list6)-k)
    return avglt, avgln                              #Returning average latitude and Longitutde

#This Function is used to calculate Haversine Distance Between 2 Nodes
def distance1(lat1, lon1, lat2, lon2):
### I have Referred this website to Calculate Haversine Distance= "https://towardsdatascience.com/heres-how-to-calculate-distance-between-2-geolocations-in-python-93ecab5bbba4"
    r = 3958.8
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2-lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * \
        np.cos(phi2) * np.sin(delta_lambda / 2)**2
    res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
    return np.round(res, 2)



def hssegment(trancity, goalcityq,file):

## I have discussed with My Friend Karan Gupta for this part hssegment function to find heuristic for segment
    qp = file
    zxnext = []
    nextcity = []
    cost = 1
    k = 0
    visitedl = []
    visitedl.append(trancity)
    zxnext, q, w, e = FindNeighbours(trancity, qp)
    while len(zxnext) > 0:
        zxcurr = zxnext
        zxnext = []
        for node in zxcurr:
            if node == goalcityq:
                return cost
            elif node in visitedl:
                pass
            else:
                nextcity, s, t, u = FindNeighbours(node, qp)
                for city in nextcity:
                    visitedl.append(node)
                    zxnext.append(city)

        cost = cost+1
    return


#This is the Function Used to Calculate Neighbours of the given City
def FindNeighbours(cityname, file):
    filec = file
    negb = []
    distance2 = []
    speedm = []
    hw = []
    for i in filec:
        if i[0] == cityname:              #This Searches city in file and stores Neighbours,Distance,Speed,Highway
            negb.append(i[1])
            distance2.append(i[2])
            speedm.append(i[3])
            hw.append(i[4])

    return negb, distance2, speedm, hw


def get_route(start, end, cost):
    routesbtct = []
    chekl = []
    r = 1
    goalcity = end
    fringe = PriorityQueue()           #We are using Priority Queue For Implementation as Fringe which will pop according to minimum key
    f = open("road-segments.txt", 'r')
    for line in f:
        city1, city2, dist, spd, hw = line.split(' ')
        hw1 = hw.split('\n')
        routesbtct.append((city1, city2, float(dist), float(spd), hw1[0]))
        routesbtct.append((city2, city1, float(dist), float(spd), hw1[0]))
    f1 = open("city-gps.txt", 'r')
    for line in f1:
        city, lat, lon = line.split(' ')
        chekl.append(city)

    intialcity = start
    s = {}
    p = []
    f1 = cost
    list1 = []
    sp = []
    dist = []
    adj = []
    hw = []
    list5 = []
    Expect1 = 0
    final = []
    loop = 99
    fringe.put((0, ([(intialcity, 0, "")], 0, 0, 0)))
    lat2, lon2 = pos(goalcity)
    list8 = []
    Expect2 = 0

    while loop != 0:
        (key, (paths, d, t, Expect1)) = fringe.get()
        city1 = paths[-1]
        adj, dist, sp, hw = FindNeighbours(city1[0], routesbtct)     #Here we are Finding Neighbours
        for i in range(len(adj)):
            for j in range(len(paths)):
                list8.append(paths[j][0])
            if adj[i] not in list8:
                a1 = []
                for opt in paths:
                    a1.append(opt)
                a1.append((adj[i], dist[i], hw[i]))
                if a1[-1][0] in chekl:
                    lat1, lon1 = pos(a1[-1][0])               #Calculating Latitude and Longitude of given city
                else:
                    lat1, lon1 = notpos(a1[-1][0], routesbtct)  #If node is not present in city_gps file it is calculating Average lon,lat

                dhur = distance1(lat1, lon1, lat2, lon2)      #Getting Haversine Distance
                if dhur == 0:
                    try:
                        lat1, lon1 = pos(a1[-2][0])
                    except:
                        lat1, lon1 = notpos(a1[-2][0], routesbtct)
                    dhur = distance1(lat1, lon1, lat2, lon2)

                if sp[i] == 50 or sp[i] > 50:                  #If Speed is greater or equal to 50
                    p = tanh(dist[i] / 1000)
                else:
                    p = 0
                Expect2 = (dist[i] / sp[i]) + (p * 2 * ((dist[i] / sp[i])+Expect1))+Expect1     #Delivery Formula

                tf = t+dist[i]/sp[i]
                df = float(d+dist[i])
                Expectn = Expect1+(dist[i]/sp[i])+dhur/sp[i]

                tn = 0
                tn = t + ((dist[i]/sp[i]) + (dhur/65))
                dn = 0
                dn = df+dhur
                if f1 == 'time':                                    #cost Function
                    fringe.put((tn, (a1, df, tf, Expect2)))
                elif f1 == 'distance':
                    fringe.put((dn, (a1, df, tf, Expect2)))
                elif f1 == 'segments':
                    hsos = hssegment(a1[-1][0], goalcity,routesbtct)
                    fringe.put((len(a1)-1+hsos, (a1, df, tf, Expect2)))
                elif f1 == 'delivery':
                    fringe.put((tn+Expect2, (a1, df, tf, Expect2)))

                list1 = [x for x, _, _ in a1]
                visited = []
                visited.append(list1)

                r = r+1
                if goalcity in list1:
                    final.append(a1)
                    dirc = []
                    k = 1
                    diqf = 0
                    for j in range(len(a1)-1):
                        dirc.append(
                            (a1[k][0], a1[k][2]+" for %f miles" % a1[k][1]))
                        diqf = a1[k][1]+diqf
                        k = k+1
                    return {"total-segments": len(a1)-1,
                            "total-miles": df,
                            "total-hours": tf,
                            "total-delivery-hours": Expect2,
                            "route-taken": dirc}

    return -1


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


