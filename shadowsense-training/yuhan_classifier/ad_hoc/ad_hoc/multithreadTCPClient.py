
# Import socket module 
import socket 
import time
import json

_json_object = {
    "id" : int(time.time()),
    "cmd" : "TextToSpeechCommand", #Command name
    "priority" : 1, ##, Priority, type int
    "text" : "Labhansh testing", #Text to be spoken, in string of lenght not more than 50 characters
    "receivingPort" : 12345
}
  
_send_setspeed_obejct = {
	"id" : int(time.time()),
	"cmd" : "SetSpeedCommand", #Command name
	"priority" : 1,#, Priority, type int
	"leftSpeed" : 1500, ## Left speed value, type int
	"rightSpeed" : 1500, ## Right speed value, type int
    "receivingPort" : 12345
}

_send_project_image = {
    "id" : int(time.time()),
    "cmd" : "ProcessProjectImageCommand", #Command name
    "priority" : 2, ##, Priority, type int
    "imageFileName" : "b.png", #Image file existing on the rover "$HOME/Images" folder, to be projected or processed
    "processImage" : False, #true/false, Flag to process image or not
    "projectImage" : False #true/false Flag to project image or not
    # "receivingPort" : 12345,
}

  
def sendObject(message):
    # local host IP '127.0.0.1' 
    host = '10.148.8.230'
  
    # Define the port on which you want to connect 
    port = 65432
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
  
    # connect to server on local computer 
    s.connect((host,port)) 
  
    s.send(json.dumps(message).encode() )
    s.close()


def Main(): 
    
    
    # message you send to server 
    message = "labhnash testing"
    while True:   
  
        # message sent to server 
        sendObject(_send_project_image)
        time.sleep(0.2)

  
if __name__ == '__main__': 
    Main() 

