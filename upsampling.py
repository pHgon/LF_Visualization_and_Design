from PIL import Image
import numpy as np

def getSaiUpLeft(path):
    img = Image.open(path + "_tempSAIs/0.png")
    np_im = np.array(img)
    return np_im

def getSaiUp(path):
    img = Image.open(path + "_tempSAIs/1.png")
    np_im = np.array(img)
    return np_im

def getSaiUpRight(path):
    img = Image.open(path + "_tempSAIs/2.png")
    np_im = np.array(img)
    return np_im

def getSaiLeft(path):
    img = Image.open(path + "_tempSAIs/3.png")
    np_im = np.array(img)
    return np_im

def getSaiRight(path):
    img = Image.open(path + "_tempSAIs/5.png")
    np_im = np.array(img)
    return np_im

def getSaiDownLeft(path):
    img = Image.open(path + "_tempSAIs/6.png")
    np_im = np.array(img)
    return np_im

def getSaiDown(path):
    img = Image.open(path + "_tempSAIs/7.png")
    np_im = np.array(img)
    return np_im

def getSaiDownRight(path):
    img = Image.open(path + "_tempSAIs/8.png")
    np_im = np.array(img)
    return np_im


def upsampling(path, times):

    img = Image.open(path + "_tempSAIs/4.png")
    np_im = np.array(img)

    shape = np_im.shape

    new_image = Image.new('RGB', (shape[1], shape[0]), color = (0,0,0))

    new_image.save('test.png')
    new_image_np = np.array(new_image)

    print(new_image_np.shape)

    for i in range(new_image_np[0,:]):
        for j in range(new_image_np[1,:]):
            for color in range(new_image_np[2,:]):
                print(new_image_np[i][j][color])
            


upsampling('/home/thiago/Mestrado_cadeiras/LF_VizualizationApp/', 2)