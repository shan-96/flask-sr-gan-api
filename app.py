import os
from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)


@app.route("/")
def file_front_page():
    return render_template('fileform.html')


@app.route("/handleUpload", methods=['POST'])
def handle_file_upload():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            photo.save(os.path.join('./static/', 'image1.png'))
    return render_template("viewFile.html")
    #return redirect(url_for('view_loaded_image'))


@app.route("/afterUpload")
def view_loaded_image():
    return render_template('viewFile.html')


if __name__ == '__main__':
    app.run()
