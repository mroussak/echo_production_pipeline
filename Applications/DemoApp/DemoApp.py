from flask import Flask, render_template, request, Response, redirect, flash
from flask import jsonify, abort, send_file, url_for
import os
app = Flask(__name__)
app.secret_key = 'icardioai'
        


# Landing page:
@app.route('/')
def index():
   return render_template('index.html')



# Demo page:
@app.route('/demo')
def demo_page():
    
    return render_template('demo.html')
    

# Return object at given path:
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
    
    return render_template('demo.html')



# Dev functions:
if __name__ == "__main__":
    
    app.run(debug=True, use_reloader=False)
