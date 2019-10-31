# Flask imports:
from flask import Flask, render_template, request, Response, redirect, flash
from flask import jsonify, abort, send_file, url_for
app = Flask(__name__)
app.secret_key = 'icardioai'
        
# Script imports:
import ProductionWebApp.Components.FileHandler as files
import ProductionWebApp.Components.Security as security
import UserLoginApp.Components.Sessions as sessions
import UserLoginApp.Components.Users as users
from time import time, sleep
from pprint import pprint
import subprocess
import json
import sys
import os

# Pipeline imports:
sys.path.insert(1, '/internal_drive/echo_production_pipeline/Pipeline/ProductionPipeline/')
from Components.Models import ModelsPipeline
import Tools.ProductionTools as tools
import ProductionPipeline



# Landing page:
@app.route('/app', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload():
   
    # variables:
    verbose = True
   
    # default message:
    message = "Drag and drop or click to select your set of Dicoms to analyze."
    
    # TODO
    # get user and session details: 
    #user_directory = users.GetUserID(None, verbose)
    #session_directory = sessions.GetSessionID(None, verbose)
    user_directory = 'UserID1'
    session_directory = 'SessionID1'
    
    # build directories:
    root_directory = files.BuildRootDirectory(user_directory, session_directory, verbose)
    files.BuildDirectoryTree(root_directory, verbose)
    
    # execute on post method:
    if request.method == 'POST':
        
        # get file list from request:
        file = request.files['filePond']
        
#         # check request for dicom files:
#         message, status = CheckForDicoms(files, verbose, start)
        
#         # raise error if incorrect file types are submitted:
#         if (status == -1) or (status == -2):
#             return render_template('uploader.html', message=message)
        
        print('here')
        
        # upload new files:
        upload_directory = root_directory + '/Dicoms/'
        file.save(os.path.join(upload_directory, file.filename))
        
        print('[upload]: saved [%s] to [%s]' %(file.filename, upload_directory))
        
        return render_template('upload.html', message=message)
    
    return render_template('upload.html', message=message)



# Info page
@app.route('/')
def home():
    return render_template('index.html')



# Loader page:
@app.route('/loader')
def loader():
    
    print('[loader]: route to loader')
    
    # TODO
    # get user and session details: 
    #user_directory = users.GetUserID(None, verbose)
    #session_directory = sessions.GetSessionID(None, verbose)
    user_directory = 'UserID1'
    session_directory = 'SessionID1'
    
    # Variables:
    start = time()
    
    # execute backend pipeline:
    ProductionPipeline.main(user_id = user_directory, session_id = session_directory, start = start)
    
    print('[loader]: end of loader')
    
    return render_template('loader.html')
    


@app.route('/demo')
def demo_page():
    
    return render_template('demo.html')
    
    
    
@app.route('/results')
def app_page():
    
    return render_template('app.html')
    
    
    
# Return json object:
@app.route('/reports', methods=['GET', 'POST'])
def reports():
    
    print('[reports]: routed to reports')
    
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
def get_file(req_path):
    
    # parse file path:
    req_path = '/' + req_path
    
    # return 404 if path doesn't exist
    if not os.path.exists(req_path):
        print('[get_file]: requested path [%s] not found'  %(req_path))
        return abort(404)

    # check if path is a file and serve
    if os.path.isfile(req_path):
        return send_file(req_path)
    
    return render_template('app.html')


   
# Main: 

# Variables:
verbose = True
start = time()   
file_paths = {
    'status_file' : '/internal_drive/echo_production_pipeline/Flask/static/status.txt',
}

# Intialize script:
tools.InitializeScript(os.path.basename(__file__), verbose, start)

# Load models:
#ModelsPipeline.main(start=time())

# Dev functions:
if __name__ == "__main__":
    
    # Launch app:
    os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    app.run(debug=True, use_reloader=False)
