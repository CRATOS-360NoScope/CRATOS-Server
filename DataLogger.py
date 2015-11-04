import sqlite3 as db

class DataLogger:

	connection = None
	cursor = None
	DEBUG = False

	def __init__(self, debug=False):
		self.DEBUG = debug
		try:
			self.connection = db.connect('cratos_data.db')
			self.cursor = self.connection.cursor()
		except db.Error, e:
			print "Error %s:" % e.args[0]

	def writeLog(self, device_id):
		try:
			self.cursor.execute("INSERT INTO firing_log (device_id) VALUES (?)",(device_id,))
			self.connection.commit()
		except db.Error, e:
			print "Error %s:" % e.args[0]
		if self.DEBUG:
			print "Log written - "+str(device_id)

	def readLog(self, new_read=True, set_size=25, device_id=None):
		if self.DEBUG:
			print "Reading log, new_read=%s set_size=%s device_id=%s" % (str(new_read), str(set_size), str(device_id))
		if new_read:
			query = "SELECT device_id, discharge_timestamp FROM firing_log";
			if device_id is not None:
				query += " WHERE device_id='"+str(device_id)+"'"
			self.cursor.execute(query)

		readCount = 0
		rows = []
		while readCount < set_size:
			row = self.cursor.fetchone()
			if row == None:
				break
			rows.append({'device_id':row[0], 'discharge_timestamp':row[1]})
			readCount += 1
                return rows

	def __del__(self):
		if self.connection:
			self.connection.close()
