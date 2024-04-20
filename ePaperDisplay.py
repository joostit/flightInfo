import datetime
import os
from display import epd7in5b_V2
from PIL import Image,ImageDraw,ImageFont

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'display')
import logging

logging.basicConfig(level=logging.DEBUG)

UpdatesBeforeFullRefresh = 3


class EPaperDisplay:

    def __init__(self):
        self.__cntBeforeFullRefresh = 1   # Counts down on every screen update. When zero, a full refresh is needed
        self.epd = epd7in5b_V2.EPD()
        self.font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        self.font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)



    def initialize(self):
        logging.info("Initializing and clearing e-paper display. This might take a few seconds")
        self.epd.init()
        self.epd.Clear()
        self.__cntBeforeFullRefresh = UpdatesBeforeFullRefresh



    def showData(self, activeFlights, pastFlights):
        
        blackImage = Image.new('1', (self.epd.width, self.epd.height), 255)
        redImage = Image.new('1', (self.epd.width, self.epd.height), 255)
        blackCanvas = ImageDraw.Draw(blackImage)
        redCanvas = ImageDraw.Draw(redImage)
        
        self.__prepareForDisplayUpdate()

        self.__drawLayout(blackCanvas, redCanvas)
        self.__drawActiveFlights(activeFlights, blackCanvas, redCanvas)
        self.__drawPastFlights(pastFlights, blackCanvas, redCanvas)

        self.__showCanvasOnDisplay(blackImage, redImage)


    def __drawActiveFlights(self, activeFlights, blackCanvas, redCanvas):
            pass
    
    def __drawPastFlights(self, pastFlights, blackCanvas, redCanvas):
            pass
    
    def __drawLayout(self,  blackCanvas, redCanvas):
            timestamp = datetime.date.today().strftime('%Y-%m-%d %H:%M:%S')
            blackCanvas.text((650, 0), timestamp, font = self.font24, fill = 0)
            redCanvas.text((650, 300), timestamp, font = self.font24, fill = 0)
            pass


    # Prepares the display for the next update by reinitializing and clearing the display
    # In a future update, this might be optimized by not always doing a full refresh?
    def __prepareForDisplayUpdate(self):
        logging.info("Initializing e-paper display.")
        self.epd.init()

        if(self.__cntBeforeFullRefresh <= 0):
            logging.info("Doing a full e-paper display clear.")
            self.epd.Clear()
            self.__cntBeforeFullRefresh = UpdatesBeforeFullRefresh
        else:
             logging.info("Omitting full display clearing.")


    # Shows the provided canvases on the display
    # In a future update this might be optimized for not always having to do a full display update
    def __showCanvasOnDisplay(self, blackImage, redImage):
         self.epd.display(self.epd.getbuffer(blackImage), self.epd.getbuffer(redImage))
         self.__cntBeforeFullRefresh -= 1


    def shutdown(self):
        logging.info("Clearing and shutting down the e-paper display. This might take a few seconds.")
        self.epd.Clear()
        self.epd.sleep()