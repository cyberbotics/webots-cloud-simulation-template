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

distanceSensors = []

# initialize Webots
robot = Robot()

if robot.getModel() == 'GCtronic e-puck2':
  print('e-puck2 robot\n')
  timeStep = 64
else: # original e-puck
  print("e-puck robot\n")
  timeStep = 256

# get a handler to the motors and set target position to infinity (speed control).
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('+inf'))
rightMotor.setPosition(float('+inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

for i in range(8):
  # get distance sensors
  deviceName = 'ps' + str(i)
  distanceSensors.append(robot.getDevice(deviceName))
  distanceSensors[i].enable(timeStep)

# main loop
while robot.step(timeStep) != -1:
  sensorsValues = []
  # get sensors values
  for i in range(8):
    sensorsValues.append(distanceSensors[i].getValue())

  # go forward until reaching a wall
  speed = []
  for i in range(2):
    if sensorsValues[0] > 100:
      speed.append(0.0)
    else:
      speed.append(3.0)
  
  # set speed values
  leftMotor.setVelocity(speed[0])
  rightMotor.setVelocity(speed[1])

robot.cleanup()
