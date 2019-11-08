import cv2
import numpy as np
import PIL
from PIL import Image, ImageEnhance
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

'''def brightness(img_array, alpha, gamma):
    return cv2.addWeighted(img_array, alpha, np.zeros(img_array.shape, img_array.dtype), 0, gamma)'''

def transformations(img_array, f_br, f_co, f_sh, f_sa):
    img = Image.fromarray(img_array, 'RGB')
    img = (PIL.ImageEnhance.Brightness(img)).enhance(f_br)
    img = (PIL.ImageEnhance.Contrast(img)).enhance(f_co)
    img = (PIL.ImageEnhance.Sharpness(img)).enhance(f_sh)
    img = (PIL.ImageEnhance.Color(img)).enhance(f_sa)

    r, g, b = img.split()
    r, g, b = r.histogram(), g.histogram(), b.histogram()

    fig, ax = plt.subplots()
    ax.set_facecolor("#202020")
    plt.xlim(xmax = 256, xmin = -1)
    plt.ylim(ymax = max([max(r), max(g), max(b)]), ymin = 0)
    #fig.set_size_inches(2.4, 1.1, forward=True)

    plt.plot( b, color ='b', label='Blue',linewidth=5.)
    plt.fill_between(np.arange(0, 256), b, color='b', alpha=0.4)
    plt.plot( g, color ='g', label='Green',linewidth=5.)
    plt.fill_between(np.arange(0, 256), g, color='g', alpha=0.4)
    plt.plot( r, color='r', label='Red',linewidth=5.)
    plt.fill_between(np.arange(0, 256), r, color='r', alpha=0.4)
    
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    #plt.show()

    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return np.array(img), data