import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/nurre/QTLaaS/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
	print("hi!")
	return 'Why are you is this part of the server?'

@app.route('/create/<x>')
def create_qtlaas(x):
	#Start process of creating the network by running the script for that with x nuber of workers
	return 'Creating QTLaaS...\n[REMOVE THIS WHEN IMPLEMENTED]'

@app.route('/workers/<x>')
def configure_number_of_workers(x):
	#Configure the number of workers available by either destroying a number of 
	#workers or by creating some with a script.
	return 'Configuring the number of workers...\n[REMOVE THIS WHEN IMPLEMENTED]'

@app.route('/destroy')
def destory():
	#Deletes the master and the worker nodes.
	return 'Deleting all available worker and master nodes...\n[REMOVE THIS WHEN IMPLEMENTED]'

@app.route('/status')
def status():
	#Return the status of the network.
	return 'Is it burning yet? Are are we good?\n[REMOVE THIS WHEN IMPLEMENTED]'


# @app.route('/upload')
# def fileupload():
# 	#Upload file.
# 	return 'Uploading file...'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <h2>Är vi här? Yup</h2>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
	#app.run(debug=True) #For Internal
	app.run(host=0.0.0.0, debug=True) #For external
