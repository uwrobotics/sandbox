# DriveTrain Prototype Control System

## Steps to setup your laptop as a base station
- Install Python3.8+ on your system
- Run `python3 -m pip install pygame pyserial`
- For Windows users: Install Git-SCM (link: https://git-scm.com/downloads) - the goal of this is to get bash

## Running the drivetrain
- Connect to the "drivetrain" wifi network, password is "drivetrain"
- Connect the joystick into your computer's USB port
- SSH into the raspberry pi by typing `ssh pi@192.168.4.1`, the password is `raspberry`
- Run `bash drivetrain.sh` script on the Pi
- Run `python3 basestation.py` on the base station computer to run the base station
- Have fun!