# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 10:41:50 2020

@author: BreezeCat
"""

import geopandas
from shapely.geometry import Polygon
import math as m
import random
import matplotlib.pyplot as plt
from shapely.geometry import Point as lib_Point

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def List(self):
        return (self.x, self.y)
        
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = self.get_length()
        
    def get_length(self):
        return m.sqrt(self.x*self.x + self.y*self.y)
    
    def print_vector(self):
        print([self.x, self.y])
        
class Robot:
    def __init__(self, x, y, theta, v, w):
        self.Pose, self.theta, self.v, self.w = Point(x, y), theta, v, w
    
    def Update_state(self, v, w, dt):
        self.v, self.w = v, w
        for i in range(10):
            self.Pose.x += self.v * m.cos(self.theta) *dt/10
            self.Pose.y += self.v * m.sin(self.theta) *dt/10
            self.theta += self.w * dt/10

class Virtual_Robot:
    def __init__(self, x_bound, y_bound, Vx=0, Vy=0):
        self.x_bound = x_bound
        self.y_bound = y_bound
        self.Random_state(Vx, Vy)
    
    def Random_state(self, Vx = 0, Vy = 0):
        self.Pose = Point(random.uniform(self.x_bound[0], self.x_bound[1]), random.uniform(self.y_bound[0], self.y_bound[1]))
        self.r = random.uniform(0.1,0.3)
        self.Vx = Vx
        self.Vy = Vy
        
    def Update_state(self, dt):
        self.Pose.x += self.Vx *dt
        self.Pose.y += self.Vy *dt
        
    def Random_Velocity(self, dV = 1):
        self.Vx += random.uniform(-dV, dV)
        self.Vy += random.uniform(-dV, dV)
        

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
    if (rA + rB) > d:
        theta = 0
    else:
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
    
    polys = Polygon([A.List(), B.List(), C.List(), D.List()])
    
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
    elif map_num == 3:
        obs_list.append(Polygon([(-5,-5), (1,-5), (1,-1), (-5,-1)]))
        obs_list.append(Polygon([(-5,1), (5,1), (5,5), (-5,5)]))
        obs_list.append(Polygon([(3,-5), (3,5), (5,5), (5,-5)]))
        test_map = Generate_GeoDataFrame(obs_list)
        return test_map
    else:
        print('map_num error')
        return 
    
def Build_velocity_poly(Robot, dV, Wmax, approximation_method = 'Tri'):
    P = Robot.Pose
    theta = Robot.theta
    V = Robot.v
    
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
        poly_list = [Polygon([A.List(), B.List(), C.List(), D.List()])]
    
    # triangle approximation
    if approximation_method == 'Tri':
        A = Point(Vv.x*(V+dV)/Vv.length + Vo.x*(V+dV)*Wmax/Vo.length + P.x, Vv.y*(V+dV)/Vv.length + Vo.y*(V+dV)*Wmax/Vo.length + P.y)
        B = Point(Vv.x*(V-dV)/Vv.length + Vo.x*(V-dV)*Wmax/Vo.length + P.x, Vv.y*(V-dV)/Vv.length + Vo.y*(V-dV)*Wmax/Vo.length + P.y)
        C = Point(Vv.x*(V-dV)/Vv.length - Vo.x*(V-dV)*Wmax/Vo.length + P.x, Vv.y*(V-dV)/Vv.length - Vo.y*(V-dV)*Wmax/Vo.length + P.y)
        D = Point(Vv.x*(V+dV)/Vv.length - Vo.x*(V+dV)*Wmax/Vo.length + P.x, Vv.y*(V+dV)/Vv.length - Vo.y*(V+dV)*Wmax/Vo.length + P.y)    
        if V*(V-dV) > 0 :#or V*(V+dV) < 0:
            poly_list = [Polygon([A.List(), B.List(), C.List(), D.List()])]
        else:
            poly_list = [Polygon([A.List(), P.List(), D.List()]), Polygon([P.List(), B.List(), C.List()])]
      
   
    Vel_df = Generate_GeoDataFrame(poly_list)
    return Vel_df    

def Show_set(Map, V_set, VRVO, name):
    plt.close('all')
    VRVO.plot(ax=V_set.plot(ax=Map.plot(color='black'), color='yellow'), color='red')
    plt.savefig('P/'+ name + '.png')
    return    

def Random_virtual_robot(x_bound, y_bound):
    VR = Point(random.uniform(x_bound[0], x_bound[1]), random.uniform(y_bound[0], y_bound[1]))
    r_VR = random.uniform(0.1,0.3)
    return VR, r_VR



def Show_robot(Robot, VR_list, Map, name):
    L = 0.5
    plt.close('all')
    plt.figure(figsize=(12,12))
    
    Map.plot(color='black')
    ax = plt.gca()

    plt.xlabel('X(m)')
    plt.ylabel('Y(m)')
    
    plt.plot(Robot.Pose.x, Robot.Pose.y, 'bo')
    plt.arrow(Robot.Pose.x, Robot.Pose.y, L*m.cos(Robot.theta), L*m.sin(Robot.theta))
    circle1 = plt.Circle(Robot.Pose.List(), 0.2, color = 'b', fill = False)
    ax.add_artist(circle1)
    
    for VR in VR_list:
        plt.plot(VR.Pose.x, VR.Pose.y, 'go')
        circleVR = plt.Circle(VR.Pose.List(), VR.r, color = 'g', fill = False)
        ax.add_artist(circleVR)
       
    plt.savefig('PP/'+ name + '.png')
    
    return

def General_action_in_set(Pose, theta, Set):
    Flag = False
    time = 0
    while(not Flag):
        time += 1
        v = random.uniform(0,1)
        w = random.uniform(-1,1)
        x = v*m.cos(theta) - v*w*m.sin(theta)
        y = v*m.sin(theta) + v*w*m.cos(theta)
        P = lib_Point(Pose.x + x, Pose.y + y)
        for item in Set.geometry:
            Flag = Flag or P.within(item)
        if time > 1000:
            print('Action time out')
            return 0, -1
    return v, w

if __name__ == '__main__':
    Map = Build_test_map(3)
    
    Main_Robot = Robot(x=0, y=0, theta=0, v=0, w=0)
    dt = 0.1
    t = 0
    while(t < 1000):
        V_set = Build_velocity_poly(Main_Robot, 1.5, 1, approximation_method='Tri')
        #forbidden velocity
        FV = Set_intersection(V_set, Map)
        plt.close('all')
        FV.plot(ax=V_set.plot(ax=Map.plot(color='black'), color='yellow'), color='green')
        plt.savefig('PPP/'+ str(round(10*t,1)) + '.png')
    
        Virtual_robot_list = []
        for i in range(len(FV.geometry)):
            bound = FV.geometry[i].bounds
            x_bound = [bound[0]-0.5, bound[2]+0.5]
            y_bound = [bound[1]-0.5, bound[3]+0.5]
            Virtual_robot_list.append(Virtual_Robot(x_bound, y_bound))
    
        time = 1
        area = 0
        while(area == 0):
            for VR in Virtual_robot_list:
               VR.Random_state()
            VR_list = [New_robot_polygon(Main_Robot.Pose, VR.Pose, 0.2, VR.r, 2, 0, 0) for VR in Virtual_robot_list]
            for item in VR_list:
                area += item.area
                
        VVO = Generate_GeoDataFrame(VR_list)
        diff = Set_difference(FV, VVO)
        while(len(diff.is_empty) != 0):
            time += 1
            area = 0
            for VR in Virtual_robot_list:
                VR.Random_state()
            VR_list = [New_robot_polygon(Main_Robot.Pose, VR.Pose, 0.2, VR.r, 2, 0, 0) for VR in Virtual_robot_list]
            for item in VR_list:
                area += item.area
            if area != 0:
                VVO = Generate_GeoDataFrame(VR_list)
                diff = Set_difference(FV, VVO)
                
            if time > 1000:
                print('Time_Out')
                time = 0
                x_bound = [Main_Robot.Pose.x-1, Main_Robot.Pose.x+1]
                y_bound = [Main_Robot.Pose.y-1, Main_Robot.Pose.y+1]
                Virtual_robot_list.append(Virtual_Robot(x_bound, y_bound))
        
        Show_set(Map, V_set, VVO, str(round(10*t,1)))    
        Show_robot(Main_Robot, Virtual_robot_list, Map, str(round(10*t,1)))
        AV = Set_difference(V_set, VVO)
        av, aw = General_action_in_set(Main_Robot.Pose, Main_Robot.theta, AV)
        
        Main_Robot.Update_state(v=av, w=aw, dt=dt)
        t += dt
        print(t)
    
    

    
    
    