#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import time
from typing import List
import requests
import configparser
from types import SimpleNamespace
from flightData import flightData
from flightDataDisplayer import FlightDataDisplayer
from localInfoData import LocalInfoData

class flightDisplayMain:

    def __init__(self):
        self.api_url_base = ""
        self.api_url_baseFormat = "https://admin.zweef.app/club/{0}/api/"
        self.headers = ""
        self.enableDisplay = False
        self.display = FlightDataDisplayer()


    def __get_flight_info(self):
    
        flightList = []
        api_url = '{0}flights.json'.format(self.api_url_base)

        response = requests.get(api_url, headers=self.headers)

        print(api_url)

        if response.status_code == 200:
            decoded = response.content.decode('utf-8')
            flights = json.loads(decoded, object_hook=lambda d: SimpleNamespace(**d))

            for f in flights:
                fData = flightData()
                fData.fillRawData(f)
                flightList.append(fData)

            return flightList
        else:
            print(response)
            return None


    # The main entry point for this class to run the application
    def run(self):
        
        self.__readConfig()

        self.display.initialize(self.enableDisplay)

        while True:
            self.__appCycle()
            time.sleep(45)


    #  Gets called at the application update cycle interval
    def __appCycle(self):
        #self.__displayFlightsDebug()

        allFlights = [flightData]

        pastFlights = self.__getPastFlights(allFlights)
        activeFlights = self.__getActiveFlights(allFlights)
        localInfo = self.__getLocalInfo()

        self.display.showData(activeFlights, pastFlights, localInfo)

        exit()      # Temporary exit here just for easier development.


    def __getPastFlights(self, allFlights):
        flightA = flightData()
        flightB = flightData()
        return [flightA, flightB]
    

    def __getLocalInfo(self):
        data = LocalInfoData()

        # Fake data. ToDo: Get the real thing
        data.QFE = 1014
        data.temperature = 21.5
        data.windDirection = 183
        data.windspeedMs = 4.5
        data.windGustsMs = 6.3
        data.sunSet = "21:45"

        return data


    def __getActiveFlights(self, allFlights:List[flightData]):

        # create some dummy flights. ToDo: Get the real thing
        flightA = flightData()
        flightA.aircraftRegistration = "PH-1480"
        flightA.pilotInCommandName = "Zacharias Zweefmans"
        flightA.launchTime = "12:23"
        flightA.landingTime = "13:19"

        flightB = flightData()
        flightB.aircraftRegistration = "PH-712"
        flightB.pilotInCommandName = "Frederique frillevrees"
        flightB.launchTime = "8:04"
        flightB.landingTime = "13:05"

        flightC = flightData()
        flightC.aircraftRegistration = "PH-401"
        flightC.pilotInCommandName = "Harry houthakker"
        flightC.launchTime = "11:31"
        flightC.landingTime = "12:54"

        flightD = flightData()
        flightD.aircraftRegistration = "PH-1471"
        flightD.pilotInCommandName = "Bram Brommermans"
        flightD.launchTime = "10:03"
        flightD.landingTime = "12:40"


        return [flightA, flightB, flightC, flightD] 


    def __displayFlightsDebug(self):
        flights = self.__get_flight_info()

        if flights is not None:
            print("flights:")
            for f in flights:
                txt = "-- "
                txt += f.aircraftRegistration
                txt += " " + f.aircraftType
                txt += " " + f.pilotInCommandName
                
                if(f.hasPassenger()):
                    txt += " & " + f.passengerName
                
                if(f.hasLaunched()):
                    txt += "   " + f.launchTime
                    txt += " (" + f.launchMethod + ")"

                    if(f.hasLanded()):
                        txt += " " + f.landingTime
                
                txt += " Overland: " + str(f.isCrossCountry)
                    
                print(txt)
        else:
            print('[!] Request Failed')


    def __readConfig(self):
            config = configparser.ConfigParser()
            config.read('fdconfig.conf')
            clubSchemaName = config['API']["clubSchemaName"]
            api_token = config['API']["apiKey"]
            self.api_url_base = self.api_url_baseFormat.format(clubSchemaName)
            self.headers = {'Content-Type': 'application/json',
                    'X-API-KEY': '{0}'.format(api_token)}
            
            self.enableDisplay = config["DISPLAY"]["displayEnabled"].upper() == "TRUE"
            
            print("Loaded club schema name: " + clubSchemaName)


    def shutdown(self):
        self.display.shutdown()



if __name__ == "__main__":
    
    flDisplay = flightDisplayMain()
    try:
        flDisplay.run()
    except KeyboardInterrupt:    
        print("Application shutting down")
        flDisplay.shutdown()
        exit()