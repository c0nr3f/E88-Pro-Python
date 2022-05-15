from sched import scheduler
import socket
import time
from pynput import keyboard

command_address = ("192.168.4.153", 8090)
command = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
command.bind(("192.168.4.100", 19097))

# Common codes
# 6680808080000099 -> No input from user
# aa80800080008055 -> Heartbeat        

def on_press(key):
    try:
        # Start the motors with any hex input on byte number 4 froim 81 to ff
        if key.char == 's':
            command.sendto(bytes.fromhex('668080fa80000099'), command_address)
        
        # The arrow keys will result in an attribute error, catch that properly to continue
    except AttributeError:
        # The controller expects a joystick like input, so you cant simply raise the motor speed from hex 80 to hex ff, 
        # you must provide some kind of incrementing numbers. This will be redone, just for testing the functionality.
        
        if key == keyboard.Key.up:
            command.sendto(bytes.fromhex('6680808080000099'), command_address)
            command.sendto(bytes.fromhex('668080c580000099'), command_address)
            command.sendto(bytes.fromhex('668080ff87007899'), command_address)
            command.sendto(bytes.fromhex('668080c587007899'), command_address)
            command.sendto(bytes.fromhex('6680808080000099'), command_address)
            
        elif key == keyboard.Key.down:
            command.sendto(bytes.fromhex('6680808080000099'), command_address)
            command.sendto(bytes.fromhex('6680804885008599'), command_address)
            command.sendto(bytes.fromhex('6680800185008599'), command_address)
            command.sendto(bytes.fromhex('6680804885008599'), command_address)
            command.sendto(bytes.fromhex('6680808080000099'), command_address)
            
        elif key == keyboard.Key.esc:
            # This will end the keyboard listener
            return False
        else:
            pass

try:        
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
            
finally:
    print('closing socket')
    video.close()
    command.close()
