import cv2
import numpy as np

def depthmap(imgL, imgR, depth_map, flag):
    #imgL = cv2.imread('/home/paulo/Downloads/Vistas/007_007.png')  # downscale images for faster processing
    #imgR = cv2.imread('/home/paulo/Downloads/Vistas/mapa_imagens.png')
    imgL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    imgR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
    depth_map = cv2.cvtColor(depth_map, cv2.COLOR_BGR2GRAY)

    width = int(imgL.shape[1]* 2) 
    height = int(imgL.shape[0]* 2) 
    dim = (width, height)
    imgL = cv2.resize(imgL, dim, interpolation = cv2.INTER_AREA)
    imgR = cv2.resize(imgR, dim, interpolation = cv2.INTER_AREA)
    depth_map = cv2.resize(depth_map, dim, interpolation = cv2.INTER_AREA)

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

    for i in range (0, len(filteredImg)):
        for j in range (0, len(filteredImg[i])):
            if filteredImg[i][j] > 100:
                filteredImg[i][j]= 100 

    for i in range (0, len(filteredImg)):
        for j in range (0, len(filteredImg[i])):
            filteredImg[i][j] = ((filteredImg[i][j]*0.25) + (depth_map[i][j]*0.75))
            #filteredImg[i][j] = depth_map[i][j]


    if flag == 1:
        return cv2.bitwise_or(filteredImg,depth_map)
    elif flag == 2:
        return cv2.bitwise_xor(filteredImg,depth_map)
    else:
        return filteredImg

    # cv2.imshow('Disparity Map', filteredImg)
    # #cv2.imwrite("mapa.png", filteredImg)
    # cv2.waitKey()
    # cv2.destroyAllWindows()