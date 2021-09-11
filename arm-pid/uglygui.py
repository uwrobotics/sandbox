import PySimpleGUI as sg
import serial




def main():
    layout = [
      [sg.Text('Current1:                                                  ', font='Ariel 24', key='-c1-')],
      [sg.Text('Current2:                                                  ', font='Ariel 24', key='-c2-')],
      [sg.Text('Current3:                                                  ', font='Ariel 24', key='-c3-')],
      [sg.Text('Current4:                                                  ', font='Ariel 24', key='-c4-')],
      [sg.Text('Current5:                                                  ', font='Ariel 24', key='-c5-')],
      [sg.Text('Current6:                                                  ', font='Ariel 24', key='-c6-')],
    ]

    window = sg.Window('UGLY UI', layout, location=(800, 400))

    while True:
        
        event, values = window.read(timeout=20)

        
        current1 = 0
        current2 = 0
        current3 = 0
        current4 = 0
        current5 = 0
        current6 = 0

        window['-c1-'].update('Current1: ' + str(current1) + "A")
        window['-c2-'].update('Current2: ' +  str(current2) + "A")
        window['-c3-'].update('Current3: ' +  str(current3) + "A")
        window['-c4-'].update('Current4: ' +  str(current4) + "A")
        window['-c5-'].update('Current5: ' +  str(current5) + "A")
        window['-c6-'].update('Current6: ' +  str(current6) + "A")


        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

    window.close()


main()