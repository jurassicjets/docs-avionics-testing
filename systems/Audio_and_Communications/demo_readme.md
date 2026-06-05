Demo Audio Setup demo_readme.md

SUMMARY:
The audio demo setup consists of a single ACP, headphone jack, headset, scarlett audio interface, DC mic bias board and demo computer. The demo is a smaller version of the audio system on the plane with some more limited functionality. The purpose is to demonstrate the basic functionality of the audio system by providing multiple channels which can be used to transmit and receive audio via the headset.

ARCHITECTURE: 
The ACP is wired into the headphone jack via a wire harness using canon plugs on the ACP end. The headphone jack has exposed pins and must be plugged in manually per the connection list below. The DC mic bias board is connected in-line with any microphone channels, between the ACP and the TRS plug. Interfacing to the scarlett is done via TRS plugs connected to the wire harness. Each audio channel is mono with each plug containing two channels. Power is provided from an external 28v DC supply to the ACP, and a 12v DC supply to the DC bias board. All grounds are common and shared on a 5-gang waygo connector. The TRS plugs are connected to the scarlett via the TRS input and outputs. PTT is wired from the headphone jack to the ACP and all logic is contained internally in the ACP. There are no control signals used in this demo. 

SOFTWARE: JJ Audio Boss using the scarlett demo config file is used for the digital routing between windows programs and scarlett 18i20. This is designed to run on the demo computer using VB cable for virtual cables. Focusrite Control 2 is used to control routing and mixing within the scarlett. The scarlett is also used for sidetone injection via input-to-output routing. Sidetone is acomplished using mix 1. 

CONNECTIONS: 
	ACP: 
		single-waygo <=> 28v DC
		5-gang waygo <=> DC ground
		mic TRS <=> scarlett analog input 1, 2
		audio TRS <=> scarlett analog output 3, 4, 5, 6
	Headphone Jack: 
		pin 18 <=> ACP pin 16 (PTT)
		pin 20 <=> ACP pin 23 (GND)
		pin 24 <=> ACP pin 17 (Audio)
		pin 25 <=> ACP pin 18 (Audio Common)
		pin 26 <=> ACP pin 14 (Mic)
		pin 27 <=> ACP pin 13 (Mic Common)

ROUTING: 
	INPUTS: 
		Analog 1 - VHF1
		Analog 2 - VHF3
	OUTPUTS: 
		Analog 3 - VHF1
		Analog 4 - VHF3
		Analog 5 - VOR1
		Analog 6 - VOR2