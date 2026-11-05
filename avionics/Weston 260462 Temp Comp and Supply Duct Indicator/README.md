README for the Weston 260462 Temp Comp and Supply Duct Indicator

_________________________________
**OVERVIEW**

This is a dual concentric gauge used to display temperature of the duct and compartments in the air conditioning system. 

_________________________________
**VARIATIONS**

Unknown

_________________________________
**APPLICABILITY**

P4 air conditioning panel

_________________________________
**DEPENDENCIES AND INTEGRATIONS**

None

_________________________________
**OPERATION AND FUNCTION**

This instrument contains two independent gauges, each with nearly identical operation. Both gauges utilize a linear ratiometer configuration with a reference and signal wire. The reference wire is connected directly to ground, the signal connects to ground via a thermistor which provides a variable resistance to drive the needle. The upper "compt" needle displays from 60 to 90 degrees F. It operates from 89.7R (17.4mA) at the bottom of the scale, to 102.3R (16.7mA) at the top of the scale (Delta 12.6R/0.7mA). The bottom "duct" needle displays from 20 to 200 degrees F. It operates from 81.1R (17.3mA) at the bottom of the scale, to 127.4R (15.0mA) at the top of the scale (Delta 46.3R/2.3mA). Both needles are linear in behavior. 

_________________________________
**QUIRKS**

Narrow range of resistances makes it finnicky when bench testing. Ensure good connections to aviod wobble and utilize a biasing resistor and parallel resistances to remove deadzone and decrease sensitivity if using a potentiometer to make your life easier. 
