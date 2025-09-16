'''
============================================================================
util.py file, that stores all the backend functions
============================================================================

This file contains the function classify_image function that takes in the 
inputimage, processes it and feeds it into the model for prediction. 

----------------------------------------------------------------------------
'''

import cv2
import numpy as np
import base64
import joblib
import pywt
import json

__class_name_to_number = {}
__class_number_to_name = {}
__model = None

def classify_image(image_base64_data, file_path=None):
    #Classify image and return class name with probabilities

    imgs = get_cropped_image_if_2_eyes(file_path, image_base64_data)

    if not imgs:
        return {
            'error': 'No face with 2 eyes detected',
            'faces found': 0
        }

    results = []

    for i, img in enumerate(imgs):
        try:
            # Feature extraction 
            scaled_raw_img = cv2.resize(img, (32, 32))
            img_har = w2d(img, 'db1', 5)
            scaled_img_har = cv2.resize(img_har, (32, 32))

            # Flatten features
            raw_features = scaled_raw_img.reshape(32*32*3, 1)
            har_features = scaled_img_har.reshape(32*32, 1)

            # Combine features
            combined_img = np.vstack([raw_features, har_features])

            # Reshapre for model input
            final_features = combined_img.reshape(1, 32*32*3 + 32*32).astype(float)

            # Get prediction and probabilities
            prediction = __model.predict(final_features)[0]
            probabilities = __model.predict_proba(final_features)[0]

            # Convert class number to name 
            predicted_class_name = __class_number_to_name[str(prediction)]

            # Create probability dictionary with class names
            class_probabilities = {}
            for class_num, prob in enumerate(probabilities, 1): 
                class_name = __class_number_to_name[str(class_num)]
                class_probabilities[class_name] = round(float(prob), 4)
            
            confidence = round(float(np.max(probabilities)), 4)

            results.append({
                'face_id' : i+1,
                'predicted_class': predicted_class_name,
                'confidence': confidence,
                'class_probabilities': class_probabilities,
            })
        
        except Exception as e:
            results.append({
                'face_id' : i+1,
                'error': f'Error processing face: {str(e)}'
            })
            
    if len(results) == 1:
        return results[0]
    else:
        return{
            'total_faces' : len(results),
            'results': results
        }
    
def load_saved_artifacts():
    # Load model and class dictionaries

    print("Loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name
    global __model
    
    try:
        # Load class dictionaries
        with open("server/artifacts/class_dictionary.json", "r") as f:
            __class_name_to_number = json.load(f)

        with open("server/artifacts/class_dictionary_reverse.json", "r") as f:  
            __class_number_to_name = json.load(f)  
        
        # Load model
        if __model is None:
            with open('server/artifacts/best_saved_model.pkl', 'rb') as f:
                __model = joblib.load(f)

        print("Loading saved artifacts...done")
        print(f"Loading classes: {list(__class_name_to_number.keys())}")

    except Exception as e:
        print(f"Error loading artifacts: {str(e)}")

def w2d(img, mode='haar', level=1):
    """
    Apply 2D wavelet transform to extract features
    """
    imArray = img
    
    # Convert to grayscale if image is colored
    if len(imArray.shape) == 3:
        imArray = cv2.cvtColor(imArray, cv2.COLOR_BGR2GRAY)  
    
    # Convert to float
    imArray = np.float32(imArray)
    imArray /= 255.0
    
    # Compute wavelet decomposition
    coeffs = pywt.wavedec2(imArray, mode, level=level)  
    
    # Process Coefficients - zero out approximation coefficients
    coeffs_H = list(coeffs)
    coeffs_H[0] *= 0
    
    # Reconstruction
    imArray_H = pywt.waverec2(coeffs_H, mode)
    imArray_H *= 255
    imArray_H = np.uint8(imArray_H)
    
    return imArray_H


def get_cv2_image_from_b64_string(b64_string):
    # Convert base64 string to cv2 image

    try:
        # Handle data URL format
        encoded_data = b64_string.split(',')[1] if ',' in b64_string else b64_string

        # Decode base64 to bytes
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)

        # Convert to cv2 image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Decoded image is None. Please check the base64 string.")
        else: 
            return img
    except Exception as e:
        return f"Could not convert b64 string to image: {str(e)}"

def get_cropped_image_if_2_eyes(image_path, image_base64_data):
    # Detect face and eyes, return cropped face images with 2 eyes

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_b64_string(image_base64_data)
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    cropped_faces = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        if len(eyes) >= 2:
            cropped_faces.append(roi_color)

    return cropped_faces
        
def get_b64_image():
    # Read base64 image from file for testing
    try:
        with open("test/b64.txt") as f:
            return f.read().strip()
        
    except Exception as e:
        return f"Error reading b64 image from file: {str(e)}"

def test():
    # Test function 
    print("Testing function...")
    try: 
        b64_image = get_b64_image()

        if b64_image is None:
            return f"Image could not be loaded for testing"
        else:
            response = classify_image(b64_image, None)
            print(response)

    except Exception as e:
        print(f"Error in test function: {str(e)}")
        return None


if __name__ == "__main__":
    load_saved_artifacts()
    # test()
    print(classify_image(None, "test/test_ageuro.jpg"))
    
