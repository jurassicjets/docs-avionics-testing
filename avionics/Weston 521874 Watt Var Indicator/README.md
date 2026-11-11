README for the Weston 521874 Watt Var Indicator

_________________________________
**OVERVIEW**

This is a dual function gauge that shows either KW or KVAR depending on the state of an external momentary pushbutton. 

_________________________________
**VARIATIONS**

None. 

_________________________________
**APPLICABILITY**

P4 AC Circuit Breaker Panels

_________________________________
**DEPENDENCIES AND INTEGRATIONS**

Requires the Essential AC Meter Module (M168) to be installed to switch the reference signal for KVAR display. KW display mode is default and has no dependencies. 

_________________________________
**OPERATION AND FUNCTION**

NOT VERIFIED: It is suspected that this gauge operates based on the ratio of AC signals. The gauge is drawn in the WDM as two parallel coils. One coil (hereunto refered as the Reference Coil) is connected directly to at least one 115VAC 400hz busses. The other coil (hereunto refered to as the Sense Coil) is connected in a closed loop to the GCT (Generator Current Transformer) located in the E&E bay. In KW operating mode, the reference coil is connected to phase B of the essential AC bus, with the other side of the coil being grounded. The sense coil is connected to the phase B GCT, and presumably has an in-phase 400hz of unknown amplitude. Most likely the ratio of amplitude between the two coils is what drives the gauge. In KVAR operating mode the sense coil configuration is unchanged. The reference coil is now connected on one side to phase C of the essential AC bus, and the other side is connected via a series resistor, to phase A of the same bus. This presumably provides an out-of-phase reference, to which the sensing coil will cause the needle to move based on out-of-phase current. The signal being driven on the sense coil is not changed depending on display mode, and therefore the logic to show KVAR should be handled internally within the aircraft. It is not clear if driving this single sense coil will be able to provide an accurate simulated KVAR value, as the KVAR reference seems to be the primary driving factor of the gauge, which is not able to be controled. It is possible that simulating KVAR is not possible without modification of the wiring to this gauge. 

_________________________________
**QUIRKS**

This gauge is sealed with a rubber gasket around the back circular plate. To disassemble, remove the 4 flathead screws on the radius of the gauge and pull the internals out from the back. To re-install, align the black sheath with the screw holes on the case. Loosen but do not fully remove the 3 large flathead screws on the circular back plate. Slide the internals in until the 4 radius screwholes align. Screw in the 4 radial screws to secure the internals. The back plate will not be fully seated. Screw in each of the 3 screws on the back plate a little at a time, cycling between the 3 screws to apply even pressure. As these screws and screwed in, the back plate will be pulled into the case and will seal the unit. It is advised to do this in a low humidity environment to avoid trapping moisture. 