'''
Wavelet compression source file for Facial Characteristics Extraction

Lucas Alexandre Soares - 9293265
Giovanna Oliveira Guimarães - 9293693
Julia Diniz - 9364865
'''


import numpy as np
import argparse
import pywt
import cv2    

def w2d(img, mode="haar", level=None):

    if mode == None:
        mode = "haar"

    imArray = cv2.imread(img)
    
    #Datatype conversions
    #convert to grayscale
    imArray = cv2.cvtColor(imArray, cv2.COLOR_RGB2GRAY)
    
    #convert to float
    imArray = np.float32(imArray)   
    imArray /= 255;
    
    # compute coefficients 
    coeffs = pywt.wavedec2(imArray, mode, level=level)

    #Process Coefficients
    coeffs_H = list(coeffs)
    coeffs_H[0] *= 0;  

    # reconstruction
    # TODO: Check reconstruction resolution
    imArray_H = pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H = np.uint8(imArray_H)
    
    #Display result
    imArray = cv2.cvtColor(imArray, cv2.COLOR_GRAY2RGB)
    cv2.imshow(img, imArray_H)
    cv2.imwrite("teste.jpg", imArray_H)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-l", "--level", required=False, help="compression level")
ap.add_argument("-m", "--mode", required=False, help="wavelet mode (\'haar\', \'db\', \'sym\', \'coif\', \'bior\', \'rbio\', \'dmey\', \'gaus\', \'mexh\', \'morl\', \'cgau\', \'shan\', \'fbsp\', \'cmor\')")

args = vars(ap.parse_args())
print(args.get("level"))
w2d(args.get("image"), args.get("mode"), int(args.get("level")))








