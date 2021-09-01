import serial
import time
import control_joystick
import threading

baudRate = 115200
COMPORT = "COM6"
serialCon = serial.Serial(COMPORT, baudRate) #Create connection on serial port

def writeToSerial(packet):
    serialCon.write(packet)

def generate_packet(items_to_encode: list):
    packet = bytearray()
    for item in items_to_encode:
        packet.append(item)
    return packet

def readline():
    print(serialCon.readline())
    time.sleep(0.005) #Prevent thread overload

if __name__ == "__main__":
    control_joystick.joystick_inits()
    threading.Thread(readline)
    while True:
        control_outputs = control_joystick.read_from_joystick()
        writeToSerial(generate_packet(control_outputs)
        