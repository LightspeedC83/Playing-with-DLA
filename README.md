# Playing with DLA
This is a program that uses diffusion limited aggregation to create images.
The premise is that you start with a point on a plane and a candidate point is moved randomly until it meets another point, then the candidate point is frozen in place and a new candidate point is created. Candidate points are initialized to a random empty location. For more information on DLA, [refer to the wikipedia](https://en.wikipedia.org/wiki/Diffusion-limited_aggregation).


## Output examples

### Candidate point freezes only if one of the top, bottom, left, right spaces (ie. the adjacent spaces) is occupied
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/output%20-diagonals%3Dfalse.jpg)

### Candidate point freezes if any space in a square around it (ie. adjacent and diagonal) is occupied
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/output%20-diagonals%3Dtrue.jpg)


## Optimizing the process with expansion
If you want to generate a large image using DLA, it is very inefficient to start with one point on that large space and randomly move the candidate point around. As the canvas size gets bigger, the less likely it is that the candidate point finds its way to the other points in a timely manner. The solution that I implemented (in the code, called "expansion_optimization") starts the DLA process with a small image and grows the points in it according to the rules of DLA until it reaches the desired density, then the borders of the space are increased by a fixed amount and the DLA process continues until the desired density is again reached. This process is repeated until the canvas space reaches the size of the desired resolution. Expanding only when the desired density is reached, ensures that said density is uniform throughout. 

I tested the efficiency of this method compared to the alternative of a fixed canvas size throughout the DLA process at a resolution of 300x300 pixels and using the expansion optimization algorithm above, it took 49 seconds. Without the optimization, it took 8 minutes and 24 seconds. This marks a 928.6% increase in efficiency. Note that in the aforementioned test, the desired density for both generations was 0.15 and the candidate point did not lock on the diagonal. This test shows that the expansion optimization algorithm is vastly more efficient than the base DLA method, the difference would be even greater at larger resolutions.

To further improve the optimization of this approach, I made it such that the growth constant decreases every time the canvas space is expanded until it reaches 1. Becuase as the canvas space gets bigger, one extra pixel added to each edge pixel results in more and more pixels added. So as the canvas size increases, the growth factor should decrease. The implementation of this part of the expansion optimization algorithm in the code is called "downscaling expansion". 

It should be noted that this expansion optimization process seems to produce images with higher densities at the center if the candidate point locks on the diagonal, than if it doesn't. (after a cursory glance, it doesn't seem to affect density in the images where the candidate point doesn't lock on the diagonal). 


## Bail out optimization
The idea behind bail out optimization is that the program gives up on walking a point around, if it has made a number of moves over a threshold. 
Bail out optimization seems to create a more "blob-y" output, that bears less resemblance to a brownian tree:
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/outputs_traditional_DLA/DLA%20output%20300x300%20-d%3D0.15%20-ld%3DFalse%20-eo%3DTrue%20-de%3DFalse%20-b%3DTrue%20-bt%3D100%20-ts%3DFalse%20-23.4s.jpg)

## Further Optimization without simulating Brownian motion
To generate the Brownian Trees produced by DLA faster, we abandon the simulation of Brownian motion in favor of a less random approach. Instead of having a candidate point move randomly until it finds another point, we pick a random point from the existing points already placed and place a new point at a random empty space next to said point. However, this basic implementation does not generate a Brownian tree, it instead creates an expanding blob.

The simplistic approach outlined above generates the following: (decidedly not a Brownian Tree)
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/self_propelled_approach_test_1.jpg)

To be fair, it did generate the image *very* quickly...

## decoding the output file names
- {number}x{number} --> image resolution
- -d={number} --> point density (ie. points placed / total canvas space)
- -ld={boolean} --> whether or not a candidate will lock when in diagonal contact with another point
- -eo={boolean} --> whether or not the output was generated using the expansion optimization algorithm
- -de={boolean} --> whether or not the expansion optimization algoirithm used downscaling expansion
- -b={boolean} --> whether or not the output was generated using bail out optimization
- -bt={number} --> the bailout time (ie. number of moves before a point was bailed out on)
- -ts={boolean} --> whether or not the image uses time shading (if true, the color of points placed approaches white in the order in which they were placed)
- -{number}s --> the number of seconds it took to generate the output


## To Do:
- fix wraparound issue (i think it happens with image conversion)
- fix non black and white pixel issue
- ~~implement scaling depending on the desired resolution to increase generation speed~~
    - ~~ie. when it starts, have a small box, when that box reaches desired density, add white space around edges, repeat until at desired resolution and density~~
    - ~~fix putdata issue from result (is there even an issue?)~~
- implement mp4 creation of building structure
- devise an alternate optimization solution where the program keeps track of the edge points and then picks a random edge point, next to which to add a new point

To Do (Later):
- mulitple candidate points at once
- change collision detection system to mirror cellular automota (ie. use binary rules to govern whether a space around the candidate point is occupied and the candidate point should therefore freeze)
    - seems unecessary (?)
- if a point is moved a certain number of times, it freezes and then a new point is created, leading to the creation of multiple "crystals"
    - would have to not use in the expansion optimizaiton simulations (expansion optimization wouldn't help significantly in this case)
- variation of the nucleation points (ie. points in the starting state)
- addition of new nucleation points in the middle of building the crystal such that multiple, crystals of different sizes are created 
- some sort of user interface to make it easy to set starting conditions and rules for generation
- implement non-random movement and/or generation of candidate points (for example, have them start on one side of the canvas and move in a certain direction with random variation whose weight can be changed)

