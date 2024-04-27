import os
from typing import Tuple
from display import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont, ImageOps
import logging

displayDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'display')
imgDumpDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'imgDump')

logging.basicConfig(level=logging.DEBUG)

# The number of updates that will be done to the display before a full clear will be done.
UpdatesBeforeFullRefresh = 2

# High level e-paper driver.
class EPaperDisplay:

    def __init__(self):
        self.EnableDisplay = False        # Enabled the e-paper display. Can be set to False for faster debugging
        self.__cntBeforeFullRefresh = 1   # Counts down on every screen update. When zero, a full refresh is needed

        self.fillColor = 0                # The foreground color. Use this for lines and text on both the black and red image canvases  
        self.backColor = 255              # The backround color. Use this for lines and text on both the black and red image canvases  
        self.width = 800                  # The width of the display in pixels
        self.height = 480                 # The height of the display in pixels
        
        self.font24 = ImageFont.truetype(os.path.join(displayDir, 'Font.ttc'), 24)
        self.font18 = ImageFont.truetype(os.path.join(displayDir, 'Font.ttc'), 18)
        self.font16 = ImageFont.truetype(os.path.join(displayDir, 'Font.ttc'), 16)
        self.fontBBold18 = ImageFont.truetype(os.path.join(displayDir, 'Bitter-Black.ttf'), 18)
        self.fontBBold24 = ImageFont.truetype(os.path.join(displayDir, 'Bitter-Black.ttf'), 24)

        self.fontArial18 = ImageFont.truetype(os.path.join(displayDir, 'arial.ttf'), 18)
        self.fontArial20 = ImageFont.truetype(os.path.join(displayDir, 'arial.ttf'), 20)
        self.fontArial24 = ImageFont.truetype(os.path.join(displayDir, 'arial.ttf'), 24)
        self.fontABlack20 = ImageFont.truetype(os.path.join(displayDir, 'arialBlack.ttf'), 20)
        self.fontABlack24 = ImageFont.truetype(os.path.join(displayDir, 'arialBlack.ttf'), 24)
        self.fontABlack28 = ImageFont.truetype(os.path.join(displayDir, 'arialBlack.ttf'), 28)
        self.fontABold24 = ImageFont.truetype(os.path.join(displayDir, 'arialBold.ttf'), 24)

        

        self.blackImage = None      # Holds the image buffer for the black display layer


    # Initializes the display
    # When enableDisplay is set to true, the e-paper display will be used. Otherwise display output will 
    # be written to /imgDump. Setting this to false is convenient during development and debugging slow e-paper displays
    def initialize(self, enableDisplay:bool):
        print("Initializing and clearing e-paper display. This might take a few seconds")

        self.EnableDisplay = enableDisplay

        if(self.EnableDisplay):
            self.epd = epd7in5_V2.EPD()
            self.epd.init()
            self.epd.Clear()
            self.__cntBeforeFullRefresh = UpdatesBeforeFullRefresh
        else:
            if not os.path.exists(imgDumpDir):
                os.makedirs(imgDumpDir)
                print("Initalize: Epaper disabled")


    # Returns the black and red display canvases
    def getDisplayCanvas(self) -> Tuple[ImageDraw.ImageDraw]:

        if(self.blackImage != None):
            raise RuntimeError("Cannot get a new canvas when the old one hasn't been shown yet")

        self.blackImage = Image.new('1', (self.width, self.height), self.backColor)
        blackCanvas = ImageDraw.Draw(self.blackImage)

        return blackCanvas


    # Shows the full canvas on the display.
    # Call this method after drawing on the canvas provided by the getDisplayCanvas method
    def showFullCanvas(self):
        if(self.blackImage == None):
            raise RuntimeError("Cannot show the canvas on the display when it hasn't been created yet")

        self.__prepareForDisplayUpdate()
        self.__showImagesOnDisplay()
        self.blackImage = None


    # Clears the display and puts it in sleep mde. This method must be called before the application shuts down
    def shutdown(self):
        print("Clearing and shutting down the e-paper display. This might take a few seconds.")
        if(self.EnableDisplay):
            self.epd.Clear()
            self.epd.sleep()

        print("Display shutdown completed")


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


    # Shows the provided canvas on the display
    def __showImagesOnDisplay(self):
         
         if(self.EnableDisplay):
            print("Writing image data to display")
            self.epd.display(self.epd.getbuffer(self.blackImage))
         else:
            print("Display disabled. Writing image data to files")
            self.__saveDisplayImage(self.blackImage)
         self.__cntBeforeFullRefresh -= 1


    # Saves the two display images as one display image
    def __saveDisplayImage(self, imgBlack: Image):
 
        whiteimg = Image.new('RGBA', (imgBlack.width, imgBlack.height))
        whiteimg.paste((255,255,255), (0,0, whiteimg.width, whiteimg.height) )

        #redMask = self.__convertToMaskedForeground(imgRed, 255, 0, 0)
        blackMask = self.__convertToMaskedForeground(imgBlack, 0, 0, 0)

        #whiteimg.paste(redMask, (0,0), redMask)
        whiteimg.paste(blackMask, (0,0), blackMask)
        
        whiteimg.save(os.path.join(imgDumpDir, 'display.bmp'))
        imgBlack.save(os.path.join(imgDumpDir, 'blackFrame.bmp'))
        #imgRed.save(os.path.join(imgDumpDir, 'redFrame.bmp'))

        print("Saved display image to display.bmp")


    # Converts a black and white image to an image with the desired foreground color leaves the white pixels as a mask
    # White pixels are seen as background and become transparent. Black is seen as foreground color
    # image: A black and white image to be converted to a transparent mask
    # r, g, b: The Red, Green and Blue values for the desired foreground color for the mask. (Will be fully opaque)
    def __convertToMaskedForeground(self, image: Image, r:int, g:int, b:int) -> Image:
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
            if pixel[R] == 0 and pixel[G] == 0 and pixel[B] == 0:
                newPixelData.append((r, g, b, Opaque))
            else:
                newPixelData.append((White, White, White, Transparent))
        mask.putdata(newPixelData)
        return mask
