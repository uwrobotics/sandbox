## Set Up Instructions

1. * Copy and paste `arm-pid.ino` into the Arduino IDE and deploy it onto the Arduino Mega. 
    * On the Arduino IDE, Make sure that the selected board is the Arduino Mega and that the processor is ATMega2560

2. * Open the arm-pid directory in a terminal and run  `python3 pid-tuning-ui.py` to open the GUI
    * Make sure to specify the correct Arduino port on line 23 of `pid-tuning-ui.py`. The port name can be found in the Arduino IDE when the Arduino is plugged in.

3. * Turn on power supply for motors and start controlling the arm with the buttons on the UI. Make sure to have a kill switch in reach

Note: Python project MUST be closed before deploying code to the Arduino.

sorry for jank lmao