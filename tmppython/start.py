#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# =============================================================================
__author__ = "Matthias Morath"
__copyright__ = "Copyright 2021"
__credits__ = ["Matthias Morath"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Matthias Morath"
__email__ = "matthias.morath@liebherr.com"
__status__ = "Development"
# =============================================================================
import sys
import json
import socket
import os
import logging
import logging.config
import logging.handlers

from datetime import datetime
from time import sleep

MICROSERVICE_NAME = None
MICROSERVICE_VERSION = None
NTP_HOST_01 = None
NTP_HOST_02 = None
MQTT_HOST = None
MQTT_PORT = None
MQTT_ENABLE_SSL = None
MQTT_USER = None
MQTT_PASSWORD = None
UPDATE_RATE = None
LOGGING_LEVEL = None
OPCUA_HOST = None
OPCUA_PORT = None
OPCUA_USER = None
OPCUA_PASSWORD = None
OPCUA_MANUFACTURER = None
OPCUA_NAME = None
OPCUA_DESCRIPTIPON = None
OPCUA_ORDER_NO = None

#dictionary of eviroment variables inlcuding type
envVariables = {
        'MICROSERVICE_NAME' :"%s",
        'MICROSERVICE_VERSION' :"%s",
        'NTP_HOST_01' :"%s",
        'NTP_HOST_02' :"%s",
        'OPCUA_HOST' :"%s",
        'OPCUA_PORT' :"%i",
        'OPCUA_USER' :"%s",
        'OPCUA_PASSWORD' :"%s",
        'OPCUA_MANUFACTURER' :"%s",
        'OPCUA_NAME' :"%s",
        'OPCUA_DESCRIPTIPON' :"%s",
        'OPCUA_ORDER_NO' :"%s",
        'MQTT_HOST' :"%s",
        'MQTT_PORT' :"%i",
        'MQTT_ENABLE_SSL' :"%r",
        'MQTT_USER' :"%s",
        'MQTT_PASSWORD' :"%s",
        'UPDATE_RATE': "%i",
        'LOGGING_LEVEL': "%s",
}

# set default update rate
UPDATE_RATE = 1000

# set up the logger based on the logger.conf file.
logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)

#Logging Level Mapping
logger_level_mapping = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

init = False

###############################################################################################################
# Envrioment settings helper function
###############################################################################################################
def importEnviromentVariables(envDict):
    """ import enviroment variables ...enviroment variables are set in docker-compose file """
    logging.debug('Reading enviroment variables from host')
    #create a list which will hold missing env variables
    missingEnvVars = []
    #for each item in the envDict dictionary
    for item in envDict:
        #read the envrioment variable from operating system
        val = os.environ.get(item)
        #Check if read input is type none or has no entry
        if (val == None) or (val == ""):
            #if value is missing append it to the list
            missingEnvVars.append(item)
        else:
            #check for type string
            if (envDict[item] == "%s"):
                exec(("%s = "+envDict[item]) % (item, val),globals())
            #check for type int    
            elif(envDict[item] == "%i"):
                exec(("%s = "+envDict[item]) % (item, int(val)),globals())
            #check for type boolean
            elif(envDict[item] == "%r"):
                exec(("%s = "+envDict[item]) % (item, json.loads(val.lower())),globals())
            else:
                #unknown type not defined...
                logging.debug(f"Unknown type")
    #if list holds missing variables
    if len(missingEnvVars) > 0:
        #return false and the list of missing variables
        return False, missingEnvVars
    else:
        #return true with emtpy list
        return True, []

def setLoggingLevel():
    global logging, logger, logger_level_mapping
    #Check if logglevel is set...if not set to debug
    if LOGGING_LEVEL is None:
        #set default log level 
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('Loglevel not set through enviroment variable, set loglevel to debug')
    else:
        #set log level set through enviroment variable
        logging.getLogger().setLevel(logger_level_mapping[LOGGING_LEVEL])

def setUpdateRate():
    global UPDATE_RATE
    UPDATE_RATE = UPDATE_RATE / 1000
###############################################################################################################
# Helper functions host
###############################################################################################################
def get_microServiceInfo():
    """ get all enviroment infos"""
    logging.info('Micro Service started')
    logging.info(f"CONTAINER_NAME: {socket.gethostname()} CONTAINER_IP: {socket.gethostbyname(socket.gethostname())}")
    logging.info('Service startet with the following enviroment variables')
    if MICROSERVICE_NAME is not None: logging.info(f"MICROSERVICE_NAME:{MICROSERVICE_NAME} MICROSERVICE_VERSION:{MICROSERVICE_VERSION}")
    logging.info(f"LOGGING_LEVEL: %s",logger.level)
###############################################################################################################
# Helper functions device dependent
###############################################################################################################

###############################################################################################################
# MAIN
###############################################################################################################
if __name__ == "__main__":
    #import the variables
    importEnviromentVariables(envVariables)
    #set logging level
    setLoggingLevel()
    #set update rate
    setUpdateRate()
    #provide information about the micro service and its set enviroment variables...
    #note the envrioment variables are set in the docker-compose file
    get_microServiceInfo()
    #create flag_connected which shows if connected or not

    #first loop statement in case called several times
    if init==False:
        #add here code for init process
        pass
    else:
        init=True

    try:
        while True:
            sleep(UPDATE_RATE)
            try:
                #add her functions to be executed in the loop 
                pass
            #break loop if keyboard interrupt...        
            except KeyboardInterrupt:
                try:
                    #handle disconnects
                    pass
                except:
                    sys.exit()         
    finally:
        pass
   