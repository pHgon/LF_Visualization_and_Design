from PIL import Image
import numpy as np
import statistics


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

    new_image = Image.new('RGB', (shape[1]*times, shape[0]*times), color = (0,0,0))

    new_image_np = np.array(new_image)

    Sais = [getSaiUpLeft(path), getSaiUp(path), getSaiUpRight(path), getSaiLeft(path), getSaiRight(path), getSaiDownLeft(path), getSaiDown(path), getSaiDownRight(path)]

    for color in range(new_image_np.shape[2]):
        for i in range(0,new_image_np.shape[0],2):
            for j in range(0,new_image_np.shape[1],2):
                #First Pixel
                new_image_np[i][j][color] = (int((Sais[0])[i//2][j//2][color]) + int((Sais[1])[i//2][j//2][color]) + int((Sais[3])[i//2][j//2][color]) + int(np_im[i//2][j//2][color]))//times
                #Second Pixel
                new_image_np[i+1][j][color] = (int((Sais[1])[i//2][j//2][color]) + int((Sais[2])[i//2][j//2][color]) + int((Sais[4])[i//2][j//2][color]) + int(np_im[i//2][j//2][color]))//times
                #Tird Pixel
                new_image_np[i][j+1][color] = (int((Sais[3])[i//2][j//2][color]) + int((Sais[5])[i//2][j//2][color]) + int((Sais[6])[i//2][j//2][color]) + int(np_im[i//2][j//2][color]))//times
                #Fourth Pixel
                new_image_np[i+1][j+1][color] = (int((Sais[4])[i//2][j//2][color]) + int((Sais[6])[i//2][j//2][color]) + int((Sais[7])[i//2][j//2][color]) + int(np_im[i//2][j//2][color]))//times
    
    upsampled_image = Image.fromarray(new_image_np, 'RGB')
    upsampled_image.save('my.png')

upsampling('/home/thiago/Mestrado_cadeiras/LF_VizualizationApp/', 2)