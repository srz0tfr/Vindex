#import libraries
import numpy as np
from flask import Flask, request, jsonify, render_template
# import pickle
# from flask_pymongo import PyMongo
# import cloudinary as Cloud
import os
from werkzeug.utils import secure_filename
# import get_annotation
import get_segmentation
import uuid

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#Initialize the flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# mongo = PyMongo(app)
# model = pickle.load(open('model.pkl', 'rb'))

#default page of our web-app
@app.route('/')
def home():
    return render_template('index.html')

#To use the predict button in our web-app
@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    # return '''
    # <img src="{{url_for('static', filename='back_img.png')}}" alt = "why?" />
    # '''
    model = 1
    if request.form['model_video'] == "Sparse Trained with many labels":
        model = 2
    elif request.form['model_video'] == "Wise Trained with heading/non-heading labels":
        model = 3
    elif request.form['model_video'] == "Sparse Trained with heading/non-heading labels":
        model = 4

    # if 'video' in request.files:
    #     video = request.files['video']
    #     # return video
    #     filename = secure_filename(video.filename)
    #     video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     # print(video.read())
    #     video_annotation = get_annotation.get_annotation(filename,video)
    #     return render_template('index.html',annotation = video_annotation)
    return render_template('index.html')

@app.route('/visualize',methods=['POST'])
def visualize():
    if 'slide_image' in request.files:
        slide_image = request.files['slide_image']
        # mongo.save_file(slide_image.filename,slide_image)
        # img = mongo.send_file(slide_image.filename)
        # print(type(img))
        model = 1
        if request.form['model_image'] == "Sparse Trained with many labels":
            model = 2
        elif request.form['model_image'] == "Wise Trained with heading/non-heading labels":
            model = 3
        elif request.form['model_image'] == "Sparse Trained with heading/non-heading labels":
            model = 4

        if slide_image:
            filename = secure_filename(slide_image.filename)
            print(filename)
            # slide_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            slide_image.save(os.path.join(app.root_path, 'static', filename))
            # latestfile.save(os.path.join(app.root_path, 'static', 'customlogos', 'logo.png'))
            file_vis = str(uuid.uuid4()) + '.png'
            file_box = str(uuid.uuid4()) + '.png'
            get_segmentation.get_segmentation(filename,model,1, file_vis, file_box)
            # file_vis =  'output_vis_' + os.path.basename(filename)[:-4] + '.png'
            # file_box = 'output_box_' + os.path.basename(filename)[:-4] + '.png'
            return  render_template('index.html', image_vis = file_vis, image_box = file_box)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')