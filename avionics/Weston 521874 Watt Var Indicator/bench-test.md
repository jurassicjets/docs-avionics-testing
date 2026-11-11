bench testing the Weston 521874 Watt Var Indicator

_________________________________
**EQUIPMENT REQUIRED**

Three-phase 400hz 115VAC power supply
High power variable resistance
_________________________________
**TEST SETUP**

NOT TESTED: Most likely theory is to apply the phase-b voltage to one side of the sensing coil through an attenuator. Suspicion is that a lower amplitude (possibly in the range of 5VAC or 28VAC) in-phase signal is used to provide a ratio to the reference side of the coil, which is connected to phase B 115VAC. Unknown what amplitude is needed to drive the sense coil. USE CAUTION WHEN APPLYING UNKNOWN VOLTAGE - START LOW, CALCULATE POWER DISSIPATION BEFORE APPLICATION. 

_________________________________
**PIN CONNECTIONS**

Pins 3+4 connect to phase B of the 400hz power supply as a reference signal. 

Pins 7+8 connect to the "sense" signal, which is TBD. See TEST SETUP section for best guess on how to determine signal characteristics. 
_________________________________
_________________________________
**LAB LOG**

11/10/2026 - Init gauge documentation. Reviewed WDM. Basic setup with low voltage 400hz signal on both coils. Observed no needle movement with phase shift or frequency shift. Further testing required using proper 115VAC power supply. 

11/11/2026 - More investigation of the WDM, determined likely operating method of the gauge, as detailed in README. 
