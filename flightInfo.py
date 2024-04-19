import json
import requests
import configparser

class FlDisplay:

    

    def __init__(self):
        self.api_url_base = ""
        self.api_url_baseFormat = "https://admin.zweef.app/club/{0}/api/"
        self.headers = ""


    def __get_flight_info(self):
    
        api_url = '{0}flights.json'.format(self.api_url_base)

        response = requests.get(api_url, headers=self.headers)

        print(api_url)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            print(response)
            return None
        
    


    def __readConfig(self):
        config = configparser.ConfigParser()
        config.read('fdconfig.conf')
        
        print(config.sections())

        clubSchemaName = config['API']["clubSchemaName"]
        api_token = config['API']["apiKey"]

        print("Club schema name: " + clubSchemaName)

        self.api_url_base = self.api_url_baseFormat.format(clubSchemaName)

        self.headers = {'Content-Type': 'application/json',
                'X-API-KEY': '{0}'.format(api_token)}


    def run(self):

        self.__readConfig()

        self.__displayFlightsDebug()

        

    def __displayFlightsDebug(self):
        flights = self.__get_flight_info()

        if flights is not None:
            print("flighs:")
            print("Length: " + str(len(flights)))
            for f in flights:
                print('{0}'.format(f))
        else:
            print('[!] Request Failed')


if __name__ == "__main__":
    
    flDisplay = FlDisplay()
    flDisplay.run()