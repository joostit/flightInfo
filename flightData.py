import time
from datetime import datetime, timedelta
import datetime


# A class that contains information about a single flight
class flightData:

    def __init__(self):

        self.uuid = ""
        self.isCrossCountry = ""
        self.launchMethod = ""
        self.callsign = ""
        self.aircraftRegistration = ""
        self.aircraftType = ""
        self.date = ""
        self.landingSite = ""
        self.landingTime = ""
        self.launchSite = ""
        self.launchTime = ""
        self.pilotInCommandName = ""
        self.passengerName = ""
        

    # Geths whether the aircraft has launched
    def hasLaunched(self) -> bool:
        return self.launchTime != None and self.launchTime != ""
    

    # Gets whether the aircraft has landed
    def hasLanded(self) -> bool:
        return self.landingTime != None and self.landingTime != "" 
    

    # Gets whether there is a passenger
    def hasPassenger(self) -> bool:
        return self.passengerName != None and self.passengerName != ""


    # Fills this object with raw data obtained from the Zweef.App API
    def fillRawData(self, raw):
        self.uuid = raw.uuid
        self.isCrossCountry = raw.is_overland
        self.launchMethod = raw.start_methode
        self.aircraftCallsign = raw.callsign
        self.aircraftRegistration = raw.registratie
        self.aircraftType = raw.type
        self.date = raw.datum
        self.landingSite = raw.vertrek_vliegveld
        self.launchSite = raw.aankomst_vliegveld
        self.landingTime = raw.landings_tijd
        self.launchTime = raw.start_tijd
        self.pilotInCommandName = raw.gezagvoerder_naam
        self.passengerName = raw.tweede_inzittende_naam


    # Returns the flight time as a timedelta object
    def getFlightTime(self) -> timedelta:
        lauchTimestamp: datetime.datetime
        timeFormat = "%H:%M"
        if self.hasLaunched():
            lauchTimestamp =  datetime.datetime.strptime(self.launchTime, timeFormat)
        else:
            return None
        
        if self.hasLanded():
            landTimestamp = datetime.datetime.strptime(self.landingTime, timeFormat)
        else:
            landTimestamp = datetime.datetime.now()

        diff = (landTimestamp - lauchTimestamp)
        return diff

        





