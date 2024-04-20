import datetime
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


    def __drawActiveFlights(self, activeFlights, blackCanvas, redCanvas):
            pass
    

    def __drawPastFlights(self, pastFlights, blackCanvas, redCanvas):
            pass
    

    def __drawLayout(self,  blackCanvas, redCanvas):
            timestamp = datetime.date.today().strftime('%Y-%m-%d %H:%M:%S')
            blackCanvas.text((650, 0), timestamp, font = self.epd.font24, fill = self.epd.fillColor)
            redCanvas.text((650, 300), timestamp, font = self.epd.font24, fill = self.epd.fillColor)


    def shutdown(self):
        self.epd.shutdown()