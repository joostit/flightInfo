import time
from datetime import datetime
import datetime

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
        

    def hasLaunched(self):
        return self.launchTime != None and self.launchTime != ""
    
    def hasLanded(self):
        return self.landingTime != None and self.landingTime != "" 
    
    def hasPassenger(self):
        return self.passengerName != None and self.passengerName != ""


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


    def getFlightTime(self):
        lauchTimestamp: datetime.datetime
        timeFormat = "%H:%M"
        if self.hasLaunched():
            lauchTimestamp =  datetime.datetime.strptime(self.launchTime, timeFormat)
        else:
            return None
        
        if self.hasLanded():
            landTimestamp = datetime.datetime.strptime(self.landingTime, timeFormat)
        else:
            landTimestamp = datetime.now().time

        diff = (landTimestamp - lauchTimestamp)
        return diff

        





