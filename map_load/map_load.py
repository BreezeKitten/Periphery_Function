# map load

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img_name = 'testmap.png'


def load_img(name):
    lena = mpimg.imread(name)
    return lena
    
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def show_map(image_name, map_res, origin):
    image = load_img(image_name)
    image_g = rgb2gray(image)
    #plt.imshow(image_g, cmap='Greys_r', origin='lower')
    #map_res = 1 # meter/pixel
    figure_res = 0.05
    plt.figure(figsize=(5,5))
    ox, oy = [], []
    obs_map = [[1 for i in range(image_g.shape[0])]
                      for j in range(image_g.shape[1])]
    
    for i in range(image_g.shape[0]):
        for j in range(image_g.shape[1]):
            if image_g[i][j] == 0:
                obs_map[j][image_g.shape[0]-1-i] = 0  #[x][y] 0 is obs
                for k in range(int(1/figure_res)):
                    for l in range(int(1/figure_res)):
                        ox.append(origin[0]+(j+figure_res*k)*map_res)
                        oy.append(origin[1]+(image_g.shape[0]-i-figure_res*l)*map_res)
                        
    plt.plot(ox, oy, ".k")
    plt.grid(True)
    plt.axis("equal")
    plt.xlim(origin[0],origin[0]+image_g.shape[1]*map_res)
    plt.ylim(origin[1],origin[1]+image_g.shape[0]*map_res)
    plt.show()
    
    return obs_map


if __name__ == '__main__':
    A = show_map(img_name, 1, [0,0])

