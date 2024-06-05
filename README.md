# Playing with DLA
This is a program that uses diffusion limited aggregation to create images.
The premise is that you start with a point on a plane and a candidate point is moved randomly until it meets another point, then the candidate point is frozen in place and a new candidate point is created. Candidate points are initialized to a random empty location. For more information on DLA, [refer to the wikipedia][https://en.wikipedia.org/wiki/Diffusion-limited_aggregation].

## Output examples

### candidate point freezes only if one of the top, bottom, left, right spaces (ie. the adjacent spaces) is occupied
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/output%20-diagonals%3Dfalse.jpg)

### candidate point freezes if any space in a square around it (ie. adjacent and diagonal) is occupied
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/output%20-diagonals%3Dtrue.jpg)

To Do:
- fix wraparound issue (i think it happens with image conversion)
- fix non black and white pixel issue
- implement scaling depending on the desired resolution to increase generation speed
    - ie. when it starts, have a small box, when that box reaches desired density, add white space around edges, repeat until at desired resolution and density
- implement mp4 creation of building structure

To Do (Later):
- change collision detection system to mirror cellular automota (ie. use binary rules to govern whether a space around the candidate point is occupied and the candidate point should therefore freeze)
- if a point is moved a certain number of times, it freezes and then a new point is created, leading to the creation of multiple "crystals"
- variation of the nucleation points (ie. points in the starting state)
- addition of new nucleation points in the middle of building the crystal such that multiple, crystals of different sizes are created 
- some sort of user interface to make it easy to set starting conditions and rules for generation
- implement non-random movement and/or generation of candidate points (for example, have them start on one side of the canvas and move in a certain direction with random variation whose weight can be changed)
