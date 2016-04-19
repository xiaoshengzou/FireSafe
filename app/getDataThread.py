#-*- coding: utf-8 -*-
import minimalmodbus
import time, threading
from app.models import SensorLog
from app import db
import datetime


minimalmodbus.BAUDRATE = 9600
minimalmodbus.TIMEOUT = 1
STARING_NUM = 512
WARNING_NUM = 257
NORMAL_NUM = 1


class WriteThread(threading.Thread):

    def __init__(self, app, sleeptimes):  
        threading.Thread.__init__(self)
        self.sleeptimes = sleeptimes
        # self.com = com
        # self.slave = slave
        # self.sensornum = sensornum
        self.thread_stop = False
        self.app = app
          
    #Overwrite run() method, put what you want the thread do here 
    def run(self):
        with self.app.app_context(): 
            try:
                instrument = minimalmodbus.Instrument('COM3', 1)      
            except IOError:
                print 'com not open!'
            else:
                while not self.thread_stop:
                    try:
                        data = instrument.read_registers(0, 6)
                        for i, value in enumerate(data):
                            if value != 0:
                                datalog = SensorLog.query.filter_by(position=i).first()
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
                                    datalog = SensorLog(slave_id=1 , position=i)
                                    db.session.add(datalog)
                        db.session.commit()
                        time.sleep(self.sleeptimes)
                    except IOError:
                        print 'sensor close'
                    except ValueError:
                        print 'no value'  
            finally:
                self.stop()
                print 'Thread close'  

            
    def stop(self):  
        self.thread_stop = True  



