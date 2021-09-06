import PySimpleGUI as sg
import serial
import time
import serial.tools.list_ports as ports

com_ports = list(ports.comports())  # create a list of com ['COM1','COM2']
for i in com_ports:
    print(i.device)  # returns 'COMx'

# HSV values
max_value = 255
max_value_H = 360
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
# time.sleep(3)

ser = serial.Serial('/dev/cu.usbmodem11301', 115200, timeout=.1)
print("Reset Arduino")
ser.write(bytes('cu.usbmodem11301', 'UTF-8'))


def isNumeric(string):
    result = False
    if(string.replace('.', '', 1).isdigit()):
        result = True
    return result


def main():
    sg.theme('LightGreen')
    low_H = 0
    low_S = 0
    low_V = 0
    high_H = max_value_H
    high_S = max_value
    high_V = max_value
    # define the window layout
    layout = [
      [sg.Image(filename='', key='-IMAGE-')],
      [sg.Text('Joint'), 
       sg.InputText("", size=(5, 5), key='-joint-')],
      [sg.Text('P'), 
       sg.InputText("", size=(5, 5), key='-P-')],
      [sg.Text('I'),
       sg.InputText("", size=(5, 5), key='-I-')],
      [sg.Text('D'),
       sg.InputText("", size=(5, 5), key='-D-')],
      [sg.Button('Submit')],
      [sg.Button('1⬆️'), sg.Button('2⬆️'), sg.Button('3⬆️'), sg.Button('4⬆️'), sg.Button('5⬆️'), sg.Button('6⬆️')],
      [sg.Button('1-'), sg.Button('2-'), sg.Button('3-'), sg.Button('4-'), sg.Button('5-'), sg.Button('6-')],
      [sg.Button('1⬇️'), sg.Button('2⬇️'), sg.Button('3⬇️'), sg.Button('4⬇️'), sg.Button('5⬇️'), sg.Button('6⬇️')],
    ]

    # Create the window
    window = sg.Window('PID Tuner', layout, location=(800, 400))

    # Start video stream
    # cap = cv2.VideoCapture(0)

    while True:
        
        event, values = window.read(timeout=20)

        joint = values['-joint-']
        p = values['-P-']
        i = values['-I-']
        d = values['-D-']
        
        print(ser.readline().decode().strip())
        ser.flushInput()
        ser.flushOutput()

        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Submit':
            ser.write(bytes(joint + "," + p + "," + i + "," + d, 'UTF-8'))
            # print(joint + "," + p + "," + i + "," + d)


        if event == '1⬆️':
            ser.write(bytes("1up", 'UTF-8'))
        if event == '1-':
            ser.write(bytes("1stop", 'UTF-8'))
        if event == '1⬇️':
            ser.write(bytes("1down", 'UTF-8'))

        if event == '2⬆️':
            ser.write(bytes("2up", 'UTF-8'))
        if event == '2-':
            ser.write(bytes("2stop", 'UTF-8'))
        if event == '2⬇️':
            ser.write(bytes("2down", 'UTF-8'))

        if event == '3⬆️':
            ser.write(bytes("3up", 'UTF-8'))
        if event == '3-':
            ser.write(bytes("3stop", 'UTF-8'))
        if event == '3⬇️':
            ser.write(bytes("3down", 'UTF-8'))

        if event == '4⬆️':
            ser.write(bytes("4up", 'UTF-8'))
        if event == '4-':
            ser.write(bytes("4stop", 'UTF-8'))
        if event == '4⬇️':
            ser.write(bytes("4down", 'UTF-8'))

        if event == '5⬆️':
            ser.write(bytes("5up", 'UTF-8'))
        if event == '5-':
            ser.write(bytes("5stop", 'UTF-8'))
        if event == '5⬇️':
            ser.write(bytes("5down", 'UTF-8'))

        if event == '6⬆️':
            ser.write(bytes("6up", 'UTF-8'))
        if event == '6-':
            ser.write(bytes("6stop", 'UTF-8'))
        if event == '6⬇️':
            ser.write(bytes("6down", 'UTF-8'))

        # while event = ''
    window.close()


main()