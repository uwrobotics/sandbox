import control_joystick
import socket
import time
import math

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
# regarding socket.IP_MULTICAST_TTL
# ---------------------------------
# for all packets sent, after two hops on the network the packet will not 
# be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

#control_joystick inits
controller = control_joystick.joystick_inits()

def arcade_to_tank(inputs: list) -> list:
    """Returns tank drive outputs from an arcade drive input, performs some inverse kinematics"""

    xSpeed = inputs[0]
    zRotation = inputs[1] 
    print("X Speed -> " + str(xSpeed), " | zRot -> " + str(zRotation))
    leftSpeed = 0
    rightSpeed = 0
    maxInput = math.copysign(max(abs(xSpeed), abs(zRotation)), xSpeed)

    if(xSpeed >= 0.0):
        if(zRotation >= 0.0):
            leftSpeed = maxInput
            rightSpeed = xSpeed - zRotation
        else:
            leftSpeed = xSpeed + zRotation
            rightSpeed = maxInput
    else:
        if(zRotation >= 0.0):
            leftSpeed = xSpeed + zRotation
            rightSpeed = maxInput
        else:
            leftSpeed = maxInput
            rightSpeed = xSpeed - zRotation

    maxMagnitude = max(abs(leftSpeed), abs(rightSpeed))
    if(maxMagnitude > 1.0):
        leftSpeed /= maxMagnitude
        rightSpeed /= maxMagnitude
    
    leftSpeed = leftSpeed*127 + 127
    rightSpeed = rightSpeed*127 + 127

    return [int(leftSpeed), int(rightSpeed)]    
    
def create_packet_from_list(tank_outputs: list):
    packet = bytearray()
    packet.append(tank_outputs[0])
    packet.append(tank_outputs[1])
    print(packet)
    return packet

while True:
    joystick_inputs = control_joystick.read_from_joystick(controller)
    del joystick_inputs[-1]
    tank_outputs = arcade_to_tank(joystick_inputs)
    print(tank_outputs)
    packet = create_packet_from_list(tank_outputs)
    # For Python 3, change next line to 'sock.sendto(b"robot", ...' to avoid the
    # "bytes-like object is required" msg (https://stackoverflow.com/a/42612820)
    sock.sendto(packet, (MCAST_GRP, MCAST_PORT))
    print("======")
    time.sleep(0.05)

