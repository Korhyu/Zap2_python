# RPi
import time
import paho.mqtt.client as mqtt


#Cosas de la Rasp
import RPi.GPIO as GPIO 

# Configuration: 
LED_PIN        = 24 
BUTTON_PIN     = 23 

# Initialize GPIO for LED and button. 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False) 
GPIO.setup(LED_PIN, GPIO.OUT) 
GPIO.output(LED_PIN, GPIO.LOW) 
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 


# Setup callback functions that are called when MQTT events happen like 
# connecting to the server or receiving data from a subscribed feed. 
def on_connect(client, userdata, flags, rc): 
   print("Connected with result code " + str(rc)) 
   # Subscribing in on_connect() means that if we lose the connection and 
   # reconnect then subscriptions will be renewed. 
   client.subscribe("/led")
   client.subscribe("/test")
   client.subscribe("/medicion/tension")
   client.subscribe("/medicion/corriente") 

# The callback for when a PUBLISH message is received from the server. 
def on_message(client, userdata, msg): 
    print(msg.topic+" "+str( msg.payload)) 
    # Check if this is a message for the Pi LED. 
    if msg.topic == '/led': 
        # Look at the message data and perform the appropriate action. 
        if msg.payload == b'ON': 
            GPIO.output(LED_PIN, GPIO.HIGH) 
        elif msg.payload == b'OFF': 
            GPIO.output(LED_PIN, GPIO.LOW) 
        elif msg.payload == b'TOGGLE': 
            GPIO.output(LED_PIN, not GPIO.input(LED_PIN))

    if msg.topic == '/test':
        print('test') 

    if msg.topic == '/medicion/tension':
        print('Te falta hacer esto capo')


'''
# Main loop to listen for button presses. 
print('Script is running, press Ctrl-C to quit...') 
while True: 
   # Look for a change from high to low value on the button input to 
   # signal a button press. 
   button_first = GPIO.input(BUTTON_PIN) 
   time.sleep(0.02)  # Delay for about 20 milliseconds to debounce. 
   button_second = GPIO.input(BUTTON_PIN) 
   if button_first == GPIO.HIGH and button_second == GPIO.LOW: 
       print('Button pressed!') 
       # Send a toggle message to the ESP8266 LED topic. 
       client.publish('/leds/esp8266', 'TOGGLE')
'''