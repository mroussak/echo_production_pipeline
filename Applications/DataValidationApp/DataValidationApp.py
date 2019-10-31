# Flask imports:
from flask import Flask, render_template, request, Response, redirect, flash
from flask import jsonify, abort, send_file, url_for
app = Flask(__name__)
app.secret_key = 'icardioai'
        
# Script imports:
import Components.FileHandler as files
import Components.Security as security
import Components.Sessions as sessions
import Components.Users as users
from time import time, sleep
from pprint import pprint
import subprocess
import json
import sys
import os

# Database imports:
#sys.path.insert(0, '/internal_drive/echo_production_pipeline/Database/EchoData/')
sys.path.insert(0, '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/')
import PostgresCaller



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


   
# Main: 

# Variables:
verbose = True
start = time()   
file_paths = {
    'status_file' : '/internal_drive/echo_production_pipeline/Flask/static/status.txt',
}

# Intialize script:
tools.InitializeScript(os.path.basename(__file__), verbose, start)

# Dev functions:
if __name__ == "__main__":
    
    # Launch app:
    app.run(debug=True, use_reloader=False)
