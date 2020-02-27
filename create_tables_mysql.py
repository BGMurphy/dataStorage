import mysql.connector
import yaml

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

db_conn = mysql.connector.connect(host=app_config['datastore']['hostname'], user=app_config['datastore']['user'], password=app_config['datastore']['password'], database=app_config['datastore']['db'])

db_cursor = db_conn.cursor()

db_cursor.execute('''
    CREATE TABLE xRay_info
    (id INT NOT NULL AUTO_INCREMENT,
    patient_id VARCHAR(250) NOT NULL,
    result VARCHAR(250) NOT NULL,
    timestamp VARCHAR(100) NOT NULL,
    date_created VARCHAR(100) NOT NULL,
    CONSTRAINT xRay_info_pk PRIMARY KEY (id))
    ''')

db_cursor.execute('''
    CREATE TABLE surgery_info
    (id INT NOT NULL AUTO_INCREMENT,
    patient_id VARCHAR(250) NOT NULL,
    bookingDate VARCHAR(100) NOT NULL,
    surgeryDate VARCHAR(100) NOT NULL,
    date_created VARCHAR(100) NOT NULL,
    CONSTRAINT surgery_info_pk PRIMARY KEY (id))
    ''')

db_conn.commit()
db_conn.close()






