from datetime import datetime, timedelta
import os
from typing import List, Tuple
from ePaperDisplay import EPaperDisplay
from flightData import flightData
from PIL import Image, ImageDraw

from localInfoData import LocalInfoData


# Responsible for displaying information on the screen and its layout
class FlightDataDisplayer:

    imgDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img')


    def __init__(self):
        self.epd = EPaperDisplay()


    # Initializes the display. 
    # enableDisplay: Set to true when the e-paper display should be enabled. Otherwise display images are saved as images
    # This is useful during development 
    def initialize(self, enableDisplay: bool):
        self.epd.initialize(enableDisplay)


    # Draws the given data to the display and refreshes the display
    def showData(self, activeFlights: List[flightData], pastFlights: List[flightData], infoData: LocalInfoData):
        blackCanvas, redCanvas = self.epd.getDisplayCanvases()

        self.__drawLayout(blackCanvas, redCanvas)
        self.__drawInfoPanel(blackCanvas, redCanvas, infoData)
        self.__drawActiveFlights(activeFlights, blackCanvas, redCanvas)
        self.__drawPastFlights(pastFlights, blackCanvas, redCanvas)

        self.epd.showCanvases()


    # Shuts down the display. This method must be called before exiting the application
    def shutdown(self):
        self.epd.shutdown()


    # Draws the global layout to the screen
    def __drawLayout(self,  blackCanvas:ImageDraw, redCanvas:ImageDraw):
        
        vertDivideX = 570
        topRowY = 33

        blackCanvas.line((0, topRowY, vertDivideX, topRowY), self.epd.fillColor, 6)             # Horizontal top line
        blackCanvas.line((vertDivideX, 0, vertDivideX, 480), self.epd.fillColor, 10)             # Vertical divider
        blackCanvas.line((vertDivideX, topRowY, 800, topRowY), self.epd.fillColor, 3)           # Horizontal infoPane bar
        blackCanvas.line((vertDivideX, 200, 800, 200), self.epd.fillColor, 3)                   # Horizontal activeFlights bar
        blackCanvas.text((180, -7), "Last flights", font = self.epd.fontABlack28, fill = self.epd.fillColor)


    # Fills the information panel with data
    def __drawInfoPanel(self, blackCanvas:ImageDraw, redCanvas:ImageDraw, infoData: LocalInfoData):

        col1X = 585
        col2X = 665

        self.__putBmp((590, 5), "refreshA.bmp", blackCanvas)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        blackCanvas.text((625, 5), timestamp, font = self.epd.fontArial20, fill = self.epd.fillColor)

        blackCanvas.text((col1X, 40), "Temp: ", font = self.epd.fontArial20, fill = self.epd.fillColor)
        blackCanvas.text((col1X, 65), "Wind: ", font = self.epd.fontArial20, fill = self.epd.fillColor)
        blackCanvas.text((col1X, 140), "QFE: ", font = self.epd.fontArial20, fill = self.epd.fillColor)
        blackCanvas.text((col1X, 165), "Sunset: ", font = self.epd.fontArial20, fill = self.epd.fillColor)

        blackCanvas.text((col2X, 40), str(infoData.temperature) + "°C", font = self.epd.fontArial20, fill = self.epd.fillColor)
        blackCanvas.text((col2X, 65), str(infoData.windDirection) + "°", font = self.epd.fontArial20, fill = self.epd.fillColor)
        blackCanvas.text((col2X, 90), str(infoData.windspeedMs) + "m/s", font = self.epd.fontArial20, fill = self.epd.fillColor)
        blackCanvas.text((col2X, 115), "(" + str(infoData.windGustsMs) + "m/s)", font = self.epd.fontArial20, fill = self.epd.fillColor)

        blackCanvas.text((col2X, 140), str(infoData.QFE) + "hPa", font = self.epd.fontArial20, fill = self.epd.fillColor)
        blackCanvas.text((col2X, 165), str(infoData.sunSet), font = self.epd.fontArial20, fill = self.epd.fillColor)


    # Fills the active flights panel with data
    def __drawActiveFlights(self, activeFlights: List[flightData], blackCanvas:ImageDraw, redCanvas:ImageDraw):
        pass
            
    
    # Fills the past flights panel with data
    def __drawPastFlights(self, pastFlights: List[flightData], blackCanvas:ImageDraw, redCanvas:ImageDraw):
        y = 40

        for fl in pastFlights:
            flTime = fl.getFlightTime()

            if flTime != None:
                flightTime = self.__pretty_time_delta(flTime.seconds)
            else:
                    flightTime = ""

            blackCanvas.text((-2, y - 4), fl.aircraftRegistration, font = self.epd.fontABlack20, fill = self.epd.fillColor)
            blackCanvas.text((100, y + 2), fl.launchTime, font = self.epd.fontArial18, fill = self.epd.fillColor)
            blackCanvas.text((150, y + 2), fl.landingTime, font = self.epd.fontArial18, fill = self.epd.fillColor)
            blackCanvas.text((215, y), fl.pilotInCommandName , font = self.epd.fontArial20, fill = self.epd.fillColor)
            blackCanvas.text((525, y + 2), flightTime, font = self.epd.fontArial18, fill = self.epd.fillColor)

            blackCanvas.line((10, y + 31, 555, y + 31), self.epd.fillColor, 1)           # Horizontal bar

            y += 40


    # Formats a count on seconds to display in HH:MM
    def __pretty_time_delta(self, seconds:int):
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


    # Opens a bitmap from storage and draws it on the given canvas
    def __putBmp(self, xy:Tuple[int, int], bmpName:str, canvas:ImageDraw):
        bmp = Image.open(os.path.join(self.imgDir, bmpName))
        canvas.bitmap(xy, bmp, fill = self.epd.fillColor)
    

