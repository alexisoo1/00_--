import config
import json
import sqlite3 as sl
import logging 
import timeit
import pandas as pd
import zipfile
from pathlib import Path
import csv
logger = logging.getLogger(__name__)
logger.setLevel(config.loggerLevel)
lfm = logging.Formatter(config.formatter)
lsh = logging.StreamHandler()
lsh.setLevel(config.streamLogHandlerLevel)
lsh.setFormatter(lfm)
lfh = logging.FileHandler(filename='log.log', mode='w')
lfh.setFormatter(lfm)
lfh.setLevel(config.fileLogHandlerLevel)
logger.addHandler(lsh)
logger.addHandler(lfh)

def getDbConnection():
    con = sl.connect(database=config.dbName, timeout=config.timeOut, detect_types=sl.PARSE_DECLTYPES | sl.PARSE_COLNAMES)
    return con

okvedZip = Path(config.dataDir, config.okvedZip)
with zipfile.ZipFile(file=okvedZip, mode='r') as zipObj:
    files = zipObj.namelist()
    print(files)
    zipObj.extract(config.okved, path=config.dataDir)

okved = Path(config.dataDir, config.okved)
# with open(okved, 'r', encoding='UTF-8') as csv_file: #encoding='UTF-8'  Windows-1251
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     for row in csv_reader:
#         print(row)

with open(okved, 'r', encoding='UTF-8') as f:
    df = pd.read_json(f)
    df.info()
    #data = json.load(f)
    #print(type(data))

con = getDbConnection()
cursor = con.cursor()
try:
    df.to_sql('okved', con)
except Exception as err:
    print(f"{err}")
finally:
    con.close()