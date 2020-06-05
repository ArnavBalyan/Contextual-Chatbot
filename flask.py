from flask import Flask, Response, request
from flask import render_template, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Display(Resource):
	def get(self, string1):
		headers = {'Content-Type': 'text/html'}
		return make_response(render_template("result.html",result= "{}".format(string1)))
