
'''
function takes x axis along (0,0), y axis along (0,90) and z axis through the poles
'''

import numpy as np

#enter location and ht from earth(in m)

#(lat, lon) notation


def get_cartesian(latitude, longitude, height, scale=1):
  lat, lon= np.deg2rad(latitude), np.deg2rad(longitude)
  R=6371500/scale
  x=(R+height)*np.cos(lat)*np.cos(lon)
  y=(R+height)*np.cos(lat)*np.sin(lon)
  z=(R+height)*np.sin(lat)
  return x,y,z


if __name__ == "__main__":
    lat=90 
    lon=0
    ht_from_earth=500
    print(get_cartesian(lat, lon, ht_from_earth))