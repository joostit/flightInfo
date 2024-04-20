from datetime import datetime
from ePaperDisplay import EPaperDisplay


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
        
        vertDivideX = 500

        blackCanvas.line((0,28, vertDivideX,28), self.epd.fillColor, 3)                 # Horizontal top line
        blackCanvas.line((vertDivideX, 0, vertDivideX, 480), self.epd.fillColor, 3)     # Vertical divider
        
        blackCanvas.line((vertDivideX, 250, 800, 250), self.epd.fillColor, 3)           # Horizontal activeFlights bar

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        blackCanvas.text((570, 3), timestamp, font = self.epd.fontBBold24, fill = self.epd.fillColor)
        blackCanvas.text((570, 33), timestamp, font = self.epd.fontBBold18, fill = self.epd.fillColor)


        blackCanvas.text((570, 130), timestamp, font = self.epd.font24, fill = self.epd.fillColor)
        blackCanvas.text((570, 160), timestamp, font = self.epd.font18, fill = self.epd.fillColor)
        blackCanvas.text((570, 190), timestamp, font = self.epd.font16, fill = self.epd.fillColor)

        #redCanvas.text((600, 300), timestamp, font = self.epd.font24, fill = self.epd.fillColor)


    def __drawActiveFlights(self, activeFlights, blackCanvas, redCanvas):
            pass
    

    def __drawPastFlights(self, pastFlights, blackCanvas, redCanvas):
            pass
    

    


    def shutdown(self):
        self.epd.shutdown()