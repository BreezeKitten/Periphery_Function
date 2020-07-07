# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 10:41:50 2020

@author: BreezeCat
"""

import geopandas
from shapely.geometry import Polygon
import math as m

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.list = (x, y)
        
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = self.get_length()
        
    def get_length(self):
        return m.sqrt(self.x*self.x + self.y*self.y)
    
    def print_vector(self):
        print([self.x, self.y])
        

def Dot(vector1, vector2):
    return vector1.x*vector2.x + vector1.y*vector2.y

def Norm2(vector):
    return m.sqrt(Dot(vector,vector))

def Rotate_vector(vector, theta):
    c = m.cos(theta)
    s = m.sin(theta)
    vx = c * vector.x - s * vector.y
    vy = s * vector.x + c * vector.y
    return Vector(vx, vy)


def New_robot_polygon(PA, PB, rA, rB, VO_range):
    u = Vector(PB.x - PA.x, PB.y - PA.y)
    u_unit = Vector((PB.x - PA.x)/u.length, (PB.y - PA.y)/u.length)
    d = u.length
    theta = m.asin((rA + rB)/d)
    u_L = Rotate_vector(u_unit, theta)
    u_R = Rotate_vector(u_unit, -theta)
    
    u_L.print_vector()
    u_R.print_vector()
    
    if VO_range == 'inf':
        LS = 0
    else:
        LS = d/VO_range/m.cos(theta)
    LL = max(5,5*LS)
    
    A = Point(PA.x + LS* u_L.x, PA.y + LS* u_L.y)
    B = Point(PA.x + LS* u_R.x, PA.y + LS* u_R.y)
    C = Point(PA.x + LL* u_R.x, PA.y + LL* u_R.y)
    D = Point(PA.x + LL* u_L.x, PA.y + LL* u_L.y)
    
    polys = Polygon([A.list, B.list, C.list, D.list])
    
    return polys

def Generate_GeoDataFrame(polys_list):
    num = len(polys_list)
    df_list = [i+1 for i in range(num)]
    polys_series = geopandas.GeoSeries(polys_list)
    df = geopandas.GeoDataFrame({'geometry': polys_series, 'df': df_list})
    
    return df
    
def Set_union(set1, set2):
    return  geopandas.overlay(set1, set2, how='union')

def Set_intersection(set1, set2):
    return  geopandas.overlay(set1, set2, how='intersection')

def Set_difference(set1, set2): #set1 - set2
    return  geopandas.overlay(set1, set2, how='difference')