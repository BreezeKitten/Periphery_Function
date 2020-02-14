# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 13:36:57 2020

@author: BreezeCat
"""

import math as m
from bresenham.bresenham import bresenham as bresen
from map_load.map_load import Map 

PI = m.pi


def Find_Beside_Points(P, search_length):
    Px, Py, Pth = P
    
    Px1 = Px + search_length * m.cos(Pth - PI/2)
    Py1 = Py + search_length * m.sin(Pth - PI/2)
    
    Px2 = Px + search_length * m.cos(Pth + PI/2)
    Py2 = Py + search_length * m.sin(Pth + PI/2)
    
    return [Px1,Py1], [Px2,Py2]
'''
def Get_Intersection(P, M, search_length):
    B1, B2 = Find_Beside_Points(P, search_length)
    MP = M.Abs2Map(P)
    MB1 = M.Abs2Map(B1)
    MB2 = M.Abs2Map(B2)
    C1 = list(bresen(MP[0],MP[1],MB1[0],MB1[1]))
    C2 = list(bresen(MP[0],MP[1],MB2[0],MB2[1]))
    BR = None
    BL = None
    for i in C1:
        if M.obs_map[i[0]][i[1]] == 1:
            print(i)
            print(M.Map2Abs(i))
            BR = M.Map2Abs(i)
            break
    for i in C2:
        if M.obs_map[i[0]][i[1]] == 1:
            print(i, '--')
            print(M.Map2Abs(i))
            BL = M.Map2Abs(i)
            break
    return BR, BL
'''
def Get_InterSection(P, G, M):
    MP = M.Abs2Map(P)
    MG = M.Abs2Map(G)
    C = list(bresen(MP[0],MP[1],MG[0],MG[1]))
    B = None
    for i in C:
        if M.obs_map[i[0]][i[1]] == 1:
            print(i)
            print(M.Map2Abs(i))
            B = M.Map2Abs(i)
            break
    return B

if __name__ == '__main__':
    img_name = 'map_load/testmap.yaml'
    A = [4,8,PI/4]
    M = Map(img_name)
    B1, B2 = Find_Beside_Points(A, 10)
    R = Get_InterSection(A, B1, M)
