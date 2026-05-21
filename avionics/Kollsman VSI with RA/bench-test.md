bench testing the Kollsman Vertical Speed Indicator with Resolution Advisory

_________________________________
**EQUIPMENT REQUIRED**

what equipment is needed to test this instrument

_________________________________
**TEST SETUP**

describe how to set up the test

Possible useful ARINC words, generic TCAS ARINC labels, per a quick google search

- 270: TCAS Vertical Resolution Advisory Data Output Word. It carries dedicated discrete information (e.g., bit functions detailing "Climb" or "Descend" RAs and vertical speed limits).

- 273: Additional discrete word mapped specifically for Resolution Advisory displays, controlling specific command indicators on primary flight instruments (like the VSI).

- 274: Traffic Display Data, Discretes, Sends traffic advisory status and display commands.

- 371: Barometric Altitude Rate, BNR, Rate of climb or descent used to calculate vertical speed.

_________________________________
**PIN CONNECTIONS**

what pins need to be connected, and to what?

_________________________________
_________________________________
**LAB LOG**

5/21/26 - initial research and WDM tracing