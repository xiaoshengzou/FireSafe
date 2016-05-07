#-*- coding: utf-8 -*-
import minimalmodbus
import time, threading
from app.models import SensorLog
from app import db
import datetime
from sqlalchemy import and_

minimalmodbus.BAUDRATE = 9600
minimalmodbus.TIMEOUT = 1
STARING_NUM = 512
WARNING_NUM = 257
NORMAL_NUM = 1


class WriteThread(threading.Thread):

    def __init__(self, app, sleeptimes, com, slave, sensornum):  
        threading.Thread.__init__(self)
        self.sleeptimes = sleeptimes
        self.com = com
        self.slave = slave
        self.sensornum = sensornum
        self.thread_stop = False
        self.app = app
          
    #Overwrite run() method, put what you want the thread do here 
    def run(self):
        with self.app.app_context(): 
            try:
                instrument = minimalmodbus.Instrument(self.com, self.slave)      
            except IOError:
                print 'com not open!'
            else:
                while not self.thread_stop:
                    try:
                        data = instrument.read_registers(0, self.sensornum)
                        for i, value in enumerate(data):
                            if value != 0:
                                datalog = SensorLog.query.filter_by(slave_id=self.slave).filter_by(position=i).first()
                                if datalog is not None:
                                    if value == STARING_NUM:
                                        datalog.sensor_state ='Staring'
                                        datalog.updata_time = datetime.datetime.now()
                                    elif value == WARNING_NUM:
                                        datalog.sensor_state ='Warning'
                                        datalog.updata_time = datetime.datetime.now()
                                    elif value == NORMAL_NUM:
                                        datalog.sensor_state ='Normal'
                                        datalog.updata_time = datetime.datetime.now()
                                    db.session.add(datalog)
                                else:
                                    datalog = SensorLog(slave_id=self.slave, position=i)
                                    db.session.add(datalog)
                                db.session.commit()           
                        time.sleep(self.sleeptimes)
                    except IOError:
                        datalog = SensorLog.query.filter_by(slave_id=self.slave).all()
                        for log in datalog:
                            log.sensor_state ='unOpen'
                            log.updata_time = datetime.datetime.now()
                            db.session.add(log)
                            db.session.commit()
                    except ValueError:
                        datalog = SensorLog.query.filter_by(slave_id=self.slave).all()
                        for log in datalog:
                            log.sensor_state ='Closed'
                            log.updata_time = datetime.datetime.now()
                            db.session.add(log) 
                            db.session.commit()
            finally:
                self.stop()
                print 'Thread close'  

            
    def stop(self):  
        self.thread_stop = True  



