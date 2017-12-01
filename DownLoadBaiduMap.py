import math;
resolutions=[];
origin=[0,0];
tileSize=256;
i=0;
extent=[13375760.548844904, 3509288.503957173, 13400124.207305659, 3523532.292628932];
while(i<19):
    resolutions.append(int(math.pow(2,18-i)));
    i=i+1;



def getTileRangeForExtentAndResolution (extent, resolution):
    left=getTileCoordForXYAndResolution(extent[0], extent[1], resolution);
    right=getTileCoordForXYAndResolution(extent[2], extent[3], resolution);
    minX = left[1];
    minY = left[2];
    maxX=right[1];
    maxY=right[2];
    return [left[0],minX,maxX,minY,maxY];

def getTileCoordForXYAndResolution(x, y, resolution):
    z=getZForResolution(resolution,resolutions);
    xFromOrigin = math.floor((x - origin[0]) / resolution);
    yFromOrigin = math.floor((y - origin[1]) / resolution);
    tileCoordX = xFromOrigin / tileSize;
    tileCoordY = yFromOrigin / tileSize;
    tileCoordX = math.floor(tileCoordX);
    tileCoordY = math.floor(tileCoordY);
    return [z, tileCoordX, tileCoordY];



def getZForResolution(resolution,resolutions):
    length=len(resolutions);
    z=0;
    index=0;
    for item in resolutions:
        if(item==resolution):
            z=index;
            break;
        else:
            index=index+1;
    return z;



for resolution in resolutions:
    result=getTileRangeForExtentAndResolution(extent, resolution);

    if (result[0]<13):
        print(result[0])
        for i in range(result[1]-1, result[2]+1):
            for j in range(result[3]-1, result[4]+1):
                print([result[0],i,j]);










