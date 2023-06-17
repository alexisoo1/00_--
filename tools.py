import config
import os
import logging 
import sqlite3 as sl
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

def checkExistsDB(_db):
    logger.debug('checkExistsDB Start')
    from os.path import isfile, getsize
    if not isfile(_db):
        return False    
    return True

def checkExistsTable(_table):
    logger.debug('checkExistsTable Start')
    con = getDbConnection()
    cursor = con.cursor()
  			
    cursor.execute(" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}' ".format(_table))
    ret = True
    if cursor.fetchone()[0] == 1:
        ret = True
    else:
        ret = False
    
    con.commit()
    con.close()
    return ret

def deleteDB(_db):
    logger.info('deleteDB Start')
    from os.path import isfile, getsize

    if not isfile(_db):
        return
    os.remove(_db)

def createDB(_db, _recreateDB):
    logger.debug('createDB Start')
    print(logger.handlers)
    if checkExistsDB(_db):
        logger.info('DB exists')
        if _recreateDB:
            deleteDB(_db)
            logger.debug('try to delete')
        else:
            logger.info('DB {} already exists'.format(_db))
            return
    else:
        logger.info('Изначально не видим БД')
    if checkExistsDB(_db):
        logger.debug('Существует!!!!!!!!!!!!!!')
    else:
        logger.debug('Не существует')
    con = getDbConnection()
    con.close()

def createJournalTable(_recreateTable = False):
    logger.info('createJournalTable start')
    con = getDbConnection()
    success = True
    table = 'journal'
    if _recreateTable:
        try:
            con.execute('drop table if exists {}'.format(table))
            con.commit()      
        except sl.Error as error:
            logger.error("Ошибка при работе с SQLite: {}".format(error))
            success = False
        finally:  
            pass
    
    try:
        con.execute('''create table {}(
        id text not null default '', 
        unzipped integer default 0 not null,
        processed integer default 0 not null
        );'''.format(table))
        con.execute('Create Unique Index idxId{0} on {0} (id)'.format(table))
        con.commit()
    except sl.Error as error:
        logger.error("Ошибка при работе с SQLite: {}".format(error))
        success = False
        con.rollback()
    finally:  
        con.commit()
        con.close()

    return success

def createStatusTable(_recreateTable = False):
    logger.info('createStatusTable start')
    con = getDbConnection()
    success = True
    table = 'status'
    if _recreateTable:
        try:
            con.execute('drop table if exists {}'.format(table))
            con.commit()      
        except sl.Error as error:
            logger.error("Ошибка при работе с SQLite: {}".format(error))
            success = False
        finally:  
            pass
    
    try:
        con.execute('''create table {}(
        started integer default 0 not null, 
        unzipped integer default 0 not null,
        processed integer default 0 not null
        );'''.format(table))
        sql = f"insert into {table}(started,unzipped,processed) values(0,0,0)"
        con.execute(sql)
        con.commit()        
    except sl.Error as error:
        logger.error("Ошибка при работе с SQLite: {}".format(error))
        success = False
        con.rollback()
    finally:  
        con.commit()
        con.close()

    return success

def createOkvedTable(_recreateTable = False):
    logger.info('createOkvedTable start')
    con = getDbConnection()
    success = True
    table = 'okved'
    if _recreateTable:
        try:
            con.execute('drop table if exists {}'.format(table))
            con.commit()      
        except sl.Error as error:
            logger.error("Ошибка при работе с SQLite: {}".format(error))
            success = False
        finally:  
            pass
    
    try:
        con.execute('''create table {}(
        code text default '' not null, 
        parent_code text default '' not null,
        section text default '' not null,
        name text default '' not null,
        comment text default '' not null
        );'''.format(table))
        con.commit()        
    except sl.Error as error:
        logger.error("Ошибка при работе с SQLite: {}".format(error))
        success = False
        con.rollback()
    finally:  
        con.commit()
        con.close()

    return success

def createTelecom_companiesTable(_recreateTable = False):
    logger.info('createTelecom_companiesTable start')
    con = getDbConnection()
    success = True
    table = 'telecom_companies'
    if _recreateTable:
        try:
            con.execute('drop table if exists {}'.format(table))
            con.commit()      
        except sl.Error as error:
            logger.error("Ошибка при работе с SQLite: {}".format(error))
            success = False
        finally:  
            pass
    
    try:
        con.execute('''create table {}(
        ogrn text default '' not null, 
        inn text default '' not null,
        kpp text default '' not null,
        name text default '' not null,
        okved text default '' not null,
        full_name text default '' not null
        );'''.format(table))
        con.commit()        
    except sl.Error as error:
        logger.error("Ошибка при работе с SQLite: {}".format(error))
        success = False
        con.rollback()
    finally:  
        con.commit()
        con.close()

    return success

