import datetime
import os
from display import epd7in5b_V2
from PIL import Image,ImageDraw,ImageFont, ImageOps

import numpy as np

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'display')
imgDumpDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'imgDump')
import logging

logging.basicConfig(level=logging.DEBUG)

UpdatesBeforeFullRefresh = 3
debugImageFolder = "imgDump"

class EPaperDisplay:

    def __init__(self):
        self.EnableDisplay = False         # Enabled the e-paper display. Can be set to False for faster debugging
        self.__cntBeforeFullRefresh = 1   # Counts down on every screen update. When zero, a full refresh is needed
        self.epd = epd7in5b_V2.EPD()
        self.font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        self.font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)


    def initialize(self):
        logging.info("Initializing and clearing e-paper display. This might take a few seconds")

        if(self.EnableDisplay):
            self.epd.init()
            self.epd.Clear()
            self.imgBackColor = 255
            self.fillColor = 0
            self.__cntBeforeFullRefresh = UpdatesBeforeFullRefresh
        else:
            self.imgBackColor = 0
            self.fillColor = 255
            if not os.path.exists(imgDumpDir):
                os.makedirs(imgDumpDir)
                logging.info("Initalize: Epaper disabled")


    def showData(self, activeFlights, pastFlights):
        
        blackImage = Image.new('1', (self.epd.width, self.epd.height), self.imgBackColor)
        redImage = Image.new('1', (self.epd.width, self.epd.height), self.imgBackColor)
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
            blackCanvas.text((650, 0), timestamp, font = self.font24, fill = self.fillColor)
            redCanvas.text((650, 300), timestamp, font = self.font24, fill = self.fillColor)
            pass


    # Prepares the display for the next update by reinitializing and clearing the display
    def __prepareForDisplayUpdate(self):
        if(self.EnableDisplay):
            logging.info("Initializing e-paper display.")
            self.epd.init()

            if(self.__cntBeforeFullRefresh <= 0):
                logging.info("Doing a full e-paper display clear.")
                self.epd.Clear()
                self.__cntBeforeFullRefresh = UpdatesBeforeFullRefresh
            else:
                logging.info("Omitting full display clearing.")


    # Shows the provided canvases on the display
    def __showCanvasOnDisplay(self, blackImage, redImage):
         
         if(self.EnableDisplay):
            logging.info("Writing image data to display")
            self.epd.display(self.epd.getbuffer(blackImage), self.epd.getbuffer(redImage))
         else:
            logging.info("Display disabled. Writing image data to files")
            self.__saveDisplayImage(blackImage, redImage)
         self.__cntBeforeFullRefresh -= 1


    def __saveDisplayImage(self, blackImage, redImage):
 
        whiteimg = Image.new('RGBA', (blackImage.width, blackImage.height))
        whiteimg.paste((255,255,255), (0,0, whiteimg.width, whiteimg.height) )

        redMask = self.__convertToMaskedForeground(redImage, 255, 0, 0)
        blackMask = self.__convertToMaskedForeground(blackImage, 0, 0, 0)

        whiteimg.paste(redMask, (0,0), redMask)
        whiteimg.paste(blackMask, (0,0), blackMask)
        whiteimg.save(os.path.join(imgDumpDir, 'display.bmp'))

        logging.info("Saved display image to display.bmp")


    # Converts a black and white image to an image with the desired foreground color leaves the white pixels as a mask
    # Black pixels are seen as background and become transparent. White is seen as foreground
    def __convertToMaskedForeground(self, image, r, g, b):
        R = 0
        G = 1
        B = 2
        Transparent = 0
        Opaque = 255
        White = 255
        mask = image.convert('RGBA')
        originalPixelData = mask.getdata()
        newPixelData = []
        for pixel in originalPixelData:
            if pixel[R] == 255 and pixel[G] == 255 and pixel[B] == 255:
                newPixelData.append((r, g, b, Opaque))
            else:
                newPixelData.append((White, White, White, Transparent))
        mask.putdata(newPixelData)
        return mask


    def shutdown(self):
        logging.info("Clearing and shutting down the e-paper display. This might take a few seconds.")
        if(self.EnableDisplay):
            self.epd.Clear()
            self.epd.sleep()

        logging.info("Display shutdown completed")