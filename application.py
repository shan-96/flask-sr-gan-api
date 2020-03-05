import os
import glob
from flask import Flask, request, render_template, url_for, redirect
import generator

application = Flask(__name__)


@application.route("/")
def file_front_page():
    return render_template('fileform.html')


@application.route("/handleUpload", methods=['POST'])
def handle_file_upload():
    photo = ""
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            filename = os.path.join('./static/', photo.filename)
            photo.save(filename)
    html = generator.generateSR(filename)
    return render_template("viewGAN.html", data=html)
    # return render_template("viewFile.html", filename=photo.filename)
    # return redirect(url_for('view_loaded_image'))


@application.route("/afterUpload", methods=['POST'])
def delete_img_and_home():
    files = glob.glob('./static/*')
    for f in files:
        os.remove(f)
    return render_template('fileform.html')


if __name__ == '__main__':
    application.run(host='0.0.0.0')
