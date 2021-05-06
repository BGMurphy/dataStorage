import connexion

from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import and_
from base import Base
from surgery import Surgery
from xray import Xray
import datetime
import yaml
import pykafka
from pykafka import KafkaClient
from threading import Thread
import json
import logging
import logging.config
from flask_cors import CORS, cross_origin

try:
    with open('/config/app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())
except:
    with open('app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

DB_ENGINE = 'mysql+pymysql://' + app_config['datastore']['user'] + ':' + app_config['datastore']['password'] + '@' + \
    app_config['datastore']['hostname'] + ':' + app_config['datastore']['port'] + '/' + app_config['datastore']['db']
DB_ENGINE = create_engine(DB_ENGINE)
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def book_surgery(reading):

    session = DB_SESSION()

    surgery = Surgery(reading['patient_id'],
                       reading['bookingDate'],
                       reading['surgeryDate'])

    session.add(surgery)

    session.commit()
    session.close()

    return NoContent, 201

def get_surgery(startDate, endDate):
    """ Get surgery info from the data store """

    results_list = []

    session = DB_SESSION()

    results = []

    results = session.query(Surgery).filter(and_(Surgery.date_created >= datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S"), Surgery.date_created <= datetime.datetime.strptime(endDate,"%Y-%m-%dT%H:%M:%S")))

    for result in results:
        results_list.append(result.to_dict())
        print(result.to_dict())

    session.close()

    return results_list, 200

def xRay_report(reading):

    session = DB_SESSION()

    xray = Xray(reading['patient_id'],
                reading['result'],
                reading['timestamp'])

    session.add(xray)

    session.commit()
    session.close()

    return NoContent, 201

def get_xRay(startDate, endDate):
    """ Get surgery info from the data store """

    results_list = []

    session = DB_SESSION()

    results = []

    results = session.query(Xray).filter(and_(Xray.date_created >= datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S"), Xray.date_created <= datetime.datetime.strptime(endDate,"%Y-%m-%dT%H:%M:%S")))

    for result in results:
        results_list.append(result.to_dict())
        print(result.to_dict())

    session.close()

    return results_list, 200

def add_to_db(type, payload):
    session = DB_SESSION()

    if (type == "xrayInfo"):
        xray = Xray(payload['patient_id'],
                    payload['result'],
                    payload['timestamp'])

        session.add(xray)
        session.commit()
        session.close()
    elif (type == "surgeryInfo"):
        surgery = Surgery(payload['patient_id'],
                          payload['bookingDate'],
                          payload['surgeryDate'])

        session.add(surgery)
        session.commit()
        session.close()

def process_messages():
    kafka = app_config['datastore']['server'] + ':' + app_config['datastore']['kafkaPort']
    client = KafkaClient(hosts=kafka)
    topic = client.topics[app_config['datastore']['topic']]
    consumer = topic.get_simple_consumer(auto_commit_enable=True, auto_commit_interval_ms=1000, consumer_group="storageApi")
    logger = logging.getLogger('basicLogger')

    for msg in consumer:
        msg_str = msg.value
        data = msg_str.decode('utf-8')
        msg = json.loads(data)
        add_to_db(msg["type"], msg["payload"])
        logger.info(msg["payload"])


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)