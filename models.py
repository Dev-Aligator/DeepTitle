## Define your models here

class Line:
    def __init__(self, id:int, startTime: str, endTime:str, scripts:str):
        self.id = id
        self.startTime = startTime
        self.endTime = endTime
        self.scripts = scripts

    def __str__(self):
        return f"{self.id}\n{self.startTime} --> {self.endTime}\n{self.scripts}"

