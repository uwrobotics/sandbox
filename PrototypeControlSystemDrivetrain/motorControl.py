from flask import Flask
from flask import request

import time
import atexit
import RPi.GPIO as IO

app = Flask(__name__)

IO.setmode(IO.BCM)
IO.setup(14,IO.OUT)
IO.setup(15,IO.OUT)
p = IO.PWM(14,100)
dutyCycle = 0
p.start(dutyCycle)
maxSpd = 255.0

@app.route('/')
def web_interface():
  html = open('web_interface.html')
  response = html.read().replace('\n', '')
  html.close()
  return response

@app.route('/set_speed')
def set_speed():
  speed = request.args.get('speed')
  print ('Received ' + str(speed))
  dutyCycle = round(int(speed)/maxSpd * 100)
  
  if dutyCycle < 0:
      IO.output(15,1)
      dutyCycle = -dutyCycle
      
  elif dutyCycle>=0:
      IO.output(15,0)
      
  
  p.ChangeDutyCycle(dutyCycle)
  return 'Received ' + str(speed)

@app.route('/', methods=['POST'])
def write_msg():
  x = request.form.get('x')
  y = request.form.get('y')
  print ('x = ' + str(x))
  print ('y = ' + str(y))
  
  dutyCycle = round(float(y) * 100)
  
  if dutyCycle < 0:
      IO.output(15,1)
      dutyCycle = -dutyCycle
      
  elif dutyCycle>=0:
      IO.output(15,0)
      
  
  p.ChangeDutyCycle(dutyCycle)
  
  return 'x = ' + str(x) + ', y = ' + str(y)

def main():
  app.run(host= '0.0.0.0')

main()
atexit.register(IO.cleanup)