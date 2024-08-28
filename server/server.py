from flask import flask, jsonify


app=flask(__name__)

@app.route("/api/users",methods=['GET'])

def users():
    return jsonify(
        {
            "users":[
                'arpan',
                'zach',
                'jessie'
                
            ]
        }
    )



if __name__ == "__main__":
    app.run(debug=True, port=8080)