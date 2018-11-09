import os
import subprocess
from qtlaas_automation import create_worker_snapshot, remove_cluster_worker, get_master_floating_ip, find_new_workers
from get_ansible_workers  import return_workers
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
existing_network = True

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_token():
	f = open("token.txt")
	line = f.readline()
	f.close()
	return line



@app.route('/')
def hello_world():
	print("hi!")
	return 'Why are you is this part of the server?'

@app.route('/create/<x>')
def create_qtlaas(x):
	#Start process of creating the network by running the script for that with x number of workers
	somethingwentwrong = "Something went wrong during the creation of the workers, check the number below.\n"
	x=int(x)
	if not existing_network:
		subprocess.check_output(['chmod', '+x', 'setup_master.sh'])
		response = subprocess.check_output(['sudo', './setup_master.sh'])
		workers_started = 1
		workercreationfail = False
		if x > 1:
			for i in xrange(1, x):
				if (create_worker_snapshot()):
					workers_started = workers_started + 1
				else:
					workercreationfail = True
			find_new_workers()
	if existing_network:
		return configure_number_of_workers(x)
	
	sparkmasteraddress = 'http://' + get_master_floating_ip() + ':60060'
	token = get_token()
	returnstring = "Number of workers started: " + str(workers_started) + "\n Address to Spark Master: " + sparkmasteraddress + " \n Token: " + token
	if not workercreationfail:
		return  returnstring
	else:
		return somethingwentwrong + returnstring

@app.route('/workers/<x>')
def configure_number_of_workers(x):
	#Configure the number of workers available by either destroying a number of 
	x=int(x)
	if not existing_network:
		return "QTLaaS has not been started!"
	else:
		current_number_of_workers = len(return_workers())
		if current_number_of_workers == x:
			return "Number of workers are already at " + str(x) + "."
		elif (current_number_of_workers > x):
			failcounter = 0
			while current_number_of_workers > x:
				if (remove_cluster_worker()):
					current_number_of_workers = current_number_of_workers - 1
					failcounter = 0
				else:
					failcounter = failcounter + 1
					if failcounter > 2:
						return "Something went wrong when deleting workers. Number of workers still active: " + str(current_number_of_workers)
			return "New number of workers: " + str(len(return_workers()))

		else:
			workercreationfail = False
			new_workers_to_add = x - current_number_of_workers
			i = 0
			while i < new_workers_to_add:
				if (create_worker_snapshot()):
					i = i + 1
				else:
					workercreationfail = True
					i = i + 1
			print(find_new_workers())
			return "boiNew number of workers: " + str(len(return_workers()))


@app.route('/destroy')
def destory():
	return "It worked."
	number_of_workers = return_workers().length()
	failcounter = 0
	while (number_of_workers > 0):
		if (remove_cluster_worker()):
			number_of_workers = number_of_workers - 1
			failcounter = 0
		else:
			failcounter = failcounter + 1
			if failcounter > 2:
				return "Something went wrong when deleting workers. Number of workers still active: " + number_of_workers

	return 'All workers have been destroyed!,'

@app.route('/token')
def token():
	sparkmasteraddress = 'http://' + get_master_floating_ip() + ':60060'
	token = get_token()
	#Return the latest token
	return "Address to Spark Master: " + sparkmasteraddress + " \n Token: " + token


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
	if (os.path.isdir(os.path.dirname(os.path.realpath(__file__)) + '/uploads/')):
		#app.run(debug=True) #For Internal
		app.run(host="0.0.0.0", debug=True) #For external
	else: 
		os.mkdir('uploads')
		#app.run(debug=True) #For Internal
		app.run(host="0.0.0.0", debug=True) #For external
