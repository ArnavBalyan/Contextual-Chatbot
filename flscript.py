from flask import Flask, Response, request
from flask import render_template, make_response
from flask_restful import Resource, Api
import numpy as np
import psycopg2

app = Flask(__name__)
api = Api(app)

def formt(list1):
	return str(list1).replace('(','').replace(')','').replace(',','')
def formt1(list1):
	sa1 = str(list1).replace('(','').replace(')','')
	return sa1[2:len(sa1)-3]
def formt2(list1):
	sample = str(list1).replace('(','').replace(')','').replace(',','').replace('[','').replace("]",'')
	ec = 0
	for i in range (len(sample)):
		if sample[i] == "'":
			ec = ec+1
			if ec%2 == 0 and i < len(sample)-1:
				sa = list(sample)
				sa[i] = ","
				sample = ''.join(sa)
	return sample.replace('(','').replace(')','').replace("'",'')
def unique(x):
	return list(dict.fromkeys(x))

class data():
    def __init__(self, Title, Author, Journal, Url):
        self.Title = Title
        self.Author = Author
        self.Journal = Journal
        self.Url = Url

class Display(Resource):
	def get(self, string1):
		input_keyword = string1
		con = psycopg2.connect(host = 'localhost', database = '<Database Name>', user = '<Database Username>', password = '<Database Password>')
		cur = con.cursor()
		cur.execute("select dspace_object_id from metadatavalue where text_value ILIKE '%{}%'".format(input_keyword))
		#cur.execute("select text_value from metadatavalue where text_value ILIKE '%{}%'".format(input_keyword))
		rows = cur.fetchall()
		if(rows):
			rows = unique(rows)
			#print(rows)
			Title = []
			Author = []
			Journal = []
			Url =[]
			for i in range (len(rows)):
				obj = formt(rows[i])
				cur.execute("select text_value from metadatavalue where metadata_field_id = 31 and dspace_object_id = {}".format(obj))
				ss = formt2(cur.fetchall())
				if(ss):
					Url.append(ss) 
				else:
					continue
				cur.execute("select text_value from metadatavalue where metadata_field_id = 70 and dspace_object_id = {}".format(obj))
				Title.append(formt1(cur.fetchall()))
				cur.execute("select text_value from metadatavalue where metadata_field_id = 9 and dspace_object_id = {}".format(obj))
				Author.append(formt2(cur.fetchall()))    
				cur.execute("select text_value from metadatavalue where metadata_field_id = 24 and dspace_object_id = {}".format(obj))
				Journal.append(formt1(cur.fetchall()))
			cur.close()
			con.close()	
			return make_response(render_template("result.html",title = Title, author = Author, journal = Journal, url = Url))
		return make_response("Unexpected Error")
api.add_resource(Display, '/search/v1/<path:string1>')

if __name__ == '__main__':
	app.run()