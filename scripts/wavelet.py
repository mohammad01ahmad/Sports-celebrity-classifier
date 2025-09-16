'''
=============================================================================
function that processes the image using wavelet
=============================================================================
'''
import numpy as np 
import pywt
import cv2

def w2d(img, mode='haar', level=1):
    """
    Apply 2D wavelet transform to extract features
    """
    imArray = img
    
    # Convert to grayscale if image is colored
    if len(imArray.shape) == 3:
        imArray = cv2.cvtColor(imArray, cv2.COLOR_BGR2GRAY)  # Fixed: cv2.cvtColor9 -> cv2.cvtColor
    
    # Convert to float
    imArray = np.float32(imArray)
    imArray /= 255.0
    
    # Compute wavelet decomposition
    coeffs = pywt.wavedec2(imArray, mode, level=level)  # Fixed: pwty -> pywt
    
    # Process Coefficients - zero out approximation coefficients
    coeffs_H = list(coeffs)
    coeffs_H[0] *= 0
    
    # Reconstruction
    imArray_H = pywt.waverec2(coeffs_H, mode)
    imArray_H *= 255
    imArray_H = np.uint8(imArray_H)
    
    return imArray_H
