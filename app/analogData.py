#-*- coding:utf-8 -*-

import random
import time, threading
from app.models import SensorLog, SonModel, Sensor
from app import db
import datetime


SLAVEADDRESS = 1
SENSORSNUM =2

def read_registers(start, num):
    data = []
    rdata = [1,1,1,1,1,1,1,1,1,257,1,1,1,0,1,1,1,1,1]
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
                    slave = s.id
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
                                sensor = Sensor.query.filter_by(sonmodel_id=instrument[SLAVEADDRESS]).filter_by(position=i*2).first()
                                if sensor is not None:
                                    if str(value) in self.state:
                                        sensor.sensor_state = self.state[str(value)]
                                        if self.state[str(value)] != 'Normal':
                                            log = SensorLog(sensor_name=sensor.name, sensor_state=self.state[str(value)], sensor=sensor)
                                            db.session.add(log)
                                        db.session.add(sensor)
                                        db.session.commit()
                        else:       #模拟查询失败
                            sensors = Sensor.query.filter_by(sonmodel_id=instrument[SLAVEADDRESS]).all()
                            for s in sensors:
                                s.sensor_state ='unOpen'
                                db.session.add(s)
                                db.session.commit()
                time.sleep(self.sleeptimes)
            
    def stop(self):  
        self.thread_stop = True  




