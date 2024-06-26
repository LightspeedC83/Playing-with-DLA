# Playing with DLA
This is a program that uses diffusion limited aggregation to create images.
The premise is that you start with a point on a plane and a candidate point is moved randomly until it meets another point, then the candidate point is frozen in place and a new candidate point is created. Candidate points are initialized to a random empty location. The structures that are generated from this process are called "Brownian Trees", named for the Browinian motion that the candidate point simulates. For more information on DLA, [refer to the wikipedia](https://en.wikipedia.org/wiki/Diffusion-limited_aggregation).


## Output Examples

### Candidate point freezes only if one of the top, bottom, left, right spaces (ie. the adjacent spaces) is occupied
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/output%20-diagonals%3Dfalse.jpg)

### Candidate point freezes if any space in a square around it (ie. adjacent and diagonal) is occupied
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/output%20-diagonals%3Dtrue.jpg)


## Optimizing the Process with Expansion
If you want to generate a large image using DLA, it is very inefficient to start with one point on that large space and randomly move the candidate point around. As the canvas size gets bigger, the less likely it is that the candidate point finds its way to the other points in a timely manner. The solution that I implemented (in the code, called "expansion_optimization") starts the DLA process with a small image and grows the points in it according to the rules of DLA until it reaches the desired density, then the borders of the space are increased by a fixed amount and the DLA process continues until the desired density is again reached. This process is repeated until the canvas space reaches the size of the desired resolution. Expanding only when the desired density is reached, ensures that said density is uniform throughout. 

I tested the efficiency of this method compared to the alternative of a fixed canvas size throughout the DLA process at a resolution of 300x300 pixels and using the expansion optimization algorithm above, it took 49 seconds. Without the optimization, it took 8 minutes and 24 seconds. This marks a 928.6% increase in efficiency. Note that in the aforementioned test, the desired density for both generations was 0.15 and the candidate point did not lock on the diagonal. This test shows that the expansion optimization algorithm is vastly more efficient than the base DLA method, the difference would be even greater at larger resolutions.

To further improve the optimization of this approach, I made it such that the growth constant decreases every time the canvas space is expanded until it reaches 1. Becuase as the canvas space gets bigger, one extra pixel added to each edge pixel results in more and more pixels added. So as the canvas size increases, the growth factor should decrease. The implementation of this part of the expansion optimization algorithm in the code is called "downscaling expansion". 

It should be noted that this expansion optimization process seems to produce images with higher densities at the center if the candidate point locks on the diagonal, than if it doesn't. (after a cursory glance, it doesn't seem to affect density in the images where the candidate point doesn't lock on the diagonal). 


## Bail out Optimization
The idea behind bail out optimization is that the program gives up on walking a point around, if it has made a number of moves over a threshold. 
Bail out optimization seems to create a more "blob-y" output, that bears less resemblance to a brownian tree, but it does run much faster; in the following test, it ran 4.25x faster.
### 200x200 output without bailout optimizaiton, generated in 114s
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/outputs_traditional_DLA/DLA%20output%20200x200%20-d%3D0.15%20-ld%3DFalse%20-eo%3DFalse%20%20-b%3DFalse%20%20-ts%3DFalse%20-114.s.jpg)

### 200x200 output with bailout optimization, generated in 26.8 seconds (bailout time 100)
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/outputs_traditional_DLA/DLA%20output%20200x200%20-d%3D0.15%20-ld%3DFalse%20-eo%3DFalse%20%20-b%3DTrue%20-bt%3D100%20-ts%3DFalse%20-26.8s.jpg)

## Decoding the Output File Names
- {number}x{number} --> image resolution
- -d={number} --> point density (ie. points placed / total canvas space)
- -ld={boolean} --> whether or not a candidate will lock when in diagonal contact with another point
- -eo={boolean} --> whether or not the output was generated using the expansion optimization algorithm
- -de={boolean} --> whether or not the expansion optimization algoirithm used downscaling expansion
- -b={boolean} --> whether or not the output was generated using bail out optimization
- -bt={number} --> the bailout time (ie. number of moves before a point was bailed out on)
- -ts={boolean} --> whether or not the image uses time shading (if true, the color of points placed approaches white in the order in which they were placed)
- -{number}s --> the number of seconds it took to generate the output

## Attempts at Further Optimization Without Simulating Brownian Motion
To generate the Brownian Trees produced by DLA faster, we abandon the simulation of Brownian motion in favor of a less random approach. Instead of having a candidate point move randomly until it finds another point, we pick a random point from the existing points already placed and place a new point at a random empty space next to said point. However, this basic implementation does not generate a Brownian tree, it instead creates an expanding blob.

The simplistic approach outlined above generates the following: (decidedly not a Brownian Tree)
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/self_propelled_approach_test_1.jpg)

To be fair, it did generate the image *very* quickly...

The next thing I tried to make it look more like a brownian tree was to change the choce from being a random one to choosing a point that was farther away from the seed point.
This approach generated the following: (also decidely not a Brownian Tree, but maybe closer?)

![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/outputs_self_propelled_approach/DLA%20output%201000x1000%20-density%3D0.15%20-generated%20in%202.25s%20equal%20probability.jpg)

Okay, What if we choose a point with a probability weighted towards those farthest away from the seed point?

![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/outputs_self_propelled_approach/DLA%20output%20500x500%20-density%3D0.35%20-generated%20in%201.32s%20high%20weights.jpg)

This produces (depending on the weights) a shape somewhere between the "o" created by having a completely random choice and the "+" created by always choosing the farthest point.

The next thing I tried was to keep track of the number of points in the square around every point, in the code, I call points in this square the "immdiate neighbors". Instead of selecting a random point that has free square adjacent, it selects a random point that has less than 4 immediate neighbors (this is 1/2 the availiable neighbor space). This approach produces something with some internal variation, but still the same overall silhouette.

![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/outputs_self_propelled_approach/DLA%20output%20500x500%20-density%3D0.35%20-generated%20in%201.53s%20test%20selecting%20point%20with%20less%20than%204%20immediate%20neighbors.jpg)

If we instead have it select a random point with less than 3 immediate neighbors, there is more internal variation with a similar silhouette (1 or 2 would not be possible)

![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/outputs_self_propelled_approach/DLA%20output%20500x500%20-density%3D0.35%20-generated%20in%201.51s%20test%20selecting%20point%20with%20less%20than%203%20immediate%20neighbors.jpg)

The next step was to predict how the canvas space would be altered with the potential new point (once it had selected a new point in the process outlined above). It counts how many neighbors the point would have (ie. points in the square around the new point) and if that number is too big, it does not put a point there, restarting the process and looking for a new candidate next to which to expand. 

This is what results when the program limits the potential neighbors to 3 or less:

![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/outputs_self_propelled_approach/DLA%20output%20500x500%20-density%3D0.25%20-generated%20in%204.05s%20limiting%20potenital%20neighbors%20greater%20than%203.jpg)

This is for 2 or less:

![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/outputs_self_propelled_approach/DLA%20output%20500x500%20-density%3D0.25%20-generated%20in%2014.9s%20limiting%20potenital%20neighbors%20greater%20than%202.jpg)

Nobody would expect it to work when it will only place a point where it will have 1 neighbor, but this is what it generated for that: (seems oddly similar to some of Stephen Wolfram's 2D cellular automota from his book "A New Kind of Science")

![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/outputs_self_propelled_approach/DLA%20output%20500x500%20-density%3D0.05%20-generated%20in%204.84s%20limiting%20potenital%20neighbors%20greater%20than%201.jpg)

What if instead of checking the immediate neighbors (ie. those points the surrounding square), we checked only the adjacent neighbors? Doing this where the program abandons a possible point if it has more than 2 adjacent neighbors produces the following result:

![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/outputs_self_propelled_approach/DLA%20output%20500x500%20-density%3D0.25%20-generated%20in%204.10s%20limiting%20potential%20adjacent%20neighbors%20greater%20than%202.jpg)

It is also interesting to note that using 1 instead of 2 produces another quirky result:

![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/outputs_self_propelled_approach/DLA%20output%20500x500%20-density%3D0.25%20-generated%20in%2023.5s%20limiting%20potential%20adjacent%20neighbors%20greater%20than%201.jpg)

## To Do:
- fix wraparound issue (i think it happens with image conversion)
- fix non black and white pixel issue
- ~~implement scaling depending on the desired resolution to increase generation speed~~
    - ~~ie. when it starts, have a small box, when that box reaches desired density, add white space around edges, repeat until at desired resolution and density~~
    - ~~fix putdata issue from result (is there even an issue?)~~
- implement mp4 creation of building structure
- devise an alternate optimization solution where the program keeps track of the edge points and then picks a random edge point, next to which to add a new point
    - weight the probability of the new adjacent point to be farther from the seed point
    - weight the probability of choosing a point based on points, that haven't or have been added on to before (or only have 2 or something)
    - what if I start at the end and work in???

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
- investigate mathematical generation by simulation of energy for each point in connection with dielectric breakdown: https://web.archive.org/web/20030806022533/http://classes.yale.edu/fractals/Panorama/Physics/DLA/DBM/DBM2.html
- branching vectors with random variation approach, okay how would we do that?
    - have a bunch of vector objects, every iteration increase the magnitude of each vector by 1 pixel (if it is going to run into another vector object, terminate that vector object's growth)
    - the longer a vector object survives without being terminated, the more likely it is to have a child branch come from it at a random angle intersecting it but <90 degrees
    - repeat this process until the desired density is reached


