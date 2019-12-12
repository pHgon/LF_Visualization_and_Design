from PIL import Image
import numpy as np
import statistics
import cv2

def upsampling(Sais, posCentral, times=2):
    shape = Sais[0].shape
    new_Sais = []

    new_Sais.append(Sais[posCentral[0]-1][posCentral[1]-1])
    new_Sais.append(Sais[posCentral[0]-1][posCentral[1]])
    new_Sais.append(Sais[posCentral[0]-1][posCentral[1]+1])
    new_Sais.append(Sais[posCentral[0]][posCentral[1]-1])
    new_Sais.append(Sais[posCentral[0]][posCentral[1]])
    new_Sais.append(Sais[posCentral[0]][posCentral[1]+1])
    new_Sais.append(Sais[posCentral[0]+1][posCentral[1]-1])
    new_Sais.append(Sais[posCentral[0]+1][posCentral[1]])
    new_Sais.append(Sais[posCentral[0]+1][posCentral[1]+1])
    

    new_image = Image.new('RGB', (shape[1]*times, shape[0]*times), color = (0,0,0))

    new_image_np = np.array(new_image)

    for color in range(new_image_np.shape[2]):
        for i in range(0,new_image_np.shape[0],2):
            for j in range(0,new_image_np.shape[1],2):
                #First Pixel
                new_image_np[i][j][color] = (int((new_Sais[0])[i//2][j//2][color]) + int((new_Sais[1])[i//2][j//2][color]) + int((new_Sais[3])[i//2][j//2][color]) + int((new_Sais[4])[i//2][j//2][color]))//4
                #Second Pixel
                new_image_np[i+1][j][color] = (int((new_Sais[1])[i//2][j//2][color]) + int((new_Sais[2])[i//2][j//2][color]) + int((new_Sais[4])[i//2][j//2][color]) + int((new_Sais[5])[i//2][j//2][color]))//4
                #Tird Pixel
                new_image_np[i][j+1][color] = (int((new_Sais[3])[i//2][j//2][color]) + int((new_Sais[4])[i//2][j//2][color]) + int((new_Sais[6])[i//2][j//2][color]) + int((new_Sais[7])[i//2][j//2][color]))//4
                #Fourth Pixel
                new_image_np[i+1][j+1][color] = (int((new_Sais[4])[i//2][j//2][color]) + int((new_Sais[5])[i//2][j//2][color]) + int((new_Sais[7])[i//2][j//2][color]) + int((new_Sais[8 ])[i//2][j//2][color]))//4
    
    upsampled_image = Image.fromarray(new_image_np, 'RGB')
    upsampled_image.save('upsampled_LF.png')
    img = cv2.imread('upsampled_LF.png')
    cv2.imwrite('upsampled_LF2.png',img)
