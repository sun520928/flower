# -*- coding: utf-8 -*-
import json
import datetime
import logging

from flask import Flask, request
import logging

import pymysql
pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy


DB_USER = 'flower'
DB_PWD  = 'flower'
DB_NAME = 'flower'
DB_IP   = 'localhost'
DB_PORT = '3306'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://%s:%s@%s/%s'% (DB_USER, DB_PWD, DB_IP, DB_NAME)
db = SQLAlchemy(app)

class Identification(db.Model):
	index = db.Column(db.Integer, primary_key=True, autoincrement=True)
	id = db.Column(db.Integer)
	description = db.Column(db.String(512))

	def __init__(self, id, desp):
		self.id = id
		self.description = desp

	def __repr__(self):
		return '<Identification %d>' % self.id


class Air(db.Model):
	index = db.Column(db.Integer, primary_key=True, autoincrement=True)
	humidity = db.Column(db.Float)
	fahrenheit = db.Column(db.Float)
	celsius = db.Column(db.Float)
	update_date = db.Column(db.DateTime, default=datetime.datetime.now)
	remarks = db.Column(db.String(256))

	def __init__(self, humidity, fahrenheit, celsius, remarks=''):
		self.humidity = humidity
		self.fahrenheit = fahrenheit
		self.celsius = celsius
		self.remarks = remarks

	def __repr__(self):
		return '<Air %f %f %f %s>' % (self.humidity, self.fahrenheit, self.celsius, self.remarks)

@app.route('/')
def hello_flower():
	return 'Hello Flower!'

@app.route("/air", methods=["POST", "GET"])
def air():
	ret = {}
	ret['code'] = 200
	ret['success'] = True
	ret['result'] = {}

	data_str = request.get_data()
	app.logger.debug('recv POST: %s' % data_str)
	data = json.loads(data_str.decode("utf-8"))

	if request.method =='POST':
		humidity = float(data.get('humidity'))
		fahrenheit = float(data.get('fahrenheit'))
		celsius = float(data.get('celsius'))

		if humidity and fahrenheit and celsius:
			air = Air(humidity, fahrenheit, celsius)
			db.session.add(air)
			db.session.commit()
			app.logger.info('add air success.Air=%s' % air)
	else:
		begin_date = data.get("begin")
		end_date = data.get("end")
		page_num = data.get("pagenum")
		page_size = data.get("pagesize")

		end_datetime = datetime.datetime.combine(end_date, datetime.time(24, 0, 0))
		begin_datetime = datetime.datetime.combine(begin_date, datetime.time(0, 0, 0))

		aires = Air.query.filter(update_date < end_datetime, update_date > begin_datetime).all()

	return json.dumps(ret, ensure_ascii=False)
 


def db_init():
	db.create_all()

if __name__ == "__main__":
	db_init()
	app.run(debug=True)
