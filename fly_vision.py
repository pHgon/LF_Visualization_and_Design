from PIL import Image
import numpy as np

def fly_vision(path):

    img = Image.open(path + "_tempSAIs/4.png")
    np_im = np.array(img)

    shape = np_im.shape
    print(shape)

    new_image = Image.new('RGB', (shape[1]*15, shape[0]*15), color = (255,255,255))
    new_image.save('test.png')
    new_image_np = np.array(new_image)

    print(new_image_np.shape)

    SAIs = []

    for i in range(225):
        aux = Image.open("/home/thiago/Mestrado_cadeiras/LF_VizualizationApp/allSAIs/" + str(i) + ".png")
        SAIs.append(np.array(aux))

    count = 0

    for color in range(new_image_np.shape[2]):
        for i in range(0,new_image_np.shape[0],15):
            for j in range(0,new_image_np.shape[1],15):
                print("i: {}   j: {}".format(i,j))
                print("i: {}   j: {}".format(i//15,j//15))
                print("Count: {}".format(count))
                new_image_np[i][j][color] = (SAIs[count])[i//15][j//15][color]
                count += 1

        count = 0
                
    
    upsampled_image = Image.fromarray(new_image_np, 'RGB')
    upsampled_image.save('my.png')

fly_vision('/home/thiago/Mestrado_cadeiras/LF_VizualizationApp/')