import json
import requests
import configparser
from types import SimpleNamespace
from flightData import flightData

class FlDisplay:

    

    def __init__(self):
        self.api_url_base = ""
        self.api_url_baseFormat = "https://admin.zweef.app/club/{0}/api/"
        self.headers = ""


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



    def run(self):
        self.__readConfig()
        self.__displayFlightsDebug()

        

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
            
            print("Loaded club schema name: " + clubSchemaName)



if __name__ == "__main__":
    
    flDisplay = FlDisplay()
    flDisplay.run()