

class flightData:

    def __init(self):

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
        return self.launchTime != None
    
    def hasLanded(self):
        return self.landingTime != None
    
    def hasPassenger(self):
        return self.passengerName != ""


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




