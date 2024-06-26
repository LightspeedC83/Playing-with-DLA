import random
from PIL import Image
import time

# controlling variables
target_density = 0.15

locks_on_diagonal = False
expansion_optimization = False
growth_const = 5
downscaling_expansion = False

if not expansion_optimization:
    downscaling_expansion = False

time_shading = False
bail_out_optimization = True
bail_out_time = 100

# creating the point class system
class Point():
    def __init__(self, x_pos, y_pos, timestamp=0):
        self.x = x_pos
        self.y = y_pos
        self.timestamp = timestamp

    def move(self, points, destination):
        """changes recorded (x,y) position to an inputted (x,y) destination AND moves the point object in the points 2D list"""
        points[destination[0]][destination[1]] = points[self.x][self.y]
        points[self.x][self.y] = None
        self.x = destination[0]
        self.y = destination[1]
        
    def is_locked(self, points):
        if locks_on_diagonal: # will return true if there is also a point diagonal to this point
            for h in range(self.x -1, self.x +2):
                for v in range(self.y -1, self.y +2):
                    if h != self.x and v != self.y:
                        try:
                            if points[h][v] != None:
                                return True 
                        except: 
                            pass
            return False
        
        else: # will return not true if there is also a point diagonal to this point
            for point in [(self.x-1,self.y), (self.x+1, self.y), (self.x, self.y-1), (self.x, self.y+1)]:
                try:
                    if points[point[0]][point[1]] != None:
                        return True
                except:
                    pass
            return False

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

def expand_array(points, addition):
    """takes a 2D array and adds None elements around the edges addition spaces out"""
    for j in range(addition):
        for i in range(len(points)):
            points[i].insert(0, None)
            points[i].append(None)
    
    for j in range(addition):
        points.insert(0, [None for x in range(len(points[0]))])
        points.append([None for x in range(len(points[0]))])

    return(points)



# setting the initial state
x_resolution = 200
y_resolution = 200

x_res_current = 10
y_res_current = 10


if not expansion_optimization:
    points = [[None for x in range(x_resolution)] for y in range(y_resolution)] #the list to keep track of the points
    
    x_res_current = x_resolution
    y_res_current = y_resolution

    # setting the initial state of the system with one point
    points[x_resolution//2][y_resolution//2] = Point(x_resolution//2, y_resolution//2) # placing one point

else:
    points = [[None for x in range(x_res_current)] for y in range(y_res_current)] # Starting with a small 2D canvas that will grow
     # setting the initial state of the system with one point
    points[x_res_current//2][y_res_current//2] = Point(x_res_current//2, y_res_current//2) # placing one point


# starting the main loop
points_placed = 1
density = 1/(x_res_current*y_res_current)
timestamp = 1

start_time = time.time()
time_expansion = time.time()
first_digit = ""

while True:
    
    # taking care of stuff for if we're using the expansion optimization process
    if expansion_optimization and density >= target_density and x_res_current >= x_resolution and y_res_current >= y_resolution:
        break
    
    if not expansion_optimization and density > target_density:
        break

    if expansion_optimization and density >= target_density:
        print(f"expanding... {x_res_current}/{x_resolution}, {str(time.time()-time_expansion)[0:4]}s") # generation updates for if expansion optimization is used
        time_expansion = time.time()
        points = expand_array(points, growth_const)
        x_res_current += 2*growth_const
        y_res_current += 2*growth_const

        # downscaling the growth constant by 1 each time the canvas expands
        if growth_const > 1 and downscaling_expansion:
            growth_const -=1    
    
    
    # creating a new point object at a random empty locaiton
    while True:
        rand_x = random.randint(0, x_res_current-1)
        rand_y = random.randint(0, y_res_current-1)
        
        if points[rand_x][rand_y] == None:
            new_point = Point(rand_x, rand_y, timestamp)
            points[rand_x][rand_y] = new_point
            break
    
    # moving the point just created 
    num_moves = 0
    while not new_point.is_locked(points):
        if num_moves > bail_out_time and bail_out_optimization: # bailing out if the candidate point has moved too much without settling
            points[new_point.x][new_point.y] = None
            points_placed -= 1
            break
        possible_points  = [] # nb: there's probably a better way to find a random possible point, but idc rn
        for x in range(new_point.x-1, new_point.x+2):
            for y in range(new_point.y-1, new_point.y+2):
                try:
                    if points[x][y] == None:
                        possible_points.append([x,y])
                except: 
                    pass
        new_point.move(points, random.choice(possible_points))
        num_moves += 1
    
    
    # recalculating density and restarting loop
    points_placed +=1
    density = points_placed/(x_res_current*y_res_current)

    timestamp +=1 

    if ((time.time()-start_time)//1)%10 == 0 and str(time.time()-start_time)[0:1] != first_digit and not expansion_optimization: # generation updates for if you're not using expansion optimization algorithm
        print(f"{str(density/target_density)[0:4]}, {str(time.time()-start_time)[0:4]}s")
        first_digit = str(time.time()-start_time)[0:1]

# converting the points list to an image
pixels = []
for line in points:
    for point in line:
        if time_shading: # assigning points a grayscale shade based on when they were added
            if point != None:
                val = int((point.timestamp / timestamp)*255//1)
                pixels.append((val,val,val))
            else:
                pixels.append((255,255,255))

        else: # assigning points to be black with a white background
            if point != None:
                pixels.append((0,0,0))
            else:
                pixels.append((255,255,255))

# saving the output image
print("saving the output image")
file_name = f"outputs_traditional_DLA\DLA output {x_resolution}x{y_resolution} -d={target_density} -ld={locks_on_diagonal} -eo={expansion_optimization} "
file_name += f"-de={downscaling_expansion} " if expansion_optimization else " "
file_name += f"-b={bail_out_optimization} " 
file_name += f"-bt={bail_out_time} " if bail_out_optimization else " " 
file_name += f"-ts={time_shading} -{str(time.time()-start_time)[0:4]}s.jpg"
print(file_name)

output = Image.new(mode="RGB", size=(len(points[0]),len(points)))
output.putdata(pixels)
output.save(file_name)

print(f"done in {str(time.time()-start_time)[0:4]}s")