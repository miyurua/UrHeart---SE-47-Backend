from distutils.log import debug
from flask import Flask
from flask_restful import Resource, Api


app=Flask(__name__)
api=Api(app)

@app.route('/test')
def test():
    return "Hello World"

app.run(debug=True)
