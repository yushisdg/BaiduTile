import urllib.request
import requests
import os
import re
import psycopg2

url = "http://api2.map.bdimg.com/customimage/tile?&udt=20171110&scale=1&ak=2YSGywmFy0PHOqVKTRNPoGOY&styles=t%3Aall%7Ce%3Al.t.s%7Cc%3A%23021364%2Ct%3Aall%7Ce%3Al.t.f%7Cc%3A%23c8ebff%2Ct%3Aarterial%7Ce%3Ag.f%7Cc%3A%23000000%2Ct%3Aarterial%7Ce%3Ag.s%7Cc%3A%233e61b7%2Ct%3Alocal%7Ce%3Ag.f%7Cc%3A%2332417a%7Cw%3A0.2%2Ct%3Alocal%7Ce%3Ag.s%7Cc%3A%232b4897%7Cw%3A0.2%2Ct%3Ahighway%7Ce%3Ag.f%7Cc%3A%23334285%2Ct%3Ahighway%7Ce%3Ag.s%7Cc%3A%23334285%2Ct%3Asubway%7Ce%3Ag.f%7Cc%3A%23c8ebff%2Ct%3Asubway%7Ce%3Ag.s%7Cc%3A%23021364%7Cw%3A1.2%2Ct%3Aland%7Ce%3Ag.f%7Cc%3A%23000934%2Ct%3Awater%7Ce%3Ag.f%7Cc%3A%23466bc7%2Ct%3Agreen%7Ce%3Ag.f%7Cc%3A%232b4993%2Ct%3Amanmade%7Ce%3Ag.f%7Cc%3A%2300063b%2Ct%3Abuilding%7Ce%3Ag.f%7Cc%3A%23000024%2Ct%3Abuilding%7Ce%3Ag.s%7Cc%3A%233e61b7%2Ct%3Apoi%7Ce%3Al%7Cv%3Aoff%2Ct%3Alabel%7Ce%3Aall%7Cv%3Aoff%7Cc%3A%23060301%2Ct%3Aboundary%7Ce%3Ag%7Cc%3A%237499ff";


def download(x,y,z,url):
    imgUrl=url+"&x=" + x + "&y=" + y + "&z=" + z
    try:
        r=requests.get(imgUrl,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        print(psycopg2.Binary(r.content));
        xyz=z+x+y;
        conn = psycopg2.connect(database="superpower", user="postgres", password="postgres", host="192.168.20.62",
                                port="5432");
        cur = conn.cursor();
        sql = "INSERT INTO baidu_map_style (img_context, img_id, x_row, y_row, z_level) VALUES ("+str(psycopg2.Binary(r.content))+", '"+xyz+"', '"+x+"', '"+y+"', '"+z+"');"
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
    cur.execute("SELECT count(*) from baidu_map_style t where t.x_row="+x+" and y_row="+y+" and z_level="+z);
    keyData1 = cur.fetchall();
    if keyData1[0][0] == 0:
        return 0;
    else:
        return 1;

def gci(filepath):
#遍历filepath下所有文件，包括子目录
  files = os.listdir(filepath)
  for fi in files:
    fi_d = os.path.join(filepath,fi)
    if os.path.isdir(fi_d):
      gci(fi_d)
    else:
        print(fi_d);
        arra= fi_d.split("\\");
        length=len(arra);
        print(length);
        z=arra[length-3];
        x=arra[length-2];
        y=arra[length-1].replace(".png","");
        print(z+x+y);
        flag=isExistPNG(x,y,z);
        if flag==0:
            download(x,y,z,url);
        else:
            print("已存在该条记录")
      # print (os.path.join(filepath,fi_d))

gci('F:\GisMap\map1718')
# download('199','51','10',url);