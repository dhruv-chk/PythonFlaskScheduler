import atexit

from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

from utils import utils
from utils.logger import init_logger
from payment import payments
from scheduler.payment_scheduler import Scheduler

app = Flask(__name__)
CORS(app)

api = Api(app)

# Health check resource
class HealthCheck(Resource):
    def get(self):
        return {'status': 'Scheduler API is up and running'}

# Notification job scheduling resource
class Subscribe(Resource):
    def post(self):
        logger = init_logger()
        try:
            print("Ssubscription API Invoked.")
            scheduler_request = request.get_json(force=True)
            
            tenant = request.headers.get('Xtenant-ID')
            logger.info(tenant)

            Scheduler.schedule_payments("customer_id", tenant)
            
            return {
                'message': 'Successfully subscribed',
            }, 200
        except Exception as e:
            logger.exception("Error: " + str(e))
            return {
                'message': 'Payment subscription failed',
            }, 500

api.add_resource(HealthCheck, '/healthCheck')
api.add_resource(Subscribe, '/schedule')

def shutdown_cleanup():
    Scheduler.stop()
    utils.get_engine().dispose()

def start_app():
    print('Starting app...')
    
    # Handle shutdown for scheduler
    atexit.register(shutdown_cleanup)

    Scheduler.initialize()
    Scheduler.start()
    
    print('Started app [OK]')
    
    return app
