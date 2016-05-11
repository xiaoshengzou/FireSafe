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
        self.state = {'512':'Staring', '257':'Warning', '1':'Normal', '0':'Closed'}
    #Overwrite run() method, put what you want the thread do here 
    def run(self):
        with self.app.app_context():
            while not self.thread_stop:
                try:
                    del self.instruments[:]     #empty instruments
                    smodel = SonModel.query.all()   #acquire all sonmodel
                    for s in smodel:
                        smodeldata = []
                        com = s.getComNumber()
                        slave = s.slaveaddress
                        sensorsNum = s.sensorsNumber * 2
                        instrument = minimalmodbus.Instrument(com, slave)
                        smodeldata.append(instrument)
                        smodeldata.append(slave)
                        smodeldata.append(sensorsNum)
                        self.instruments.append(smodeldata)     #acquire all sonmodel's instrusment
                except IOError:
                    print 'com not open!'
                else:
                    try:
                        for instrument in self.instruments:
                            datas = instrument[0].read_registers(0, instrument[SENSORSNUM])
                            pop_zero_data = datas[::2]
                            for i, value in enumerate(pop_zero_data):
                                datalog = SensorLog.query.filter_by(slave_id=instrument[SLAVEADDRESS]).filter_by(position=i*2).first()
                                if datalog is not None:
                                    if str(value) in self.state:
                                        datalog.sensor_state = self.state[str(value)]
                                        datalog.updata_time = datetime.datetime.now()
                                        db.session.add(datalog)
                                        db.session.commit()
                    except IOError:
                        datalog = SensorLog.query.filter_by(slave_id=instrument[SLAVEADDRESS]).all()
                        for log in datalog:
                            log.sensor_state ='unOpen'
                            log.updata_time = datetime.datetime.now()
                            db.session.add(log)
                            db.session.commit()
                    except ValueError:
                        datalog = SensorLog.query.filter_by(slave_id=instrument[SLAVEADDRESS]).all()
                        for log in datalog:
                            log.sensor_state ='Error'
                            log.updata_time = datetime.datetime.now()
                            db.session.add(log) 
                            db.session.commit() 
                finally:
                    time.sleep(self.sleeptimes)
            
    def stop(self):  
        self.thread_stop = True  



