#Run this beforehand: sudo ip route add 224.0.0.0/4 dev wlan0

import socket
import struct
import RPi.GPIO as IO

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
IS_ALL_GROUPS = True

pwm_freq = 1500
pin_pwm_left = 13
pin_pwm_right = 12
pin_dir_left = 5
pin_dir_right = 6

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
    print("Left -> " + str(left) + " | Right -> " + str(right))
    left = int((left - 127)/127*100)
    right = int((right - 127)/127*100)
    print("Left -> " + str(left) + " | Right -> " + str(right))
    if(left < 0):
        IO.output(pin_dir_left, 1)
    else:
        IO.output(pin_dir_left, 0)

    if(right < 0):
        IO.output(pin_dir_right, 1)
    else:
        IO.output(pin_dir_right, 0)

    PWM_LEFT_OBJ.ChangeDutyCycle(abs(left))
    PWM_RIGHT_OBJ.ChangeDutyCycle(abs(right))       

init_socket()   

while True:
  # For Python 3, change next line to "print(sock.recv(10240))"      
  packet = sock.recv(10240)
  decoded_msg = data_struct.unpack(packet)
  update_duty_cycle(decoded_msg[0], decoded_msg[1])
