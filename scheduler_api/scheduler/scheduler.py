from enum import Enum

from datetime import date, datetime, timedelta
from threading import current_thread
from pandas.tseries.offsets import Day, Hour, MonthBegin
from pytz import utc, timezone
import requests
import pandas
import uuid
import json

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from sqlalchemy.engine.base import Engine

# from payment import payments
from utils import utils, logger
from db_layer.db_access import db_connection, get_donation_config, set_scheduled_payments, get_email, set_payment_details
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from service.email import send_email


class Scheduler:
    scheduler: BackgroundScheduler = None
    log = logger.init_logger()

    @staticmethod
    def initialize():
        jobstores = {
            'default': SQLAlchemyJobStore(url=utils.get_config_value('JOB_STORE_DB_CONN_STR'), tablename=utils.get_config_value('JOB_TABLE'))
        }
        executors = {
            'default': ThreadPoolExecutor(20)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 100000,  # Set this to a really high number
            'misfire_grace_time': 15 * 60  # 15mins
        }

        est = timezone('US/Eastern')
        Scheduler.scheduler = BackgroundScheduler(
            jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

    @staticmethod
    def start():
        if Scheduler.scheduler == None:
            print(
                'Scheduler not initialized, call initialize() method in this module first')
        else:
            Scheduler.scheduler.start()
            print('Scheduler started')

    @staticmethod
    def stop():
        if Scheduler.scheduler == None:
            print(
                'Scheduler not initialized, call initialize() method in this module first')
        elif not Scheduler.scheduler.running:
            print('Scheduler already shutdown')
        else:
            print('Shutting down scheduler')
            Scheduler.scheduler.shutdown()

    @staticmethod
    def schedule_emails(recipient: str, subject: str, body: str):
        end_date = datetime.utcnow() + timedelta(hours=2)
        job = Scheduler.scheduler.add_job(
            send_email, 'interval', args=[recipient, subject, body], hours=1, start_date=datetime.utcnow(), end_date=end_date)
        Scheduler.log.info(job)

    @staticmethod
    def payments(customer_id: str, tenant: str):
        try:
            
            end_date = datetime.utcnow() + timedelta(days=720)
            # One time future date.
            job = Scheduler.scheduler.add_job(
                Scheduler.make_payment, 'date', run_date=datetime.now, args=[])
            Scheduler.log.info(job)
                
            # Annual.

            job = Scheduler.scheduler.add_job(
                Scheduler.make_payment, 'interval', [], days=365, start_date=datetime.now, end_date=end_date)
            Scheduler.log.info(job)

            # Monthly.

            job = Scheduler.scheduler.add_job(
                Scheduler.make_payment, 'interval', [], days=30, start_date=datetime.now,  end_date=end_date)
            Scheduler.log.info(job)

            # Bi-monthly.
            job = Scheduler.scheduler.add_job(
                Scheduler.make_payment, 'interval', [], days=60, start_date=datetime.now,  end_date=end_date)
            Scheduler.log.info(job)
        except Exception as e:
            Scheduler.log.exception("Error: " +str(e))
            raise e


        except Exception as e:
            Scheduler.log.exception("Error while making payment: ", e)
            return -1


    @staticmethod
    def make_payment(customer_id, amount, percentage, tenant, account, payment_type):
        try:
            pass
        except:
            print("Error")
