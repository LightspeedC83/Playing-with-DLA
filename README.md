# Playing with DLA
This is a program that uses diffusion limited aggregation to create images

## Output examples

### candidate point freezes only if one of the top, bottom, left, right spaces(ie. the adjacent spaces) is occupied
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/output%20-diagonals%3Dfalse.jpg)

### candidate point freezes if any space in a square around it (ie. adjacent and diagonal) is occupied
![alt text](https://github.com/LightspeedC83/Playing-with-DLA/blob/main/output%20-diagonals%3Dtrue.jpg)