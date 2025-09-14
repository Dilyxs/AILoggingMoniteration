from PostGresConn import PostgresSQL
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from huggingface_hub import whoami
from GemmaAPI import GemmaAPI
from DbManagement import CustomLoggerManagement

class Test:
	def __init__(self):
		self.db = PostgresSQL()
		self.api = GemmaAPI()
		self.DbManager = CustomLoggerManagement(self.db)
		self.Loggers = []
		self.data = self.FetchLoggers()  # this returns a list with each row of db as a Map
		self.AddLastLoggedLines()
		self.AddLinesToView()
		self.model = self.ReturnModel()
		self.DetectIfErrorLarge()
		self.AiOpinion()
		self.UpdateDB()

	def ReturnModel(self, model_name="byviz/bylastic_classification_logs"):
		tokenizer = AutoTokenizer.from_pretrained(model_name)
		model = AutoModelForSequenceClassification.from_pretrained(model_name)
		classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
		return classifier

	def FetchLoggers(self):
		return self.db.FetchAllData("loggerpath")

	def FindLastLoggedLine(self, LoggerID):
		data = self.db.FetchSpecificData("lastloggedlines", condition="loggerid = %s", params=[LoggerID])
		return None if not data else data

	def AddLastLoggedLines(self):
		for data in self.data:
			localdata = self.FindLastLoggedLine(data['id'])
			localdata = 0 if not localdata else localdata['lastline']
			data['lastloggedline'] = localdata

	def LoggedLinesToInspect(self, filepath, lastloggedline):
		with open(filepath, "r") as f:
			lines = f.readlines()
		ValidLines = lines[:] if not lastloggedline else lines[lastloggedline + 1:]
		NewLastLoggedLines = len(lines) - 1
		return ValidLines, NewLastLoggedLines

	def AddLinesToView(self):
		for data in self.data:
			data['NewLastLoggedLines'] = self.LoggedLinesToInspect(
				data['loggerpath'], data['lastloggedline']
			)[1]
			data['LinesToView'] = self.LoggedLinesToInspect(
				data['loggerpath'], data['lastloggedline']
			)[0]

	def DetectIfError(self, filepath, model, StartLine=0, Endline=None):
		ErrorDetected = False
		with open(filepath, 'r') as f:
			lines = f.readlines()
		TrainingLines = lines[StartLine:] if not Endline else lines[StartLine:Endline]
		for line in TrainingLines:
			result = (model(line))[0]
			if result['label'] == "ERROR" and result['score'] >= 0.7:
				ErrorDetected = True
				break
		return ErrorDetected

	def DetectIfErrorLarge(self):
		for data in self.data:
			data['ErrorPresent'] = self.DetectIfError(
				data['loggerpath'], self.model, data['lastloggedline'], None
			)

	def AiOpinion(self):
		for data in self.data:
			AIsolution = None
			if data['ErrorPresent']:
				filepath = data['filepath']
				txt_filepath = self.api.convert_log_to_txt(data['loggerpath'])
				data = self.api.file_to_text(txt_filepath)
				response = self.api.SendMessage(data, filepath=filepath)
				AIsolution = response
			data['AIsolution'] = AIsolution

	def UpdateDB(self):
		for data in self.data:
			self.DbManager.UpdateLoggerLine(data['lastloggedline'], data['id'])
			self.DbManager.AddData(data['lastloggedline'], data['ErrorPresent'], data['AIsolution'])


a = Test()
for i in a.data:
	print(i['loggerpath'])
	print(i['ErrorPresent'])
