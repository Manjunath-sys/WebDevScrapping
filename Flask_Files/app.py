from flask import Flask,jsonify,render_template

from pymongo import MongoClient



#database connection
client = MongoClient("mongodb://127.0.0.1:27017")

dbname = client.mydatabase

collection = dbname.webcollection1




app=Flask(__name__)


#Flask API
@app.route('/')

def display_data():

	#collection of data

	collection_list=collection.find()

	return render_template('result.html',todos=collection_list)



if __name__=='__main__':
	
	app.run(debug=True)