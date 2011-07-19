from enclosureCalc import enclosureManager
from enclosureCalc import driverManager

# Test program starts here
print '''************************************************
Welcome to test program. This program testdrives enclosureManager class by setting parameters.
You can modify it yourself to test different scenarios although there are not much to test yet.
************************************************'''
newProject = enclosureManager("testi")
enclosureManager.printProjects()
newProject.setDimensions(51.0,62.0,61.0,2.2)
print 'Setting port: 15.24 cm diameter and 20Hz tune' 
newProject.setPort(15.24, 20)
newProject.printAll()
print 'setting driver'
newProject.setDriver(5)
newProject.printAll()
print 'Setting height: 65cm'
newProject.setHeight(65.0)
newProject.printAll()
del newProject
shiva = driverManager("testi")
del shiva
# program ends here
