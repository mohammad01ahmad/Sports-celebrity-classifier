# Sports Classifier – Football Icons Recognition ⚽  

This project classifies images of three world-famous football icons using **computer vision** and **machine learning**.  

Why football? Because it’s a sport I watch regularly — and since nobody asked, yes, I’m a **Manchester City fan** 💙.  

---

## 🔍 How it works
- **Face & Eye Detection:** Images are preprocessed by extracting faces and eyes using Haar Cascade classifiers (`haarcascade_frontalface_default.xml` and `haarcascade_eye.xml`).  
- **Feature Engineering:** Cropped face regions are combined (stacked) with the original images to improve feature representation.  
- **Model Training:** Multiple ML models were trained and fine-tuned using **GridSearchCV** for hyperparameter optimization.  
- **Best Model:** The final model chosen was **Support Vector Machine (Linear kernel)**, achieving **~89% accuracy** on the validation set.  
- **Model Serving:** The trained model (`best_model.pkl`) and class dictionary (`class_dict.json`) are stored inside the `artifacts/` folder. Predictions are served through a **Flask REST API**.  

---

## ⚙️ Tech Stack
- **Python**: Data preprocessing, model training, and backend  
- **OpenCV**: Image preprocessing (face/eye detection, cropping)  
- **scikit-learn**: Model training, hyperparameter tuning  
- **Flask**: API to serve predictions  
- **Frontend (HTML, CSS, JS):** A simple web interface for image upload and results display  
  > Note: The frontend code was generated with the help of Claude.ai (I focus more on backend + ML).  

---

## 📂 Project Structure
