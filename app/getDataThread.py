#-*- coding: utf-8 -*-
import minimalmodbus
import time, threading
from app.models import SensorLog, SonModel
from app import db
import datetime
# from sqlalchemy import and_

minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL=True
minimalmodbus.BAUDRATE = 9600
minimalmodbus.TIMEOUT = 3

SLAVEADDRESS = 1
SENSORSNUM =2

class WriteThread(threading.Thread):

    def __init__(self, app, sleeptimes):  
        threading.Thread.__init__(self)
        self.sleeptimes = sleeptimes
        self.thread_stop = False
        self.app = app
        self.instruments = []
        self.state = {'512':'Staring', '257':'Warning', '1':'Normal'}
    #Overwrite run() method, put what you want the thread do here 
    def run(self):
        with self.app.app_context(): 
            try:
                smodel = SonModel.query.all()
                for s in smodel:
                    smodeldata = []
                    com = s.getComNumber()
                    slave = s.slaveaddress
                    sensorsNum = s.sensorsNumber * 2
                    instrument = minimalmodbus.Instrument(com, slave)
                    instrument.debug = True 
                    smodeldata.append(instrument)
                    smodeldata.append(slave)
                    smodeldata.append(sensorsNum)
                    self.instruments.append(smodeldata)    
                    print s.name ,':', instrument
            except IOError:
                print 'com not open!'
            else:
                while not self.thread_stop:
                    for instrument in self.instruments:
                        try:
                            data = instrument[0].read_registers(0, instrument[SENSORSNUM])
                            #print debug log
                            print instrument[SLAVEADDRESS],':', data

                            for i, value in enumerate(data):
                                if value != 0:
                                    datalog = SensorLog.query.filter_by(slave_id=instrument[SLAVEADDRESS]).filter_by(position=i).first()
                                    if datalog is not None:
                                        if str(value) in self.state:
                                            datalog.sensor_state = self.state[str(value)]
                                            datalog.updata_time = datetime.datetime.now()
                                            db.session.add(datalog)
                                            db.session.commit()
                            time.sleep(self.sleeptimes)                  
                        except IOError,e:
                            print 'IoError'
                            datalog = SensorLog.query.filter_by(slave_id=instrument[SLAVEADDRESS]).all()
                            for log in datalog:
                                log.sensor_state ='unOpen'
                                log.updata_time = datetime.datetime.now()
                                db.session.add(log)
                                db.session.commit()
                        except ValueError,e:
                            print 'ValueError'
                            # datalog = SensorLog.query.filter_by(slave_id=instrument[SLAVEADDRESS]).all()
                            # for log in datalog:
                            #     log.sensor_state ='Closed'
                            #     log.updata_time = datetime.datetime.now()
                            #     db.session.add(log) 
                            #     db.session.commit()
            
    def stop(self):  
        self.thread_stop = True  



