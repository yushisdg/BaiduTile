import math;
import requests
import os
import re
import psycopg2


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


url = "http://api2.map.bdimg.com/customimage/tile?&udt=20171110&scale=1&ak=2YSGywmFy0PHOqVKTRNPoGOY&styles=t%3Aall%7Ce%3Al.t.s%7Cc%3A%23021364%2Ct%3Aall%7Ce%3Al.t.f%7Cc%3A%23c8ebff%2Ct%3Aarterial%7Ce%3Ag.f%7Cc%3A%23000000%2Ct%3Aarterial%7Ce%3Ag.s%7Cc%3A%233e61b7%2Ct%3Alocal%7Ce%3Ag.f%7Cc%3A%2332417a%7Cw%3A0.2%2Ct%3Alocal%7Ce%3Ag.s%7Cc%3A%232b4897%7Cw%3A0.2%2Ct%3Ahighway%7Ce%3Ag.f%7Cc%3A%23334285%2Ct%3Ahighway%7Ce%3Ag.s%7Cc%3A%23334285%2Ct%3Asubway%7Ce%3Ag.f%7Cc%3A%23c8ebff%2Ct%3Asubway%7Ce%3Ag.s%7Cc%3A%23021364%7Cw%3A1.2%2Ct%3Aland%7Ce%3Ag.f%7Cc%3A%23000934%2Ct%3Awater%7Ce%3Ag.f%7Cc%3A%23466bc7%2Ct%3Agreen%7Ce%3Ag.f%7Cc%3A%232b4993%2Ct%3Amanmade%7Ce%3Ag.f%7Cc%3A%2300063b%2Ct%3Abuilding%7Ce%3Ag.f%7Cc%3A%23000024%2Ct%3Abuilding%7Ce%3Ag.s%7Cc%3A%233e61b7%2Ct%3Apoi%7Ce%3Al%7Cv%3Aoff%2Ct%3Alabel%7Ce%3Aall%7Cv%3Aoff%7Cc%3A%23060301%2Ct%3Aboundary%7Ce%3Ag%7Cc%3A%237499ff";
def download(x,y,z,url):
    imgUrl=url+"&x=" + str(x)+ "&y=" + str(y) + "&z=" + str(z)
    try:
        r=requests.get(imgUrl,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        print(psycopg2.Binary(r.content));
        xyz=str(z)+str(x)+str(y);
        conn = psycopg2.connect(database="superpower", user="postgres", password="postgres", host="192.168.20.62",
                                port="5432");
        cur = conn.cursor();
        sql = "INSERT INTO baidu_map_style (img_context, img_id, x_row, y_row, z_level) VALUES ("+str(psycopg2.Binary(r.content))+", '"+str(xyz)+"', '"+str(x)+"', '"+str(y)+"', '"+str(z)+"');"
        print(sql);
        try:
            cur.execute(sql);
            conn.commit();
            cur.close();
            conn.close();
        except Exception as e:
            print(e);
            cur.close();
            conn.close();
    except Exception as e:
        print(e);

def isExistPNG(x,y,z):
    conn = psycopg2.connect(database="superpower", user="postgres", password="postgres", host="192.168.20.62",port="5432");
    cur = conn.cursor();
    cur.execute("SELECT count(*) from baidu_map_style t where t.x_row="+str(x)+" and y_row="+str(y)+" and z_level="+str(z));
    keyData1 = cur.fetchall();
    if keyData1[0][0] == 0:
        return 0;
    else:
        return 1;


def batchDownLoadBaiduMap(extent,resolutions):
    for resolution in resolutions:
        result = getTileRangeForExtentAndResolution(extent, resolution);
        print(result[0])
        for i in range(result[1] - 1, result[2] + 1):
            for j in range(result[3] - 1, result[4] + 1):
                flag = isExistPNG(i, j, result[0]);
                if flag == 0:
                    download(i, j, result[0], url);
                else:
                    print("已存在该条记录")



batchDownLoadBaiduMap(extent,resolutions);





