# Flask imports:
from flask import Flask, render_template, request, Response, redirect, flash
from flask import jsonify, abort, send_file, url_for
app = Flask(__name__)
app.secret_key = 'icardioai'

# Script imports:
import os
import sys
import json
from pprint import pprint
from time import time, sleep
import subprocess

# Pipeline imports:
sys.path.insert(1, '/internal_drive/echo_production_pipeline/Pipeline')
#import ProductionPipeline as pl
#import Tools.ProductionTools as tools



# Accepts file path, deletes all files in file path:
def DeleteFilesInPath(file_path, verbose=False, start=time()):
    
    file_list = os.listdir(file_path)
    
    for file in file_list:
        os.remove(file_path + file)
    
    if verbose:
        print('[@ %7.2f s] [DeleteFilesInPath]: cleared  [%s]' %(time()-start, file_path))

        
        
# Accepts list of files, returns message, status:
def CheckForDicoms(files, verbose=False, start=time()):

    # no files are submitted:
    if len(files) == 0:
        message = 'No files submitted'
        status = -1
        return message, status

    # file other than dicom submitted:
    for file in files:
        if file.filename[-3:] != 'dcm':
            message = '[%s] is not a dicom' %(file.filename)
            status = -2
            return message, status
    
    # file list okay:
    message = 'Reading dicoms'
    status = 1

    if verbose:
        print('[@ %7.2f s] [CheckForDicoms]: Verified file list' %(time()-start))

    return message, status



# Variables:
verbose = True
start = time()   
file_paths = {
    'upload_directory' : '/internal_drive/Dicoms/',
    'dicoms_directory' : '/ineternal_drive/echo_production_pipeline/',
    'status_file' : '/internal_drive/echo_production_pipeline/Flask/static/status.txt',
}



# Landing page:
@app.route('/', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def index():
   
    # default message:
    message = "Drag and drop or click to select your set of Dicoms to analyze."

    # execute on post method:
    if request.method == 'POST':
        
        # get file list from request:
        files = request.files.getlist('dicoms')
        print(files[0].filename)
        
        # check request for dicom files:
        message, status = CheckForDicoms(files, verbose, start)
        
        # raise error if incorrect file types are submitted:
        if (status == -1) or (status == -2):
            return render_template('uploader.html', message=message)
        
        # delete existing files in upload folder:
        print('here')
        DeleteFilesInPath(file_paths['upload_directory'], verbose, start)
        
        # upload new files:
        [file.save(os.path.join(file_paths['upload_directory'], file.filename)) for file in files] 
        
        return redirect('/loader')
    
    return render_template('uploader.html', message=message)



# Loader page:
@app.route('/loader')
def loader():
    print('route to loader')
    # execute backend pipeline:
    command = ['python3 -u /internal_drive/echo_production_pipeline/Pipeline/ProductionPipeline.py > ' + file_paths['status_file']]

    proc = subprocess.Popen(
        command,             
        shell=True,
        stdout=subprocess.PIPE
    )

    return render_template('loader.html')
    


@app.route('/results')
def app_page():
    
    return render_template('app.html')
    
    
    
# Return json object:
@app.route('/reports', methods=['GET', 'POST'])
def reports():
    
    print('routed to reports')
    
    # initialize variables:
    reports_json = '/internal_drive/Reports/reports.json'
    
    # read json file:
    with open(reports_json) as json_file:
        json_data = json.load(json_file)
        
    # return json file:
    response = jsonify(json_data)
    
    return response



# Return video files:
@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    
    # parse file path:
    req_path = '/' + req_path
    
    # return 404 if path doesn't exist
    if not os.path.exists(req_path):
        print(req_path)
        return abort(404)

    # check if path is a file and serve
    if os.path.isfile(req_path):
        return send_file(req_path)
    
    return render_template('app.html')


   
# Main: 
if __name__ == "__main__":
    
    # Intialize script:
    #tools.InitializeScript(os.path.basename(__file__), verbose, start)
    
    # Run app:
    app.run(debug=True)        
    

