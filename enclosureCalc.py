#!/usr/bin/python
# Filename: enclosureCalc.py
# Calculates inner volume of desired box and few additional parameters. 
# Uses International System of Units (SI)
# By Jukka Vatjus-Anttila

import math

class enclosureManager:
    '''With enclosureManager-class one can start speakerbox simulation which helps with common DIY loudspeaker
	mathematical operations. For now this class helps only subwoofer design but it extends rapidly. '''
    # Class variable. Names of all instances created from this class
    projects = []   
    
    def __init__(self,name):
        '''Defines all variables and sets them to zero.'''
        self.name = name          # Name of the "project"
        self.width = 0.0          # Box width (cm)
        self.height = 0.0         # Box height (cm)
        self.depth = 0.0          # Box depth (cm)
        self.material = 0.0       # Material thickness (cm)
        self.outerVolume = 0.0    # Volume of the whole box with materials: (litres)
        self.grossVolume = 0.0    # Volume of inner box: (litres)
        self.netVolume = 0.0      # Volume of inner box with port and driver substracted: (litres)
        self.tune = 0.0           # Tuning frequency of port (Hz)
        self.portDia = 0.0        # Diameter of port (cm)
        self.portLen = 0.0        # Length of port (cm)
        self.portVol = 0.0        # Volume of port (litres)
        self.driverVol = 0.0      # Volume of the driver (litres)
        self.iterFlag = True      # used with port iterator
        
        # Lets add this project to class variable as open project
        print 'Creating project {0}'.format(self.name)
        enclosureManager.projects.append(self.name)
 
    def printProjects():
        '''Static method which prints all instances made from this class.'''
        print 'Projects open: {0}'.format(enclosureManager.projects)
    printProjects = staticmethod(printProjects)   
    
    def __del__(self):
        '''Deletes instance of enclosureManager form project list'''
        print 'Deleting project {0}'.format(self.name)
        enclosureManager.projects.remove(self.name)
    
    def __updateVolume(self):
        '''Private method which encapsulates enclosure volume calculation formulas so everytime box volume needs updating this method is called.'''
        self.outerVolume = ( self.width * self.height * self.depth ) / 1000
        self.grossVolume = ((self.width - self.material*2) * (self.height - self.material*2) * (self.depth - self.material*2)) / 1000
        self.netVolume = self.grossVolume - self.portVol - self.driverVol
        
    def __portLengthIterator(self, portDia, tune):
        '''This is private method which iterates portLen and checks tuning frequency after port volume is subtracted from grossVolume.
        Increases portLen and subtracts new portVol from netVolume as long as tuning frequency hits desired value  '''
        while self.tune != tune:
            if self.iterFlag:   # First iteration is done with grossVolume.
                self.portLen = (22700 * self.portDia**2) / (tune**2 * self.grossVolume) - 0.79 * self.portDia
                self.iterFlag = False
            else:   # Then we re-check with netVolume as many times as needed.
                self.portLen = (22700 * self.portDia**2) / (tune**2 * self.netVolume) - 0.79 * self.portDia
            self.portVol = (math.pi*(portDia/2)**2 * self.portLen) / 1000
            self.netVolume = self.grossVolume - self.portVol - self.driverVol
            self.tune = ( (22700*self.portDia**2)/(self.netVolume*(self.portLen+0.79*self.portDia)) )**0.5
            # Sometimes iterator cant match self.tune and tune because 32bit floating points are inaccurate. 
            # Therefore this if stops iteration loop when self.tune is close enough.
            if tune < (self.tune + 0.01) and tune > (self.tune - 0.01):
                self.tune = tune
                break
        iterFlag = True
        print 'Calculating port...' # This is here for fun, lol
  
    def printAll(self):
        '''Prints all calculated parameters.'''
        print '''{0} has these attributes: 
        outerVolume: \t\t{1:.2f} litres
        grossVolume: \t\t{2:.2f} litres
        netVolume: \t\t{3:.2f} litres
        material thickness: \t{4:.1f} mm
        Port tuning: \t\t{5:.1f} Hz
        Port length: \t\t{6:.1f} cm
        Port volume: \t\t{7:.1f} litres'''.format(self.name, self.outerVolume, self.grossVolume, self.netVolume, self.material*10, self.tune, self.portLen, self.portVol)

    def setDimensions(self, width, height, depth, material):
        '''Sets parameters of the enclosure and calculates box volume.'''
        self.width = width
        self.height = height
        self.depth = depth
        self.material = material
        
        self.__updateVolume()
    
    def setPort(self, portDia, tune):
        '''Sets port diameter and calculates netVolume of the box, portVol and portLen.'''
        self.portDia = portDia
        self.__portLengthIterator(portDia, tune)
        
    def setDriver(self, driver):
        '''Sets the driver volume and recalculates box tuning if necessary.'''
        self.driverVol = driver
        
        if self.portDia != 0:
            tune = self.tune
            self.tune = 0
            self.__portLengthIterator(self.portDia, tune)
        
    def setWidth(self, width):
        '''Sets enclosure width parameter and updates volume.'''
        self.width = width
        self.__updateVolume()
        
        if self.portDia != 0:
            tune = self.tune
            self.tune = 0
            self.__portLengthIterator(self.portDia, tune)
    
    def setHeight(self, height):
        '''Sets enclosure height parameter and updates volume.'''
        self.height = height
        self.__updateVolume()
        
        if self.portDia != 0:
            tune = self.tune
            self.tune = 0
            self.__portLengthIterator(self.portDia, tune)
    
    def setDepth(self, depth):
        '''Sets enclosure depth parameter and updates volume.'''
        self.depth = depth
        self.__updateVolume()
        
        if self.portDia != 0:
            tune = self.tune
            self.tune = 0
            self.__portLengthIterator(self.portDia, tune)   
            
    def setMaterial(self, material):
        '''Sets enclosure material thickness parameter and updates volume.'''
        self.material = material
        self.__updateVolume()

    def getOuterVolume(self):
        return self.outerVolume
        
    def getGrossVolume(self):
        return self.grossVolume
        
    def getNetVolume(self):
        return self.netVolume
        
    def getPortLength(self):
        return self.portLen
        
    def getPortDia(self):
        return self.portDia
        
    def getPortVol(self):
        return self.portVol
        
    def getTune(self):
        return self.tune
        
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getDepth(self):
        return self.depth
    
