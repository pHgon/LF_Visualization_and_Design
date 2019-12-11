import cv2
import numpy as np
import PIL
from PIL import Image, ImageEnhance
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

'''def brightness(img_array, alpha, gamma):
    return cv2.addWeighted(img_array, alpha, np.zeros(img_array.shape, img_array.dtype), 0, gamma)'''

def transformations(img_array, f_br, f_co, f_sh, f_sa, cs_r, cs_g, cs_b):
    img = Image.fromarray(img_array, 'RGB')
    img = (PIL.ImageEnhance.Brightness(img)).enhance(f_br)
    img = (PIL.ImageEnhance.Contrast(img)).enhance(f_co)
    img = (PIL.ImageEnhance.Sharpness(img)).enhance(f_sh)
    img = (PIL.ImageEnhance.Color(img)).enhance(f_sa)
    matrix = ( int(cs_r), 0, 0, 0, 0, int(cs_g), 0, 0, 0, 0, int(cs_b), 0)
    img = img.convert("RGB", matrix)

    r, g, b = img.split()
    r, g, b = r.histogram(), g.histogram(), b.histogram()

    if not cs_r:
        r[0] = 0
    if not cs_g:
        g[0] = 0
    if not cs_b:
        b[0] = 0

    fig, ax = plt.subplots()
    ax.set_facecolor("#202020")
    plt.xlim(xmax = 256, xmin = -1)
    plt.ylim(ymax = max([max(r), max(g), max(b)]), ymin = 0)
    #fig.set_size_inches(2.4, 1.1, forward=True)

    if cs_b:
        plt.plot( b, color ='b', label='Blue',linewidth=5.)
        plt.fill_between(np.arange(0, 256), b, color='b', alpha=0.4)
    if cs_g:
        plt.plot( g, color ='g', label='Green',linewidth=5.)
        plt.fill_between(np.arange(0, 256), g, color='g', alpha=0.4)
    if cs_r:
        plt.plot( r, color='r', label='Red',linewidth=5.)
        plt.fill_between(np.arange(0, 256), r, color='r', alpha=0.4)
    
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    #plt.show()

    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    plt.close(fig)
    return np.array(img), data


def depthmap(imgL, imgR):
    #imgL = cv2.imread('/home/paulo/Downloads/Vistas/007_007.png')  # downscale images for faster processing
    #imgR = cv2.imread('/home/paulo/Downloads/Vistas/mapa_imagens.png')
    imgL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    imgR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
    width = int(imgL.shape[1]* 2) 
    height = int(imgL.shape[0]* 2) 
    dim = (width, height)
    imgL = cv2.resize(imgL, dim, interpolation = cv2.INTER_AREA)
    imgR = cv2.resize(imgR, dim, interpolation = cv2.INTER_AREA)

    # SGBM Parameters -----------------
    window_size = 3                     # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
     
    left_matcher = cv2.StereoSGBM_create(
        minDisparity=0,
        numDisparities=32,             # max_disp has to be dividable by 16 f. E. HH 192, 256
        blockSize=7,
        P1=8 * 3 * window_size ** 2,    # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
        P2=32 * 3 * window_size ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=15,
        speckleWindowSize=0,
        speckleRange=2,
        preFilterCap=63,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )
    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)
     
    # FILTER Parameters
    lmbda = 80000
    sigma = 1.2
    visual_multiplier = 1.0
     
    wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
    wls_filter.setLambda(lmbda)
    wls_filter.setSigmaColor(sigma)

    displ = left_matcher.compute(imgL, imgR)  # .astype(np.float32)/16
    dispr = right_matcher.compute(imgR, imgL)  # .astype(np.float32)/16
    displ = np.int16(displ)
    dispr = np.int16(dispr)
    filteredImg = wls_filter.filter(displ, imgL, None, dispr)  # important to put "imgL" here!!!
     
    filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
    filteredImg = np.uint8(filteredImg)
    #return filteredImg
    cv2.imshow('Disparity Map', filteredImg)
    #cv2.imwrite("mapa.png", filteredImg)
    cv2.waitKey()
    cv2.destroyAllWindows()