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
			query = "SELECT fl.device_id, u.name, fl.discharge_timestamp FROM firing_log fl JOIN users u ON u.device_id=fl.device_id"
			if device_id is not None:
				query += " WHERE device_id='"+str(device_id)+"'"
                        query += " ORDER BY discharge_timestamp DESC"
                        if self.DEBUG:
                                print query
                        try:
			        self.cursor.execute(query)
                        except db.Error, e:
                                print "Error %s:" % e.args[0]

		readCount = 0
		rows = []
		while readCount < set_size:
			row = self.cursor.fetchone()
			if row == None:
				break
                        rows.append({'device_id':row[0], 'name':row[1], 'discharge_timestamp':row[2]})
			readCount += 1
                return rows

        def registerDevice(self, device_id, name):
                try:
                        self.cursor.execute("INSERT OR IGNORE INTO users (device_id, name) VALUES (?, ?)",(device_id,name))
                        self.connection.commit()
                except db.Error, e:
                        print "Error %s:" % e.args[0]
                if self.DEBUG:
                        print "Device registered - "+str(device_id)+":"+str(name)


	def __del__(self):
		if self.connection:
			self.connection.close()
