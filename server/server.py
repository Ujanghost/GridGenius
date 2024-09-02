from flask import Flask, jsonify, render_template
import os

template_dir = os.path.abspath('../templates')  # Set the absolute path to templates
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    return jsonify({"message": "API data response"})

if __name__ == '__main__':
    app.run(debug=True)
