from flask import Flask, jsonify, render_template
from flask_cors import CORS
import os

template_dir = os.path.abspath('../templates')  # Set the absolute path to templates
app = Flask(__name__, template_folder=template_dir)
cors = CORS(app,origins='*')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/')
def about():
    return render_template('about.html')

@app.route('/api/data')
def get_data():
    return jsonify({"message": "API data response"})

if __name__ == '__main__':
    app.run(debug=True) #convert it to false in prod
    
    
