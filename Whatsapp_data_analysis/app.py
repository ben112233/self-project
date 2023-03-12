from flask import Flask, Response, redirect, render_template, request, jsonify, url_for, send_file
from flask_cors import CORS
import json
import os


import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import re
import seaborn as sns
from datetime import datetime
from matplotlib.ticker import MaxNLocator

from werkzeug.utils import secure_filename
from db import db_init, db
from models import Img

UPLOAD_FOLDER = 'text'
IMAGE_FOLDER = 'static\images'

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def start():
    return render_template("index.html")

@app.route('/upload_static_file', methods=['POST'])
def upload_static_file():
    print("Got request in static files")
    print(request.files)
    f = request.files['static_file']
    f.save('text.txt')
    resp = {"success": True, "response": "file saved!"}
    return f.read(), 200

@app.route('/new', methods=['POST'])
def new():
    return render_template('plot.html')

app.config['UPLOAD_IMAGE'] = IMAGE_FOLDER
@app.route('/run', methods=['POST'])
def index():
    import main
    run = True
    while run:
        if os.path.exists(r'text.txt'):
            main.main()

            #basic_info, get_author_info
            analysis_on_day = os.path.join(app.config['UPLOAD_IMAGE'], 'analysis_on_day.png')
            get_most_active_member = os.path.join(app.config['UPLOAD_IMAGE'], 'get_most_active_member.png')
            most_media_by_author = os.path.join(app.config['UPLOAD_IMAGE'], 'most_media_by_author.png')
            get_most_word_by_author = os.path.join(app.config['UPLOAD_IMAGE'], 'get_most_word_by_author.png')
            no_link_share = os.path.join(app.config['UPLOAD_IMAGE'], 'no_link_share.png')
            active_hour = os.path.join(app.config['UPLOAD_IMAGE'], 'active_hour.png')
            active_date = os.path.join(app.config['UPLOAD_IMAGE'], 'active_date.png')
            graph_of_message_vs_month = os.path.join(app.config['UPLOAD_IMAGE'], 'graph_of_message_vs_month.png')
            active_month = os.path.join(app.config['UPLOAD_IMAGE'], 'active_month.png')
            message_vs_year = os.path.join(app.config['UPLOAD_IMAGE'], 'message_vs_year.png')
            run = False
        else:
            run = True
    os.remove(r'text.txt')
    return render_template('test.html', image = analysis_on_day
                                      , image2 = get_most_active_member
                                      , image3 = most_media_by_author
                                      , image4 = get_most_word_by_author
                                      , image5 = no_link_share
                                      , image6 = active_hour
                                      , image7 = active_date
                                      , image8 = graph_of_message_vs_month
                                      , image9 = active_month
                                      , image10 = message_vs_year)

@app.route('/upload' , methods=['POST'])
def upload():
    pic = request.files['pic']

    if not pic:
        return 'No pic uploaded ', 400

    filename=secure_filename(pic.filename)
    mimetype=pic.mimetype

    img=Img(img=pic.read(), mimetype=mimetype, name=filename)
    db.session.add(img)
    db.session.commit()
    return 'Img has been uploaded!', 200

if __name__ == "__main__":
	app.run(debug=True)