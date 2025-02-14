import azure.functions as func
import logging
import json
import random
import os


app = func.FunctionApp()

# @app.service_bus_queue_trigger(arg_name="azservicebus", queue_name=content_feed_queue,
#                                connection="infomonai_SERVICEBUS") 
# def feed_triggered(azservicebus: func.ServiceBusMessage):
#     logging.info('feed_triggered triggered')
#     pass
