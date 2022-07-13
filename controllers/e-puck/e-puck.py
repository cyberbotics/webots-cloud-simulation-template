# Copyright 1996-2022 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from controller import Robot

WHEEL_RADIUS = 0.02
AXLE_LENGTH = 0.052
RANGE = (1024 / 2)

def computeOdometry(leftPositionSensor, rightPositionSensor):
  l = leftPositionSensor.getValue()
  r = rightPositionSensor.getValue()
  dl = l * WHEEL_RADIUS         # distance covered by left wheel in meter
  dr = r * WHEEL_RADIUS         # distance covered by right wheel in meter
  da = (dr - dl) / AXLE_LENGTH  # delta orientation
  print('estimated distance covered by left wheel: ' +  dl + ' m.\n')
  print('estimated distance covered by right wheel: ' +  dr + ' m.\n')
  print('estimated change of orientation: % ' +  da + ' rad.\n')

braitenbergCoefficients = [(0.942, -0.22), (0.63, -0.1), (0.5, -0.06),  (-0.06, -0.06),
                                           (-0.06, -0.06), (-0.06, 0.5), (-0.19, 0.63), (-0.13, 0.942)]

# initialize Webots
robot = Robot()

if robot.getModel() == 'GCtronic e-puck2':
  print('e-puck2 robot\n')
  time_step = 64
  camera_time_step = 64
else: # original e-puck
  print("e-puck robot\n")
  timeStep = 256
  cameraTimeStep = 1024

# get and enable the camera and accelerometer
camera = robot.getDevice('camera')
camera.enable(cameraTimeStep)
accelerometer = robot.getDevice('accelerometer')
accelerometer.enable(timeStep)

# get a handler to the motors and set target position to infinity (speed control).
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('+inf'))
rightMotor.setPosition(float('+inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

# get a handler to the position sensors and enable them.
leftPositionSensor = robot.getDevice('left wheel sensor')
rightPositionSensor = robot.getDevice('right wheel sensor')
leftPositionSensor.enable(timeStep)
rightPositionSensor.enable(timeStep)

for i in range(8):
  # get distance sensors
  deviceName = 'ps' + i
  distanceSensor = []
  distanceSensor.append(robot.getDevice(deviceName)) 
  distanceSensor[i].enable(timeStep)


# main loop
while robot.step(timeStep) != -1:
  sensorsValue = []
  # get sensors values
  for i in range(8):
    sensorsValue[i] = distanceSensor[i].getValue()
  a = accelerometer.getValues()
  print('accelerometer values = ' + a[0] + ' ' + a[1] + ' ' + a[2])

  # compute odometry and speed values
  computeOdometry(leftPositionSensor, rightPositionSensor)
  speed = []
  for i in range(2):
    speed[i] = 0.0
    for j in range(8):
      speed[i] += braitenbergCoefficients[j][i] * (1.0 - (sensorsValue[j] / RANGE))
  
  # set speed values
  leftMotor.setVelocity(speed[0])
  rightMotor.setVelocity(speed[1])

robot.cleanup()