from flask import Flask, flash, url_for, render_template, request, redirect, make_response, Response, jsonify
from pymongo import MongoClient
import datetime
logging = True

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['pattern_network']
patterns = db['patterns']

app = Flask(__name__)

app.secret_key = "L\x97\xb9^\xa4\x18\x91\xd5\xb4\xae\x87\x92&\xf32\xdf\xbfC\xf7S~\xdb)g"

@app.route('/log/<user_id>/<pattern>')
def payment(user_id,pattern):
    details = {'timestamp':datetime.datetime.now()}
    details.update({'user_id':user_id})
    details.update({'pattern':pattern})
    patterns.insert_one(details)
    print details
    return "LOGGED"

@app.route('/db_check')
def db_check():
    return jsonify(logging=logging)

@app.route('/recent')
def recent():
    recent = list(patterns.find({'timestamp':{'$gt':datetime.datetime.now() - datetime.timedelta(seconds=3)}},{'_id':0}))
    if len(recent) > 0:
        return jsonify(result=recent[0])
    else:
        return jsonify(result=None)

if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True)
