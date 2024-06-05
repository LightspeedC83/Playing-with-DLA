import random
from PIL import Image

locks_on_diagonal = True

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
                output += "0 "
            else:
                output += "1 "
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



# creating the list to keep track of the points
x_resolution = 10
y_resolution = 10

points = [[None for x in range(x_resolution)] for y in range(y_resolution)] #the list to keep track of the points

# setting the initial state of the system
points[x_resolution//2][y_resolution//2] = Point(x_resolution//2, y_resolution//2) # placing one point

# starting the main loop
target_density = 0.15
points_placed = 1
density = 1/(x_resolution*y_resolution)
timestamp = 1



while density < target_density:
    # creating a new point object at a random empty locaiton
    while True:
        rand_x = random.randint(0, x_resolution-1)
        rand_y = random.randint(0, y_resolution-1)
        
        if points[rand_x][rand_y] == None:
            new_point = Point(rand_x, rand_y, timestamp)
            points[rand_x][rand_y] = new_point
            break
    
    # moving the point just created 
    while not new_point.is_locked(points):
        possible_points  = [] # nb: there's probably a better way to find a random possible point, but idc rn
        for x in range(new_point.x-1, new_point.x+2):
            for y in range(new_point.y-1, new_point.y+2):
                try:
                    if points[x][y] == None:
                        possible_points.append([x,y])
                except: 
                    pass
        new_point.move(points, random.choice(possible_points))
    
    
    # recalculating density and restarting loop
    points_placed +=1
    density = points_placed/(x_resolution*y_resolution)

    timestamp +=1 

# crude_print()

# converting the points list to an image
pixels = []
for line in points:
    for point in line:
        if point != None:
            pixels.append((0,0,0))
        else:
            pixels.append((255,255,255))

# saving the output image
output = Image.new(mode="RGB", size=(x_resolution,y_resolution))
output.putdata(pixels)
output.save(f"DLA output {x_resolution}x{y_resolution} -target_density={target_density} -locks_on_diagonal={locks_on_diagonal}.jpg") 

print("done")