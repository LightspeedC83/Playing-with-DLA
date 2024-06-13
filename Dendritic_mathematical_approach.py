"""
- have a bunch of vector objects, every iteration increase the magnitude of each vector by 1 pixel (if it is going to run into another vector object, terminate that vector object's growth)
- the longer a vector object survives without being terminated, the more likely it is to have a child branch come from it at a random angle intersecting it but <90 degrees
- repeat this process until the desired density is reached

"""

import random
import math

class Vector():
    def __init__(self, angle, start_point):
        self.angle = angle
        self.start_x = start_point[0]
        self.start_y = start_point[1]
        self.start_point = start_point
        self.magnitude = 0
        self.active = True 

# key controlling variables
x_res = 100
y_res = 100
render_res = 50

# starting the system by populating the vector object list with a random number of vectors with radial angles at the origin (which will be the seed point)
initial_branches = 6
vectors = []
for i in range(initial_branches):
    angle = random.randint(i*(360/initial_branches), (i+1)*(360/initial_branches)) #to assign an angle, it divides the circle into x number of pieces and each vector gets an random angle from inside their respective piece
    vectors.append(Vector(angle, (0,0)))

for x in range(100):
    for vector in vectors:
        vector.magnitude +=1

# creating an output list
canvas = [[0 for x in range(x_res)] for y in range(y_res)]

def draw_point(x,y):
    try:
        canvas[int(y_res//2 + x)][int(x_res//2 + y)] = 1 # canvas[y_res//2][x_res//2] will be the origin in the 2D array
        return True
    except IndexError:
        return False

# drawing the vectors
for vector in vectors:
    for i in range(1,render_res)[::-1]:
        result = draw_point(vector.start_x + vector.magnitude*math.cos((vector.magnitude/i)) , + vector.start_y + vector.magnitude*math.sin((vector.magnitude/i)))
        if not result:
            break

# printing the output
output = ""
for line in canvas:
    for point in line:
        if point == 0:
            output += ". "
        else:
            output += "# "
    output += "\n"
print(output)