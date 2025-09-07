from PostGresConn import  PostgresSQL

class Test:
    def __init__(self):
        self.db = PostgresSQL()
        self.Loggers = []
        self.data = self.FetchLoggers();#this return a list with each row of db as a Map;
        self.AddLastLoggedLines()
        self.AddLinesToView()

    def FetchLoggers(self):
        return self.db.FetchAllData("loggerpath")
    
    def FindLastLoggedLine(self, LoggerID):
        data = self.db.FetchSpecificData("lastloggedlines",condition="loggerid = %s", params=[LoggerID])

        return None if not data else data
    
    def AddLastLoggedLines(self):
        for data in self.data:
            data['lastloggedline'] = self.FindLastLoggedLine(data['id'])['lastline'] if self.FindLastLoggedLine(data['id']) else None

    def LoggedLinesToInspect(self,filepath,lastloggedline):
        with open(filepath, "r") as f:
            lines = f.readlines()

        ValidLines = lines[:] if not lastloggedline else lines[lastloggedline+1:]
        NewLastLoggedLines = len(lines)-1

        return ValidLines, NewLastLoggedLines
    
    def AddLinesToView(self):
        for data in self.data:
            data['NewLastLoggedLines'] = self.LoggedLinesToInspect(data['loggerpath'], data['lastloggedline'])[1]
            
            data['LinesToView'] = self.LoggedLinesToInspect(data['loggerpath'], data['lastloggedline'])[0]


a = Test()
print(a.data)
