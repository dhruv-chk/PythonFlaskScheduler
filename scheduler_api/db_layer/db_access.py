from sqlalchemy import create_engine
# from config import dbendpoint, dbname, dbuser, dbpassword
from datetime import datetime
import pymysql
import pandas as pd
from utils import utils, logger

sqlEngine = None
log = logger.init_logger()

def db_connection(tenant):
    global sqlEngine
    try:
        dbendpoint = utils.get_config_value('JOB_STORE_DB_CONN_STR')
        index = dbendpoint.rfind('/')
        dbendpoint = 'mysql+pymysql' + dbendpoint[5:index+1]

        sqlEngine = create_engine(
            dbendpoint + '{0}'.format(get_db_name(tenant)), pool_recycle=1800)

        dbConnection = sqlEngine.connect()

        return dbConnection
    except Exception as e:
        log.exception("Error occured:" + str(e))
        raise e


def get_db_name(tenant):
    db_name = {'1': 'db1',
               '2': 'db2'}
    return db_name[tenant]


def get_donation_config(dbConn, id, tenant):
    dbname = get_db_name(tenant)
    try:
        query = "SELECT * FROM {1}.random_table WHERE id='{0}'".format(id, dbname)
        frame = pd.read_sql(query, dbConn)
            
        return frame
    except Exception as e:
        log.exception("Error occured:" + str(e))
        raise e


def set_scheduled_payments(dbConn, id, amount, percentage, exp, tenant):
    dbname = get_db_name(tenant)
    global sqlEngine
    try:
        
        query = "INSERT INTO "+dbname+".`random_table`(`id`,`amount`,`percentage`,`exp`) VALUES (%s,%s,%s,%s)"
        params= (id, int(amount), int(percentage), exp)
        sqlEngine.execute(query,params)
    except Exception as e:
        log.exception("Error occured:" + str(e))
        raise e
