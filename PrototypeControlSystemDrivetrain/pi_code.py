#Run this beforehand: sudo ip route add 224.0.0.0/4 dev wlan0

import socket
import struct
import RPi.GPIO as IO
import time
from mcp3008 import MCP3008
import threading
from datetime import datetime
import csv

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
IS_ALL_GROUPS = True

pwm_freq = 1500
pin_pwm_left = 13
pin_pwm_right = 12
pin_dir_left = 5
pin_dir_right = 6
timeout_s = 0.2

data_struct = struct.Struct('>BB')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

def init_socket():
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if IS_ALL_GROUPS:
        # on this port, receives ALL multicast groups
        sock.bind(('', MCAST_PORT))
    else:
        # on this port, listen ONLY to MCAST_GRP
        sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.settimeout(timeout_s)

IO.setmode(IO.BCM) #set pin mappings
IO.setup(pin_pwm_left, IO.OUT)
IO.setup(pin_dir_left, IO.OUT)
PWM_LEFT_OBJ = IO.PWM(pin_pwm_left, pwm_freq)
PWM_LEFT_OBJ.start(0)
IO.setup(pin_pwm_right, IO.OUT)
IO.setup(pin_dir_right, IO.OUT)
PWM_RIGHT_OBJ = IO.PWM(pin_pwm_right, pwm_freq)
PWM_RIGHT_OBJ.start(0)

def update_duty_cycle(left:int, right:int):
    """0 - 255, 127 deadpoint"""
    left = int((left - 127)/127*100)
    right = int((right - 127)/127*100)
    #print("Left -> " + str(left) + " | Right -> " + str(right))
    if(left < 0):
        IO.output(pin_dir_left, 0)
    else:
        IO.output(pin_dir_left, 1)

    if(right < 0):
        IO.output(pin_dir_right, 1)
    else:
        IO.output(pin_dir_right, 0)

    PWM_LEFT_OBJ.ChangeDutyCycle(abs(left))
    PWM_RIGHT_OBJ.ChangeDutyCycle(abs(right))       

init_socket()

adc = MCP3008()
f = open("current_log_drivetrain.txt", "a")
writer = csv.writer(f)
writer.writerow(['Time', 'Channel', 'Voltage'])
summed_voltages = 0
number_of_samples = 0
peak_voltage = 0
neutral = 3.3/2
def read_current(channel: int):
    value = adc.read(channel)
    voltage = abs(neutral - (value / 1023.0 * 3.3))
    t = time.localtime()
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    string = f"Time: {current_time} | Channel: {channel} | Applied voltage: {voltage}\n"
    #print(string)
    writer.writerow([current_time, channel + 1, (value / 1023.0 * 3.3)])

    #Current Calcs
    global number_of_samples
    global summed_voltages
    global peak_voltage
    number_of_samples += 1
    summed_voltages += voltage
    if(voltage > peak_voltage):
        peak_voltage = voltage
    print(f"Average Current: {convert_voltage_to_torque(summed_voltages/number_of_samples)} | Peak Current: {convert_voltage_to_torque(peak_voltage)}")

def convert_voltage_to_torque(voltage):
    return voltage * 25

def read_current_thread():
    for i in range(0, 6):
        read_current(i)

deadband = 8
print("Starting RC drivetrain application!")
while True:
  try:
    packet = sock.recv(10240)
    decoded_msg = data_struct.unpack(packet)
    left = decoded_msg[0]
    right = decoded_msg[1]
    if((left > 127 + deadband or left < 127 - deadband) or (right > 127 + deadband or right < 127 - deadband)):
        update_duty_cycle(left, right)
        read_current_thread()
    else:
        update_duty_cycle(127, 127)
  except socket.timeout:
      print("Drivetrain stopped - no input received")
      update_duty_cycle(127, 127) #Stop driving if transmissions stop

  
