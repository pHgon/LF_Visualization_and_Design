import cv2

def upsampling(path, times):

    path = r"/home/thiago/Mestrado_cadeiras/Lytro_fake/Bikes/007_007.ppm"

    img = cv2.imread(path, -1)
    times = times + 1

    cv2.imshow('SAI', img)




upsampling("/home/thiago/Mestrado_cadeiras/Lytro_fake/Bikes/007_007.ppm", 2)