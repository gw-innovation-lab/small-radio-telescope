For the Small Radio Telescope's control box:

MainCode: has the first working code for the Arduino that:
	-Takes in a string from the Pi over a Serial connection
	-Converts strings from ASCII to decimal that produces 
		variables for: direction, number of reed 
		switch pulses to determine location, and 
		PWM speed.
	-Takes these variables and inputs them into a "Move" 
		function that sends commands to a 
		Pololu TB67H420FTG Dual/Single Motor 
		Driver Carrier that will act as an
		H-Bridge motor driver, allowing current
		to flow either direction as needed.

MainCodeV2: basically the same with updated comments and a little
	    cleaner code through the Move function in the code.

MainCodeV3: Now with PWM speed!

MainCodeV4: Has implemented a Go Home function. It also changed the
	    the first input in the string from direction to order.
	    pickFunction will the be the intermediate that feeds
	    direction from the serial read to the Move function. 
		
	
	