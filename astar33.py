from pandas import read_excel
import haversine
from datetime import datetime, date, timedelta, time

# read the data

allCities = read_excel(r'C:\Users\HP\Downloads\Artificial intelligence\Travel-Agent-KB-2-sheets.xlsx',
                       sheet_name='Cities')

allFlights = read_excel(r'C:\Users\HP\Downloads\Artificial intelligence\Travel-Agent-KB-2-sheets.xlsx',
                        sheet_name='Flights')


def heuristic(departure, destination):
    if departure and destination in allCities.values:
        flightofCity = allCities[allCities.City == departure]
        latitude1 = flightofCity['Latitude'].iloc[0]

        flightofCity = allCities[allCities.City == departure]
        longitude1 = flightofCity['Longitude'].iloc[0]

        flightofCity = allCities[allCities.City == destination]
        latitude2 = flightofCity['Latitude'].iloc[0]

        flightofCity = allCities[allCities.City == destination]
        longitude2 = flightofCity['Longitude'].iloc[0]

        departure = (latitude1, longitude1)
        destination = (latitude2, longitude2)
        dist = (haversine.haversine(departure, destination)) / 299792.458

        return dist


def flightTime(arrivalTime, departureTime):
    costTime = datetime.combine(date.today(), arrivalTime) - datetime.combine(date.today(), departureTime)
    secs = costTime.seconds
    minutes = ((secs / 60) % 60) / 60.0
    hours = secs / 3600
    costTime2 = hours + minutes
    return costTime2


def waiting(arrivalTime, departureTime):
    costTime = datetime.combine(date.today(), departureTime) - datetime.combine(date.today(), arrivalTime)
    secs = costTime.seconds
    minutes = ((secs / 60) % 60) / 60.0
    hours = secs / 3600
    wait = hours + minutes
    return wait


def searchopen(list, neighbor):
    for i, x in enumerate(list):
        if neighbor in x:
            return i
    return -1


def searchclosed(list, neighbor):
    if neighbor in list:
        i = list.index(neighbor)
        return i
    else:
        return -1


def Astar(source, destination, startDay, endDay):
    arr = ['sat', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri']
    startDay_indx = arr.index(startDay)
    endDay_indx = arr.index(endDay)

    arr2 = []
    if startDay_indx > endDay_indx:
        for i in range(startDay_indx, len(arr)):
            arr2.append(arr[i])
        for j in range(0, endDay_indx + 1):
            arr2.append(arr[j])
    else:

        for i in range(startDay_indx, endDay_indx + 1):
            arr2.append(arr[i])
    length = len(arr2)
    for i in range(length):
        curDay = arr2[i]
        openl = []
        closed = []
        path = []
        openl.append([[], source, 0, []])  # [[arrival time],source,cost,[flightNum]]

        while len(openl) > 0:
            current = min(openl, key=lambda x: x[2])

            if current[1] == destination:
                flight = current[3].copy()
                path.append(flight)
                break

            openl.remove(current)
            closed.append(current[1])

            for index, row in allFlights.iterrows():
                day = row['List of Days']
                S_city = row['Source']
                if curDay in day and current[1] in S_city:
                    neighbor = allFlights.iloc[index, 1]  # neighbor/destination
                    arrivalTime = allFlights.iloc[index, 3]
                    departureTime = allFlights.iloc[index, 2]  # waiting = dep - arri[in open list]
                    flightNum = allFlights.iloc[index, 4]
                    if len(current[0]) == 0:
                        wait = 0        # at first path
                    else:
                        arrival = current[0][0]
                        wait = waiting(arrival, departureTime)

                    if searchclosed(closed, neighbor) == -1:  # not in closed list

                        neighbor_g = flightTime(arrivalTime, departureTime) + wait
                        f = neighbor_g + heuristic(neighbor, destination)

                        if searchopen(openl, neighbor) == -1:  # not in open list
                            flight = current[3].copy()
                            flight.append(flightNum)
                            openl.append([[arrivalTime], neighbor, f, flight])

                        else:

                            if searchopen(openl, neighbor) != -1:  # in open list
                                indx = searchopen(openl, neighbor)
                                li = openl[indx].copy()  # path in open list
                                costNe = li[2]      # cost in open list
                                if f < costNe:
                                    openl.remove(li)
                                    flight = current[3].copy()
                                    flight.append(flightNum)
                                    openl.append([[arrivalTime], neighbor, f, flight])

        return path


if __name__ == '__main__':
    source = 'Alexandria'
    destination = 'Tokyo'
    startDay = 'sat'
    endDay = 'mon'
    a = Astar(source, destination, startDay, endDay)

    for i in range(len(a)):
        for j in range(len(a[i])):
            flightofCity = allFlights[allFlights["Flight Number"] == a[i][j]]
            s = flightofCity['Source'].iloc[0]
            d = flightofCity['Destination'].iloc[0]
            dt = flightofCity['Departure Time'].iloc[0]
            at = flightofCity['Arrival Time'].iloc[0]
            print("{0}) {1}".format(j + 1, " use flight " + a[i][j] + " from " + s + " to " +
                                    d + ". Departure time " + str(dt) + " and arrival time " + str(at)))



