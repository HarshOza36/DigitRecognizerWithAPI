from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify, send_from_directory, Response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators, IntegerField
from wtforms.validators import InputRequired, Email, Length, ValidationError, Regexp
import logging
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
import cv2
import numpy as np
import jsonpickle

app = Flask(__name__, static_folder='static')

app.config["SECRET_KEY"] = "THISISsecretkey!"
app.config["IMAGE_UPLOADS"] = "static\\img\\uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = [
    "JPEG", "JPG", "PNG", "GIF", "png", "jpg"]


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/')
def index():
    return "Use /upload-image route"


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    pred = "No File Chosen Yet"
    chosen = ""
    model = tf.keras.models.load_model(
        'models/kfulldrmodeldigit')
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                print("No filename")
                return redirect(request.url)
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print("Image saved")
                originalImage = cv2.imread(
                    "static\\img\\uploads\\"+str(filename))
                grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
                (thresh, blackAndWhiteImage) = cv2.threshold(
                    grayImage, 127, 255, cv2.THRESH_BINARY)
                # resizing the image
                blackAndWhiteImage = cv2.resize(
                    blackAndWhiteImage, (28, 28), interpolation=cv2.INTER_AREA)
                print(type(blackAndWhiteImage))
                blackAndWhiteImage = blackAndWhiteImage.reshape((1, 28, 28, 1))
                print(blackAndWhiteImage.shape)
                p = model.predict_classes(blackAndWhiteImage)
                print(type(p))
                print(p)
                print(p[0])
                pred = p[0]
                chosen = filename
                imgfile = "static\\img\\uploads\\"+str(filename)
                # return redirect(request.url)
                return render_template("digitrecog.html", pred="Prediction:"+str(pred), chosen="FileName:"+str(chosen), imgfile=imgfile)
            else:
                print("That file extension is not allowed")
                return redirect(request.url)
    return render_template("digitrecog.html")


@app.route('/api/test', methods=['POST'])
def test():
    r = request
    print(r)
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    print(nparr)
    # decode image
    originalImage = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print(originalImage)
    # do some fancy processing here....
    model = tf.keras.models.load_model(
        'models/kfulldrmodeldigit')
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(
        grayImage, 127, 255, cv2.THRESH_BINARY)
    # resizing the image
    blackAndWhiteImage = cv2.resize(
        blackAndWhiteImage, (28, 28), interpolation=cv2.INTER_AREA)
    blackAndWhiteImage = blackAndWhiteImage.reshape((1, 28, 28, 1))
    p = model.predict_classes(blackAndWhiteImage)
    print(p[0])
    pred = p[0]

    # build a response dict to send back to client
    #response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
    response = {'message': 'Prediction is {} '.format(pred)}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


if __name__ == '__main__':
    app.run(port=50000, debug=True)
