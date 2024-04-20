from datetime import datetime, timedelta
import time
from typing import List
from ePaperDisplay import EPaperDisplay
from flightData import flightData


class FlightDataDisplayer:

    def __init__(self):
        self.epd = EPaperDisplay()


    def initialize(self, enableDisplay):
        self.epd.initialize(enableDisplay)


    def showData(self, activeFlights, pastFlights):
        blackCanvas, redCanvas = self.epd.getDisplayCanvases()

        self.__drawLayout(blackCanvas, redCanvas)
        self.__drawActiveFlights(activeFlights, blackCanvas, redCanvas)
        self.__drawPastFlights(pastFlights, blackCanvas, redCanvas)

        self.epd.showCanvases()


    def __drawLayout(self,  blackCanvas, redCanvas):
        
        vertDivideX = 570

        blackCanvas.line((0,33, vertDivideX,33), self.epd.fillColor, 3)                 # Horizontal top line
        blackCanvas.line((vertDivideX, 0, vertDivideX, 480), self.epd.fillColor, 6)     # Vertical divider
        
        blackCanvas.line((vertDivideX, 200, 800, 200), self.epd.fillColor, 3)           # Horizontal activeFlights bar

        blackCanvas.text((180, -6), "Last flights", font = self.epd.fontABlack28, fill = self.epd.fillColor)
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        blackCanvas.text((595, 3), timestamp, font = self.epd.fontArial20, fill = self.epd.fillColor)


    def __drawActiveFlights(self, activeFlights: List[flightData], blackCanvas, redCanvas):
            
            y = 40

            for fl in activeFlights:
                flTime = fl.getFlightTime()

                if flTime != None:
                    flightTime = self.__pretty_time_delta(flTime.seconds)
                else:
                     flightTime = ""

                blackCanvas.text((1, y - 4), fl.aircraftRegistration, font = self.epd.fontABlack20, fill = self.epd.fillColor)
                blackCanvas.text((100, y + 2), fl.launchTime, font = self.epd.fontArial18, fill = self.epd.fillColor)
                blackCanvas.text((150, y + 2), fl.landingTime, font = self.epd.fontArial18, fill = self.epd.fillColor)
                blackCanvas.text((215, y), fl.pilotInCommandName , font = self.epd.fontArial20, fill = self.epd.fillColor)
                blackCanvas.text((515, y + 2), flightTime, font = self.epd.fontArial18, fill = self.epd.fillColor)

                blackCanvas.line((20, y + 31, 550, y + 31), self.epd.fillColor, 1)           # Horizontal bar

                y += 40
    

    def __drawPastFlights(self, pastFlights, blackCanvas, redCanvas):
            pass


    def __pretty_time_delta(self, seconds):
        sign_string = '-' if seconds < 0 else ''
        seconds = abs(int(seconds))
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        if days > 0:
            return '%s%dd %d:%02d' % (sign_string, days, hours, minutes, seconds)
        elif hours > 0:
            return '%s%d:%02d' % (sign_string, hours, minutes)
        elif minutes > 0:
            return '%s0:%02d' % (sign_string, minutes)
        else:
            return '%s:%02d' % (sign_string, seconds)


    

    def shutdown(self):
        self.epd.shutdown()