#imports
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import base64
import cv2
import random


app = Flask(__name__)
app.static_folder = "Styles"
app.config['SECRET_KEY'] = 'super'
app.config['UPLOAD_FOLDER'] = 'files'

# form class definition
class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Detect Faces")

@app.route("/home", methods=["GET", "POST"])
def homePage():
    form = UploadFileForm()
    
    if form.validate_on_submit():
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
             # Make sure the directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Print filepath for debugging
            print("Filepath:", filepath)
            
            file.save(filepath)
            
            # Perform face detection on the uploaded image using OpenCV
            image = cv2.imread(filepath)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_data = cv2.CascadeClassifier('AI Face Detector App Project\haarcascade_frontalface_default.xml')
            detected_faces = face_data.detectMultiScale(gray_image)

            # Draw rectangles around the detected faces
            for (x, y, w, h) in detected_faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (random.randrange(256),random.randrange(256),random.randrange(256)),10)
            
            # Save the image with detected faces
            result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_' + filename)
            cv2.imwrite(result_path, image)

            # Encode the image to base64 to display directly in HTML
            with open(result_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode("utf-8")

            return render_template('results.html', img_data=img_data)
    
    return render_template("index.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
