import os
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, url_for, flash, render_template, session
from skimage import io
from skimage.transform import resize
from sklearn import svm
import pickle
from sklearn.preprocessing import StandardScaler

UPLOAD_FOLDER = "/uploads"
ALLOWED_EXTENSIONS = set(['pdf','png','jpg', 'jpeg', 'gif'])
scaler = pickle.load(open('scaler.pkl', 'rb'))
model = pickle.load(open('topmodel.pkl', 'rb'))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

class global_file():
    name = ''

@app.route("/")
def viz_page():
    #opens home page
    with open("templates/home.html", 'r') as viz_file:
        return viz_file.read()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 'No file!'
        if file and allowed_file(file.filename):
            global scaler
            global model
            filename = secure_filename(file.filename)
            global_file.name=filename
            img = io.imread(file, as_grey=False)
            resized = resize(img, (32, 32)).reshape(1,-1)
            x = scaler.transform(resized)
            ypred = model.predict(x)
            if ypred == 1:
                return redirect(url_for('success'))
            else:
                return redirect(url_for('failure'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/success')
def success():
    filename = global_file.name
    return render_template('success.html', filename=filename)

@app.route('/failure')
def failure():
    filename = global_file.name
    return render_template('fail.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)