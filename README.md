# FlightInfo

Shows up-to-date Zweef.App flights and meteorological information on a WaveShare 7.5" E-paper display. For use at Dutch Glider clubs.

## Author: Joost Haverkort
https://github.com/DevOats

## Usage
The application has been designed to run on a Raspberry Pi using Raspberry Pi OS, though it probably should run on any platform, albeit with some tweaks to the low level E-Paper driver.

1. Install all prerequisites for the E-Paper accoring to the WaveShare manual (Not needed if running with the display enabled)
1. Copy the file `fdconf.conf.template` and rename it to `fdconf.conf`
1. Open `fdconf.conf` and update the settings according to your situation
   - The Club schema name can be obtained form your Zweef.App admin console
   - An API key with read acccess can be created from the Zweef.App admin console
   - When setting `displayEnabled = false`, the application can run without an e-reader display attached. The display output will be written to the `imgDump` folder, which is useful during development and testing.
1. execute `python flightDisplayMain.py`

### Important
- Make sure that the application is closed gracefully (On the terminal with Ctrl+C). Otherwiser the E-paper display might be left in a power-on state, potentially leading to damage.

## Acknowledgements
- The E-reader driver stack is based on the excellent demo code and cocumentation provided by Waveshare: https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B)_Manual
- Uses the Bitter-Black font: https://github.com/solmatas/BitterPro
- Uses Microsoft Arial. Thanks MS :)
