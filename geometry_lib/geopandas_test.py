# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 10:41:50 2020

@author: BreezeCat
"""

import geopandas
from shapely.geometry import Polygon
import math as m
import random

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


def New_robot_polygon(PA, PB, rA, rB, VO_range, Vx, Vy):
    u = Vector(PB.x - PA.x, PB.y - PA.y)
    u_unit = Vector((PB.x - PA.x)/u.length, (PB.y - PA.y)/u.length)
    d = u.length
    theta = m.asin((rA + rB)/d)
    u_L = Rotate_vector(u_unit, theta)
    u_R = Rotate_vector(u_unit, -theta)
    
    #u_L.print_vector()
    #u_R.print_vector()
    
    if VO_range == 'inf':
        LS = 0
    else:
        LS = d/VO_range/m.cos(theta)
    LL = max(5,5*LS)
    
    A = Point(PA.x + LS* u_L.x + Vx, PA.y + LS* u_L.y + Vy)
    B = Point(PA.x + LS* u_R.x + Vx, PA.y + LS* u_R.y + Vy)
    C = Point(PA.x + LL* u_R.x + Vx, PA.y + LL* u_R.y + Vy)
    D = Point(PA.x + LL* u_L.x + Vx, PA.y + LL* u_L.y + Vy)
    
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


def Build_test_map(map_num):
    obs_list = []
    if map_num == 1:
        obs_list.append(Polygon([(-5,-5), (5,-5), (5,-1), (-5,-1)]))
        obs_list.append(Polygon([(-5,1), (5,1), (5,5), (-5,5)]))
        test_map = Generate_GeoDataFrame(obs_list)
        return test_map
    elif map_num == 2:
        obs_list.append(Polygon([(-5,-5), (0,-5), (0,-1), (-5,-1)]))
        obs_list.append(Polygon([(-5,1), (5,1), (5,5), (-5,5)]))
        test_map = Generate_GeoDataFrame(obs_list)
        return test_map
    else:
        print('map_num error')
        return 
    
def Build_velocity_poly(P, theta, V, dV, Wmax, approximation_method = 'Tri'):
    Vc = Point(P.x+V*m.cos(theta), P.y+V*m.sin(theta))
    if V == 0:
        Vv = Vector((V+dV)*m.cos(theta), (V+dV)*m.sin(theta))
    else:
        Vv = Vector(V*m.cos(theta), V*m.sin(theta))
    Vo = Rotate_vector(Vv, m.pi/2)
    
    # Square approximaion   
    if approximation_method == 'Squ':      
        A = Point(Vc.x+dV, Vc.y+dV)
        B = Point(Vc.x-dV, Vc.y+dV)
        C = Point(Vc.x-dV, Vc.y-dV)
        D = Point(Vc.x+dV, Vc.y-dV)
        poly_list = [Polygon([A.list, B.list, C.list, D.list])]
    
    # triangle approximation
    if approximation_method == 'Tri':
        A = Point(Vv.x*(V+dV)/Vv.length + Vo.x*(V+dV)*Wmax/Vo.length, Vv.y*(V+dV)/Vv.length + Vo.y*(V+dV)*Wmax/Vo.length)
        B = Point(Vv.x*(V-dV)/Vv.length + Vo.x*(V-dV)*Wmax/Vo.length, Vv.y*(V-dV)/Vv.length + Vo.y*(V-dV)*Wmax/Vo.length)
        C = Point(Vv.x*(V-dV)/Vv.length - Vo.x*(V-dV)*Wmax/Vo.length, Vv.y*(V-dV)/Vv.length - Vo.y*(V-dV)*Wmax/Vo.length)
        D = Point(Vv.x*(V+dV)/Vv.length - Vo.x*(V+dV)*Wmax/Vo.length, Vv.y*(V+dV)/Vv.length - Vo.y*(V+dV)*Wmax/Vo.length)    
        if V*(V-dV) > 0:
            poly_list = [Polygon([A.list, B.list, C.list, D.list])]
        else:
            poly_list = [Polygon([A.list, P.list, D.list]), Polygon([P.list, B.list, C.list])]
      
   
    Vel_df = Generate_GeoDataFrame(poly_list)
    return Vel_df    

def Show_set(Map, V_set, VRVO):
    VRVO.plot(ax=V_set.plot(ax=Map.plot(color='black'), color='yellow'), color='red')
    return    

def Random_virtual_robot(x_bound, y_bound):
    VR = Point(random.uniform(x_bound[0], x_bound[1]), random.uniform(y_bound[0], y_bound[1]))
    r_VR = random.uniform(0.1,0.3)
    return VR, r_VR


if __name__ == '__main__':
    Map = Build_test_map(1)
    Pose = Point(0,0)
    direction = -0*m.pi/180
    V_set = Build_velocity_poly(Pose, direction, 0.5, 1, 1, approximation_method='Squ')
    #forbidden velocity
    FV = Set_intersection(V_set, Map)
    Show_set(Map, V_set, FV)
    
    time = 1
    VR, r_VR = Random_virtual_robot([-1,2], [0,2])
    VR_list = [New_robot_polygon(Pose, VR, 0.2, r_VR, 2, 0, 0)]
    VVO = Generate_GeoDataFrame(VR_list)
    diff = Set_difference(FV, VVO)
    
    while(len(diff.is_empty) != 0):
        time += 1        
        VR, r_VR = Random_virtual_robot([0,2], [-1.2,-0.5])
        VR_list = [New_robot_polygon(Pose, VR, 0.2, r_VR, 2, 0, 0)]
        VVO = Generate_GeoDataFrame(VR_list)
        diff = Set_difference(FV, VVO)
        
    Show_set(Map, V_set, VVO)
    
    
    