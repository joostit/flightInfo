#!/usr/bin/python
# -*- coding:utf-8 -*-
################################
#
# Displays flight information obtained from Zweef.App on a WaveShare 7.5" e-paper display
# Author: Joost Haverkort
#
################################
import json
import time
from typing import List
import requests
import configparser
from types import SimpleNamespace
from flightData import flightData
from flightDataDisplayer import FlightDataDisplayer
from localInfoData import LocalInfoData


# Main application class
class flightDisplayMain:

    def __init__(self):
        self.api_url_base = ""
        self.api_url_baseFormat = "https://admin.zweef.app/club/{0}/api/"
        self.headers = ""
        self.enableDisplay = False
        self.display = FlightDataDisplayer()


    # Reads flight information from the Zweef.App public API
    def __get_flight_info(self) -> List:
    
        flightList = []
        api_url = '{0}flights.json'.format(self.api_url_base)
        response = requests.get(api_url, headers=self.headers)

        if response.status_code == 200:
            decoded = response.content.decode('utf-8')
            flights = json.loads(decoded, object_hook=lambda d: SimpleNamespace(**d))

            for f in flights:
                fData = flightData()
                fData.fillRawData(f)
                flightList.append(fData)

            return flightList
        else:
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

    	# Temporary exit here just for easier development.
        # ToDo: Remove this
        #exit()      


    # Filters the list containing all flights and returns only flights that have landed
    def __getPastFlights(self, allFlights: List[flightData]) -> List[flightData]:

        flights: List[flightData] = []

        # create some dummy flights. ToDo: Get the real thing
        flightA = flightData()
        flightA.aircraftRegistration = "PH-1480"
        flightA.pilotInCommandName = "Zacharias Zweefmans"
        flightA.launchTime = "12:23"
        flightA.landingTime = "13:19"
        flights.append(flightA)

        flightB = flightData()
        flightB.aircraftRegistration = "PH-712"
        flightB.pilotInCommandName = "Frederique frillevrees"
        flightB.launchTime = "11:55"
        flightB.landingTime = "13:05"
        flights.append(flightB)

        flightC = flightData()
        flightC.aircraftRegistration = "PH-401"
        flightC.pilotInCommandName = "Harry houthakker"
        flightC.launchTime = "11:31"
        flightC.landingTime = "12:54"
        flights.append(flightC)

        flightD = flightData()
        flightD.aircraftRegistration = "PH-1471"
        flightD.pilotInCommandName = "Bram Brommermans"
        flightD.launchTime = "09:03"
        flightD.landingTime = "12:40"
        flights.append(flightD)

        flightE = flightData()
        flightE.aircraftRegistration = "PH-798"
        flightE.pilotInCommandName = "Peter Pief"
        flightE.launchTime = "12:22"
        flightE.landingTime = "12:37"
        flights.append(flightE)

        flightF = flightData()
        flightF.aircraftRegistration = "D-8338"
        flightF.pilotInCommandName = "Vinny Vario"
        flightF.launchTime = "12:04"
        flightF.landingTime = "12:25"
        flights.append(flightF)

        flightG = flightData()
        flightG.aircraftRegistration = "PH-798"
        flightG.pilotInCommandName = "Peter Pief"
        flightG.launchTime = "11:59"
        flightG.landingTime = "12:11"
        flights.append(flightG)

        flightH = flightData()
        flightH.aircraftRegistration = "PH-1480"
        flightH.pilotInCommandName = "Roland Schneider"
        flightH.launchTime = "11:47"
        flightH.landingTime = "11:55"
        flights.append(flightH)

        flightI = flightData()
        flightI.aircraftRegistration = "PH-712"
        flightI.pilotInCommandName = "Deborah De Beau"
        flightI.launchTime = "11:12"
        flightI.landingTime = "11:35"
        flights.append(flightI)

        return flights 
    

    # Filters the list containing all flights and returns only flights that are currently flying
    def __getActiveFlights(self, allFlights:List[flightData]) -> List[flightData]:

        flightA = flightData()
        flightB = flightData()
        return [flightA, flightB]


    # Obtains useful local information
    def __getLocalInfo(self) -> LocalInfoData:
        data = LocalInfoData()

        # Fake data. ToDo: Get the real thing
        data.QFE = 1014
        data.temperature = 21.5
        data.windDirection = 183
        data.windspeedMs = 4.5
        data.windGustsMs = 6.3
        data.sunSet = "21:45"

        return data

    
    # Prints flight information to the console
    # ToDo: Remove this
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


    # Reads the configuration file and stores it parameters
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


    # Shuts down the application.
    # Important: This method must be called upon shutdown to prevent damage to the e-paper.
    def shutdown(self):
        self.display.shutdown()


# Application Entry point.
# Note that when terminating the application from the console with Ctrl+C, the application will gracefully shut down
# This is to prevent damage to the e-paper display
if __name__ == "__main__":
    
    flDisplay = flightDisplayMain()
    try:
        flDisplay.run()
    except KeyboardInterrupt:    
        print("Application shutting down")
        flDisplay.shutdown()
        exit()