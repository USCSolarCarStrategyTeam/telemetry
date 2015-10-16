__author__ = 'paul'

class HazardZone:
    SAFE=0
    WARN=1
    DANGER=2
    def __init__(self, safe=[0,40], warn=[40,60],danger=60):
        self.saferange=safe
        self.warnrange=warn
        self.dangerrange=danger

    def currentRange(self, val):
        '''
        gives the (int) hazard level that something is in given the current value.
        :param val:
        :return:
        '''
        return self.WARN#testing for now, do some logic to figure this out.

class SuperDataModel:
    """
    base class for all the data that we'll be displaying.
    """
    histsize = 100
    def __init__(self, name):
        self.name = name
        self.unit = 'Undef'
        self.val = 0
        self.hist = [0]*self.histsize
        self.hazardranges = HazardZone()
        return
    def getCurrentVal(self):
        return self.val

    def getUnit(self):
        return self.unit

    def getHistory(self):
        return self.hist;

    def getHazardRanges(self):
        return self.hazardranges;

    def getQuickText(self):
        return str(self.val) + ' ' + str(self.unit)

class TemperatureModel(SuperDataModel):
    """
    temperature readings
    """
    def __init__(self, name):
        SuperDataModel.__init__(self,name)
        #lol unicode is hard in python...
        self.unit = u"\u00B0C".encode('utf-8')
        return

class VoltageModel(SuperDataModel):
    def __init__(self, name):
        SuperDataModel.__init__(self,name)
        #lol unicode is hard in python...
        self.unit = "V".encode('utf-8')
        return

class AmpModel(SuperDataModel):
    def __init__(self, name):
        SuperDataModel.__init__(self,name)
        #lol unicode is hard in python...
        self.unit = "A".encode('utf-8')
        return

class RpmModel(SuperDataModel):
    def __init__(self, name):
        SuperDataModel.__init__(self,name)
        #lol unicode is hard in python...
        self.unit = "rpm".encode('utf-8')
        return

"""
    This class simply contains a list of all the data models we'll be looking for in the program.
"""
import socket   #for sockets
import sys  #for exit
from kivy.clock import Clock

# this is a static variable. if you wanted a object specific variable, you declare it in init
datalist = {'cabintemp': TemperatureModel('Cabin Temp'),
            'motortemp': TemperatureModel('Motor Temp'),
            'batterytemp': TemperatureModel('Battery Temp'),
            'motor rpm': RpmModel('Motor RPM'),
            'solar volt': VoltageModel('Solar Volt'),
            'bat volt': VoltageModel('Battery Volt')
            #etc
            };


class SolarCarConnector:
    HOST="";
    PORT=0;
    REMOTE_IP=''
    """
    this class handles actually making a connection to the simulation or the actual microprocessor.
    """

    def __init__(self, addr):
        REMOTE_IP = addr
        try:
            #create an AF_INET, STREAM socket (TCP)
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            sys.exit()
        print 'Socket Created'
        pass

    def startserv(self, pollrate):
        '''
        should attempt to establish a connection and spin off a new thread that polls every @pollrate seconds(or something)
        do whatever necessary for when you can't establish a connection...
        do NOT block the main UI with this.
        :return:
        '''
        ''' Should we try to connect given a host name
        try:
            REMOTE_IP = socket.gethostbyname(HOST)
        except socket.gaierror:
            #could not resolve
            print 'Hostname could not be resolved. Exiting'
            sys.exit()
        print 'Ip address of ' + HOST + ' is ' + REMOTE_IP
        '''
        try:
            self.s.connect((self.REMOTE_IP,self.PORT))
        except socket.error:
            print('Connection cannot be established. Exiting')
            sys.exit()
        print 'Socket Connected to'+self.HOST+'on ip '+self.REMOTE_IP
        Clock.schedule_interval(self.poll,pollrate)
        pass


    def poll(self):
        '''
        grr...idk how to make private methods...
        should be called within thread in startserv
        :return:
        '''
        message=self.s.recv(4096)
        parsedmessage=self.parsemessage(self,message)
        #do something to parsedmessage
        #self.updateModel(self)
        pass

    def parsemessage(self, msg):
        '''
        code to parse message
        '''
        str1=[]
        str1=msg.split(',')
        for item in str1:
            print item
        return

    def updateModel(self):
        '''

        :return:
        '''
        pass