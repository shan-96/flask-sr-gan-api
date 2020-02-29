import os
import glob
from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)


@app.route("/")
def file_front_page():
    return render_template('fileform.html')


@app.route("/handleUpload", methods=['POST'])
def handle_file_upload():
    photo = ""
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            filename = os.path.join('./static/', photo.filename)
            photo.save(filename)
    return render_template("viewFile.html", filename=photo.filename)
    # return redirect(url_for('view_loaded_image'))


@app.route("/afterUpload", methods=['POST'])
def delete_img_and_home():
    files = glob.glob('./static/*')
    for f in files:
        os.remove(f)
    return render_template('fileform.html')


if __name__ == '__main__':
    app.run()
