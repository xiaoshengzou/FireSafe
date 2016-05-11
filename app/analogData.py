#-*- coding:utf-8 -*-

import random
import time, threading
from app.models import SensorLog, SonModel
from app import db
import datetime


SLAVEADDRESS = 1
SENSORSNUM =2

def read_registers(start, num):
    data = []
    rdata = [1,1,1,1,0,1,257,512,1,1,1,1,1,1,1,1]
    rNum = num - start
    if rNum < 0:
        return data
    else:
        i = 0
        while i < rNum:
            data.append(random.choice(rdata))
            data.append(0)
            i = i + 2
        a = []
        a.append(data)
        #a.append([])
        return random.choice(a)


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
                del self.instruments[:]     #empty instruments
                smodel = SonModel.query.all()   #acquire all sonmodel
                for s in smodel:
                    smodeldata = []
                    com = s.getComNumber()
                    slave = s.slaveaddress
                    sensorsNum = s.sensorsNumber * 2
                    instrument = random.choice(['open'])    #模拟打开端口
                    smodeldata.append(instrument)
                    smodeldata.append(slave)
                    smodeldata.append(sensorsNum)
                    self.instruments.append(smodeldata)     #acquire all sonmodel's instrusment
                    
                for instrument in self.instruments:
                    if instrument[0] == 'open':
                        datas = read_registers(0,instrument[SENSORSNUM])
                        if datas:      #模拟查询成功
                            pop_zero_data = datas[::2]
                            for i, value in enumerate(pop_zero_data):
                                datalog = SensorLog.query.filter_by(slave_id=instrument[SLAVEADDRESS]).filter_by(position=i*2).first()
                                if datalog is not None:
                                    if str(value) in self.state:
                                        datalog.sensor_state = self.state[str(value)]
                                        datalog.updata_time = datetime.datetime.now()
                                        db.session.add(datalog)
                                        db.session.commit()
                        else:       #模拟查询失败
                            datalog = SensorLog.query.filter_by(slave_id=instrument[SLAVEADDRESS]).all()
                            for log in datalog:
                                log.sensor_state ='unOpen'
                                log.updata_time = datetime.datetime.now()
                                db.session.add(log)
                                db.session.commit()
                time.sleep(self.sleeptimes)
            
    def stop(self):  
        self.thread_stop = True  




