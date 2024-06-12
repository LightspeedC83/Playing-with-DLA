import random
from PIL import Image
import time
import math



# creating the point class system
class Point():
    def __init__(self, x_pos, y_pos, timestamp=0):
        self.x = x_pos
        self.y = y_pos
        self.timestamp = timestamp
        self.immediate_neighbors = 0

    def update_adjacents(self):
        self.immediate_neighbors = 0
        for y in range(self.y-1, self.y+2):
            for x in range(self.x-1, self.x+2):
                try:
                    if points[y][x] != None and self.y != y and self.x != x:
                        self.immediate_neighbors +=1
                        points[y][x].immediate_neighbors += 1
                except IndexError:
                    pass # consider (in the future) considering a edge point to have occupied neighbors off the canvas instead of free ones (in that case, you'd incriment immediate neighbors in the case of an index error)

            
# function declarations
def crude_print(points):
    """prints the output list in the terminal with a . for an empty space and a # for a filled space"""
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
x_res = 500
y_res = 500
target_density = 0.65

# setting the program's initial state
points = [[None for x in range(x_res)] for y in range(y_res)] # the canvas space with point objects for points and None objects for empty spaces
only_points = [Point(x_res//2, y_res//2)] # a list of all the point objects that have an adjacent free space

points[y_res//2][x_res//2] = only_points[0] # putting the seed point in the points list at the center of the canvas space

seed_point = only_points[0] # keeping track of the seed point


# starting the main loop
point_space = x_res*y_res
density = 1/point_space
points_placed = 1
start_time = time.time()
timestamp = 1

first_digit = ""
while density < target_density:

    # choosing a point to add onto
    while True:
        
        try:
            # Selecting a point in the structure onto which to add a new adjacent point
            #here we are going to try only selecting points with less than or equal to 4 occupied neighbors 
            candidate = random.choice(only_points)
            if candidate.immediate_neighbors >= 3: # not considering a point if it has more than 3 immediate neighbors
                only_points.remove(candidate)
                continue

            # choosing what adjacent square will be populated with a new point
            candidates = []
            for possible in [(candidate.x-1,candidate.y), (candidate.x+1, candidate.y), (candidate.x, candidate.y-1), (candidate.x, candidate.y+1)]: # going through the neighbors of the selected candidate
                if points[possible[1]][possible[0]] == None:
                    candidates.append(possible)
            
            if len(candidates) == 0: # if there are no free neighbors
                only_points.remove(candidate)
                
            else:
                
                # creating a list of coordinates, sorted by distance from the seed point
                indexed_candidates = [(candidates[0], math.sqrt((candidates[0][0]-seed_point.x)**2 + (candidates[0][1]-seed_point.y)**2))]
                for point in candidates[1:]:
                    
                    distance = math.sqrt((point[0]-seed_point.x)**2 + (point[1]-seed_point.y)**2)
                    insertion_index = 0
                    inserted = False
                    for i in range(len(indexed_candidates)):
                        if indexed_candidates[i][1] > distance:
                            candidates.insert(i, (point, distance))
                            inserted = True
                            break

                    if not inserted:
                        indexed_candidates.append((point, distance))

                
                # picking a point with a weight to prefer those farthest from the center
                weights = [int(x*(100/len(indexed_candidates))) for x in range(1,len(indexed_candidates)+1)] # making a list of weights that get heavier as the index is higher
                chosen_index = random.choices([x for x in range(len(indexed_candidates))], weights)[0]
                location = indexed_candidates[chosen_index][0]
                new_point = Point(location[0], location[1], timestamp)

                # updating the state variables and restarting the loop
                only_points.append(new_point)
                points[location[1]][location[0]] = new_point
                new_point.update_adjacents()
                break
                

        except:
            pass

    # giving user update every 10 seconds
    
    if ((time.time()-start_time)//1)%10 == 0 and str(time.time()-start_time)[0:1] != first_digit: # generation updates for if you're not using expansion optimization algorithm
        print(f"{str(density/target_density)[0:4]}, {str(time.time()-start_time)[0:4]}s")
        first_digit = str(time.time()-start_time)[0:1]
        
    
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