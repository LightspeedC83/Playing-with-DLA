import random

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
        for h in range(self.x -1, self.x +2):
            for v in range(self.y -1, self.y +2):
                if h != self.x and v != self.y:
                    try:
                        val = points[h][v]
                        if val != None:
                            return True 
                    except: 
                        pass
        return False


# function declarations
def crude_print():
    output = ""
    for line in points:
        for point in line:
            if point == None:
                output += "0 "
            else:
                output += "1 "
        output += "\n"
    print(output)

# creating the list to keep track of the points
x_resolution = 21
y_resolution = 21

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

crude_print()