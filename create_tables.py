import sqlite3
import mysql.connector

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE surgery_info
          (id INTEGER PRIMARY KEY ASC,
           patient_id VARCHAR(250) NOT NULL,
           bookingDate VARCHAR(100) NOT NULL,
           surgeryDate VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE xRay_info
          (id INTEGER PRIMARY KEY ASC,
           patient_id VARCHAR(250) NOT NULL,
           result VARCHAR(250) NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
