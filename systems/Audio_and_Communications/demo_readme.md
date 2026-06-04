Demo Audio Setup demo_readme.md

The audio demo setup consists of a single ACP, headphone jack, headset, scarlett audio interface, DC mic bias board and demo computer. The demo is a smaller version of the audio system on the plane with some more limited functionality. The purpose is to demonstrate the basic functionality of the audio system by providing multiple channels which can be used to transmit and receive audio via the headset. 

Architecture: The ACP is wired into the headphone jack via a wire harness using canon plugs on the ACP end. The headphone jack has exposed pins and must be plugged in manually per the connection list below. The DC mic bias board is connected in-line with any microphone channels, between the ACP and the TRS plug. Interfacing to the scarlett is done via TRS plugs connected to the wire harness. Each audio channel is mono with each plug containing two channels. Power is provided from an external 28v DC supply to the ACP, and a 12v DC supply to the DC bias board. All grounds are common and shared on a 5-gang wago connector. The TRS plugs are connected to the scarlett via the TRS input and outputs. PTT is wired from the headphone jack to the ACP and all logic is contained internally in the ACP. There are no control signals used in this demo. 

Software: The only software required to run this demo is JJ Audio Boss using the scarlett demo config file. This is designed to run on the demo computer using VB cable for virtual cables. 

Pinout: 
	ACP: 
	Headphone Jack: 