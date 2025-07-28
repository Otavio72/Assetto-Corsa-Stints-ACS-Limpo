# AC App Template by Hunter Vaners
# ------------------------------
#
# Don't forget to rename assettocorsa\apps\python\Template_Assetto_Corsa_App
#           by assettocorsa\apps\python\[Your_App_Name_Without_Spaces]
#  and
# the file Template_Assetto_Corsa_App.py
#           by Your_App_Name_Without_Spaces.py
#
# ------------------------------
import time
import sys
from socket import *
import ac
import acsys
from third_party.sim_info import *

host = "192.168.15.77"
port = 1111

client_DATA = socket(AF_INET, SOCK_STREAM)
client_DATA.connect((host,port))

appName = "ACS"
width, height = 300 , 300 # width and height of the app's window

simInfo = SimInfo()

lapcount = 0 

l_gas = 0
gas = 0

l_brake = 0
brake = 0

l_steer = 0
steer = 0

l_gear = 0
gear = 0



def acMain(ac_version):

 
    global appWindow , l_gas, l_brake, l_steer, l_gear # <- you'll need to update your window in other functions.

    appWindow = ac.newApp(appName)
    ac.setTitle(appWindow, appName)
    ac.setSize(appWindow, width, height)
    ac.setBackgroundOpacity(appWindow,0)

    
    
    l_gas = ac.addLabel(appWindow, "Gas: 0")
    ac.setPosition(l_gas, 2, 30)

    l_brake = ac.addLabel(appWindow, "Brake: 0")
    ac.setPosition(l_brake, 4, 50)

    l_steer = ac.addLabel(appWindow, "Steer: 0")
    ac.setPosition(l_steer, 5, 70)



    ac.log("Helloo after session")

    ac.addRenderCallback(appWindow, appGL) # -> 

    return appName




def appGL(deltaT):#-------------------------------- OpenGL UPDATE
    """
    This is where you redraw your openGL graphics
    if you need to use them .
    """
    #pass # -> Delete this line if you do something here !



def convert_laptime(Laptime_non_converted):
    minutes = Laptime_non_converted // 60000
    seconds = Laptime_non_converted % 60000 // 1000
    milliseconds = Laptime_non_converted % 1000
    return "{:02}:{:02}:{:03}".format(minutes,seconds,milliseconds)



#socket
def send_data():
  global lapcount, gas, lapTime, lastlap, car_name, track_name

  lap_time_and_number = "{}||{}".format(lapcount,lastlap)

  Name_car = "Car:{}".format(car_name)
  Name_track = "Track:{}".format(track_name)

  
  client_DATA.send(lap_time_and_number.encode() + b"\n" + "Code=02".encode() + b"\n" + Name_car.encode() + b"\n" + Name_track.encode())

    


#socket
def acShutdown():
   client_DATA.send("Code=01".encode() + b"\n")
   client_DATA.close()


def acUpdate(deltaT):#-------------------------------- AC UPDATE
   global lapcount, l_gas, gas, l_brake, brake, l_steer, steer, l_gear, gear, lapTime, lastlap, car_name, track_name

   Gas = ac.getCarState(0, acsys.CS.Gas)
   gas = Gas
   ac.setText(l_gas, "Gas: {}".format(gas))

   
   Brake = ac.getCarState(0, acsys.CS.Brake)
   brake = Brake
   ac.setText(l_brake, "Brake: {}".format(brake))   


   Steer = ac.getCarState(0, acsys.CS.Steer)
   steer = "{:.2f}".format(Steer)
   ac.setText(l_steer, "Steer: {}°".format(steer))


   Laptime_non_converted = ac.getCarState(0, acsys.CS.LapTime)
   Laptime_non_converted = int(Laptime_non_converted)
   Laptime_converted = convert_laptime(Laptime_non_converted)
   lapTime = Laptime_converted


   laps_Last_non_converted = ac.getCarState(0, acsys.CS.LastLap)
   laps_Last_non_converted = int(laps_Last_non_converted)

   lastlap = laps_Last_non_converted
  
   
   laps = ac.getCarState(0, acsys.CS.LapCount)
   if laps > lapcount:
    lapcount = laps
    

    car = ac.getCarName(0)
    car_name = car
    

    track = ac.getTrackName(0)
    track_name = track
    

    send_data()


    

    




    




