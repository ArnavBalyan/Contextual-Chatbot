from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
import numpy as np
import psycopg2
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
class ActionDefaultFallback(Action):

   def name(self):
      return "action_default_fallback"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("I am sorry, I did not understand what you meant.")

class ActionDatabaseSearch(Action):

	def name(self) -> Text:
		return "action_database_search"
	def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		input_keyword = tracker.get_slot("keyword")
		con = psycopg2.connect(host = 'localhost', database = 'backend_data', user = 'postgres', password = 'p@ss2hell')
		cur = con.cursor()
		cur.execute("select dspace_object_id from metadatavalue where text_value ILIKE '%{}%'".format(input_keyword))
		#cur.execute("select text_value from metadatavalue where text_value ILIKE '%{}%'".format(input_keyword))
		rows = cur.fetchall()
		rows = unique(rows)
		#print(rows)
		Title = []
		Author = []
		Journal = []
		Url =[]
		response_string = "Here is what I found: \n"
		for i in range (len(rows)):
			obj = formt(rows[i])
			cur.execute("select text_value from metadatavalue where metadata_field_id = 70 and dspace_object_id = {}".format(obj))
			Title.append(formt1(cur.fetchall()))
			cur.execute("select text_value from metadatavalue where metadata_field_id = 9 and dspace_object_id = {}".format(obj))
			Author.append(formt2(cur.fetchall()))    
			cur.execute("select text_value from metadatavalue where metadata_field_id = 24 and dspace_object_id = {}".format(obj))
			Journal.append(formt1(cur.fetchall()))
			cur.execute("select text_value from metadatavalue where metadata_field_id = 31 and dspace_object_id = {}".format(obj))
			Url.append(formt2(cur.fetchall()))
			response_string += "\t {} {} by {} published in {} available at {} \n".format(i+1, Title[i], Author[i], Journal[i], Url[i])
		if len(Title) == 0:
			dispatcher.utter_message(text="Sorry, I could not find this in our database")
		if len(Title) > 0:
			dispatcher.utter_message(text = response_string)
			#dispatcher.utter_message(text="Here is what I found: {}".format(Title))
		cur.close()
		con.close()
		return [AllSlotsReset()]
		if response_string:
			print("test")
		"""status = np.zeros(4, dtype = int)
		if(input_title):
			status[0] = 1
		if(input_author):
			status[1] = 1
		if(input_month):
			status[2] = 1
		if(input_year):
			status[3] = 1
		con = psycopg2.connect(host = 'localhost', database = 'dspace', user = 'postgres', password = 'p@ss2hell')
		cur = con.cursor()
		if(input_keyword):
			cur.execute("select title, author, month, year from dummy_data where month = '{}' or title = '{}' or author = '{}'".format(input_keyword,input_keyword,input_keyword))
			rows = cur.fetchall()
			if(rows):
				dispatcher.utter_message(text="Here is what I found: {}".format(rows))
			else:
				dispatcher.utter_message(text="Sorry, I could not find this in our database")
			return [AllSlotsReset()]
		else:
			if(status == ([0, 0, 0, 1])).all():
				cur.execute("select title, author, month, year from dummy_data where year = '{}'".format(input_year))
			if(status == ([0, 0, 1, 0])).all():
				cur.execute("select title, author, month, year from dummy_data where month = '{}'".format(input_month))
			if(status == ([0, 0, 1, 1])).all():
				cur.execute("select title, author, month, year from dummy_data where month = '{}' and year = '{}'".format(input_month,input_year))
			if(status == ([0, 1, 0, 0])).all():
				cur.execute("select title, author, month, year from dummy_data where author = '{}'".format(input_author))
			if(status == ([0, 1, 0, 1])).all():
				cur.execute("select title, author, month, year from dummy_data where author = '{}' and year = '{}'".format(input_author,input_year))
			if(status == ([0, 1, 1, 0])).all():
				cur.execute("select title, author, month, year from dummy_data where author = '{}' and month = '{}'".format(input_author,input_month))
			if(status == ([0, 1, 1, 1])).all():
				cur.execute("select title, author, month, year from dummy_data where author = '{}' and month = '{}' year = '{}'".format(input_author,input_month,input_year))
			if(status == ([1, 0, 0, 0])).all():
				cur.execute("select title, author, month, year from dummy_data where title = '{}'".format(input_title))
			if(status == ([1, 0, 0, 1])).all():
				cur.execute("select title, author, month, year from dummy_data where title = '{}' year = '{}'".format(input_title,input_year))
			if(status == ([1, 0, 1, 0])).all():
				cur.execute("select title, author, month, year from dummy_data where title = '{}' and month = '{}'".format(input_title,input_month))
			if(status == ([1, 0, 1, 1])).all():
				cur.execute("select title, author, month, year from dummy_data where title = '{}' and ,month = '{}' and year = '{}'".format(input_title,input_month,input_year))
			if(status == ([1, 1, 0, 0])).all():
				cur.execute("select title, author, month, year from dummy_data where title = '{}' and author = '{}'".format(input_title,input_author))
			if(status == ([1, 1, 0, 1])).all():
				cur.execute("select title, author, month, year from dummy_data where title = '{}' and author = '{}' and year = '{}'".format(input_title ,input_author,input_year))
			if(status == ([1, 1, 1, 0])).all():
				cur.execute("select title, author, month, year from dummy_data where title = '{}' and author = '{}' and month = '{}'".format(input_title ,input_author,input_month))
			if(status == ([1, 1, 1, 1])).all():
				cur.execute("select title, author, month, year from dummy_data where title = '{}' and author = '{}' and month = '{}' and year = '{}'".format(input_title ,input_author,input_month,input_year))
			try:
				rows = cur.fetchall()
				fetch_data = rows
				if(rows):
					dispatcher.utter_message(text="Here is what I found: {}".format(rows))
				else:
					dispatcher.utter_message(text="Sorry, I could not find this in our database")
			except:
				dispatcher.utter_message(text="Sorry, I could not find this in our database") 
				pass"""
