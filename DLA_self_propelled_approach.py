import random
from PIL import Image
import time



# creating the point class system
class Point():
    def __init__(self, x_pos, y_pos, timestamp=0):
        self.x = x_pos
        self.y = y_pos
        self.timestamp = timestamp


# function declarations
def crude_print(points):
    """prints the output list in the terminal with a 0 for an empty space and a 1 for a filled space"""
    output = ""
    for line in points:
        for point in line:
            if point == None:
                output += ". "
            else:
                output += "# "
        output += "\n"
    print(output)


# key controlling variables
x_res = 200
y_res = 200
target_density = 0.15

# setting the program's initial state
points = [[None for x in range(x_res)] for y in range(y_res)] # the canvas space with point objects for points and None objects for empty spaces
only_points = [Point(x_res//2, y_res//2)] # a list of all the point objects 

points[y_res//2][x_res//2] = only_points[0] # putting the seed point in the points list at the center of the canvas space


# starting the main loop
point_space = x_res*y_res
density = 1/point_space
points_placed = 1
start_time = time.time()
timestamp = 1

while density < target_density:

    # choosing a point to add onto
    while True:
        try:
            candidates = []
            candidate = random.choice(only_points)
            for possible in [(candidate.x-1,candidate.y), (candidate.x+1, candidate.y), (candidate.x, candidate.y-1), (candidate.x, candidate.y+1)]:
                if points[possible[1]][possible[0]] == None:
                    candidates.append(possible)
            
            if len(candidates) == 0:
                only_points.remove(candidate)
            else:
                location = random.choice(candidates)
                new_point = Point(location[0], location[1], timestamp)
                only_points.append(new_point)
                points[location[1]][location[0]] = new_point
                break

        except:
            pass

    # giving user update every 10 seconds
    if ((time.time()-start_time)//1)%10 == 0 and (time.time()-start_time)//1 != 0: # generation updates for if you're not using expansion optimization algorithm
        print(f"{str(density/target_density)[0:4]}, {str(time.time()-start_time)[0:4]}s")
    
    # preparing to restart the loop
    timestamp +=1
    points_placed +=1
    density = points_placed/point_space


# converting the points list to an image
pixels = []
for line in points:
    for point in line:
        # assigning points to be black with a white background
        if point != None:
            pixels.append((0,0,0))
        else:
            pixels.append((255,255,255))

# saving the ouptut
print("saving the output image")
output = Image.new(mode="RGB", size=(len(points[0]),len(points)))
output.putdata(pixels)
output.save(f"outputs_self_propelled_approach\DLA output {x_res}x{y_res} -density={target_density} -generated in {str(time.time()-start_time)[0:4]}s.jpg")

print(f"done in {str(time.time()-start_time)[0:4]}s")