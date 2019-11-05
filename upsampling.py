from PIL import Image

import numpy as np

def upsampling(path, times):

    path = '/home/paulo/Git-Repository/LF_VizualizationApp/007_007.ppm'

    img = Image.open(path)
    img.save("teste.png")

    #img2 = np.array(img)
    #print (img2.shape)
    return

    img = np.uint32(img)
    cv2.imshow('SAI', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




upsampling("/home/thiago/Mestrado_cadeiras/Lytro_fake/Bikes/007_007.ppm", 2)