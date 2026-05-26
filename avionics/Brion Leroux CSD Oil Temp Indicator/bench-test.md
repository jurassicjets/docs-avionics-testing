bench testing the Brion Leroux CSD Oil Temp Indicator

_________________________________
**EQUIPMENT REQUIRED**
* 28v DC supply
* 2x 10kR potentiometers or some other source of variable resistance
* recommended: DPDT switch



_________________________________
**TEST SETUP**

Use a DPDT switch to emulate the drive temp select logic which is integrated in the AC generator panel, see 24-11-21 for wiring. 

Connect the potentiometers or variable resistance source per 24-11-21 and use them to adjust the simulated temperature. 

Connect 28vDC power and ground per pinout. 

Adjusting the two potentiometers will adjust the current flow into the gauge, and change the dial position.

Flipping the switch will reconfigure how the potentiometers are wired into the instrument and will toggle between CSD oil outlet temp and CSD oil temp rise. 


_________________________________
**PIN CONNECTIONS**

3 - DPDT switch

4 - ground

5 - DPDT switch

6 - DPDT switch

11 - 28v DC supply

12 - potentiometers

_________________________________
_________________________________
**LAB LOG**

4/26/26 - Experimenting with driving a signal. Found that a low voltage AC signal >20Hz can be used to drive the CSD rise indication (pins 4 and 6) without needing power on the instrument. Added 28v and experimented with using two potentiometers to serve as the thermistors and was able to get both temp and rise readings although the setup made it difficult to switch between the two. Next time will use a DPDT switch to better emulate the internal logic in the AC generator panel. 

5/4/26 - Added documentation
