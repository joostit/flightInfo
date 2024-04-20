import datetime
import os
from display import epd7in5b_V2
from PIL import Image,ImageDraw,ImageFont, ImageOps
import numpy as np
import logging

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'display')
imgDumpDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'imgDump')

logging.basicConfig(level=logging.DEBUG)

UpdatesBeforeFullRefresh = 3

class EPaperDisplay:

    def __init__(self):
        self.EnableDisplay = False         # Enabled the e-paper display. Can be set to False for faster debugging
        self.__cntBeforeFullRefresh = 1   # Counts down on every screen update. When zero, a full refresh is needed
        self.epd = epd7in5b_V2.EPD()
        self.font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        self.font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

        self.blackImage = None      # Holds the image buffer for the black display layer
        self.redImage = None        # # Holds the image buffer for the red display layer


    def initialize(self, enableDisplay):
        print("Initializing and clearing e-paper display. This might take a few seconds")

        self.EnableDisplay = enableDisplay

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
                print("Initalize: Epaper disabled")


    def getDisplayCanvases(self):

        if(self.blackImage != None or self.redImage != None):
            raise RuntimeError("Cannot get new canvases when the old ones haven't been shown yet")

        self.blackImage = Image.new('1', (self.epd.width, self.epd.height), self.imgBackColor)
        self.redImage = Image.new('1', (self.epd.width, self.epd.height), self.imgBackColor)
        blackCanvas = ImageDraw.Draw(self.blackImage)
        redCanvas = ImageDraw.Draw(self.redImage)

        return blackCanvas, redCanvas


    def showCanvases(self):
        if(self.blackImage == None or self.redImage == None):
            raise RuntimeError("Cannot canvases on the display when they haven'nt been created yet")

        self.__prepareForDisplayUpdate()
        self.__showImagesOnDisplay()
        self.blackImage = None
        self.redImage = None


    # Prepares the display for the next update by reinitializing and clearing the display
    def __prepareForDisplayUpdate(self):
        if(self.EnableDisplay):
            print("Waking up e-paper display.")
            self.epd.init()

            if(self.__cntBeforeFullRefresh <= 0):
                print("Doing a full e-paper display clear.")
                self.epd.Clear()
                self.__cntBeforeFullRefresh = UpdatesBeforeFullRefresh
            else:
                print("Omitting display full clear.")


    # Shows the provided canvases on the display
    def __showImagesOnDisplay(self):
         
         if(self.EnableDisplay):
            print("Writing image data to display")
            self.epd.display(self.epd.getbuffer(self.blackImage), self.epd.getbuffer(self.redImage))
         else:
            print("Display disabled. Writing image data to files")
            self.__saveDisplayImage(self.blackImage, self.redImage)
         self.__cntBeforeFullRefresh -= 1


    def __saveDisplayImage(self, imgBlack, imgRed):
 
        whiteimg = Image.new('RGBA', (imgBlack.width, imgBlack.height))
        whiteimg.paste((255,255,255), (0,0, whiteimg.width, whiteimg.height) )

        redMask = self.__convertToMaskedForeground(imgRed, 255, 0, 0)
        blackMask = self.__convertToMaskedForeground(imgBlack, 0, 0, 0)

        whiteimg.paste(redMask, (0,0), redMask)
        whiteimg.paste(blackMask, (0,0), blackMask)
        whiteimg.save(os.path.join(imgDumpDir, 'display.bmp'))

        print("Saved display image to display.bmp")


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
        print("Clearing and shutting down the e-paper display. This might take a few seconds.")
        if(self.EnableDisplay):
            self.epd.Clear()
            self.epd.sleep()

        print("Display shutdown completed")