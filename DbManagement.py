from datetime import dateime,timezone

class CustomLoggerManagement:
	def __init__(self, db):
		self.db = db


	def UpdateLastLoggedLine(self, lastLoggedLine, loggerid):
		self.db.DeleteSpecificData("lastloggedines", {'loggerid':loggerid})
		#build the data
		data = {'loggerid':loggerid,
				'lastline':lastLoggedLine,
				'lastupdated': datetime.now(timezone.utc)}

		res = db.InsertData("lastloggedlines", data)
		return res

	def AddData(self, loggerid,ErrorPresent,  message = None):
		data = {'loggerid':loggerid,
				'importance':True if ErrorPresent else False,
				'message':message,
				'messagetime':datetime.now(timezone.utc)}
		
		
		res = self.db.InsertData('loggerdetails', data)
		return res
	
		