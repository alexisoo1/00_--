import logging
dbName = 'hw1.db'
loggerLevel = logging.ERROR
fileLogHandlerLevel = logging.DEBUG
streamLogHandlerLevel = logging.ERROR
formatter = '%(asctime)s - %(lineno)s - %(name)s - %(levelname)s - %(message)s'
timeOut = 5
exportDir = './xls/'
backUpDir = './backup/'
backUpExt = '_backUp.sql'
mode = 'dev'
okved = 'okved_2.json'
okvedZip = 'okved_2.json.zip'
dataDir = 'data'