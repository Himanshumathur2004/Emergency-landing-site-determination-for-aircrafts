from flask import Flask, request, render_template, redirect, url_for
import cv2
import numpy as np
from ultralytics import YOLO
import os

app = Flask(__name__)
model = YOLO("Models/best.pt")  # Make sure this path is correct!

@app.route('/')
def home():
    return render_template("upload.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return "No image uploaded!"
        
        file = request.files['image']
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        
        # Run detection (updated part)
        results = model(img)  # This returns a list of Results objects
        for r in results:     # Loop through results (usually just one)
            img = r.plot()    # This generates the image with boxes
        
        # Save result
        os.makedirs("static", exist_ok=True)
        output_path = "static/result.jpg"
        cv2.imwrite(output_path, img)
        
        return redirect(url_for('result'))
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/result')
def result():
    return render_template("result.html", result_image="static/result.jpg")

if __name__ == '__main__':
    app.run(debug=True)