# map load

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import yaml

img_name = 'testmap.png'


class Map():
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as f:
            Info = yaml.load(f, Loader=yaml.FullLoader)
        self.image = Info['image']
        self.resolution = Info['resolution']
        self.origin = Info['origin']
        self.load_map()
        
    def load_map(self):
        self.gray_image = np.dot(mpimg.imread(self.image)[...,:3], [0.299, 0.587, 0.114])
        self.heigh = self.gray_image.shape[0]
        self.width = self.gray_image.shape[1]
        self.obs_map = [[0 for i in range(self.heigh)]
                      for j in range(self.width)]
        for i in range(self.heigh):
            for j in range(self.width):
                if self.gray_image[i][j] == 0:
                    self.obs_map[j][self.heigh-1-i] = 1 #[x][y] = 0 is obs
                    
                    
    def show_map(self):
        figure_res = 0.05
        plt.figure(figsize=(5,5))
        ox, oy = [], []
    
        for i in range(self.heigh):
            for j in range(self.width):
                if self.gray_image[i][j] == 0:
                    for k in range(int(1/figure_res)):
                        for l in range(int(1/figure_res)):
                            ox.append(self.origin[0]+(j+figure_res*k)*self.resolution)
                            oy.append(self.origin[1]+(self.heigh-i-figure_res*l)*self.resolution)
                        
        plt.plot(ox, oy, ".k")
        plt.grid(True)
        plt.axis("equal")
        plt.xlim(self.origin[0],self.origin[0]+self.width*self.resolution)
        plt.ylim(self.origin[1],self.origin[1]+self.heigh*self.resolution)  
        plt.show()
        
    def Abs2Map(self, Abs):
        M_X = int(Abs[0]/self.resolution - self.origin[0]/self.resolution)
        M_Y = int(Abs[1]/self.resolution - self.origin[1]/self.resolution)
        return [M_X, M_Y]
    
    def Map2Abs(self, M):
        Abs_X = M[0]*self.resolution + self.origin[0]
        Abs_Y = M[1]*self.resolution + self.origin[1]
        return [Abs_X, Abs_Y]


if __name__ == '__main__':
    A = Map('testmap.yaml')

