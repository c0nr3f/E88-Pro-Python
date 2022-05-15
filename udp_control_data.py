from sched import scheduler
import socket
import time
from pynput import keyboard

command_address = ("192.168.4.153", 8090)
command = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
command.bind(("192.168.4.100", 19097))

# Insights into the used communication protocol:
# The controller basically sends bytes in hex format to the drone, telling it what to do. Meaning of the bytes:

# Byte 0: start byte, always 66
# Byte 1: controls the yaw (z axis rotation), from 01 (left) to fe (right)
# Byte 2: controls the pitch (y axis rotation), from 01 (left) to fe (right)
# Byte 3: controls the thrust (z axis translation), from 01 (left) to fe (right)
# Byte 4: controls the roll (x axis rotation), from 01 (left) to fe (right)
# Byte 5: (probably) no function, always 00
# Byte 6: not figured out yet
# Byte 7: end byte, always 99

# Some common codes
# 6680808080000099 -> No input from user, neutral position
# aa80800080008055 -> Heartbeat       

def on_press(key):
    try:
        # Start the motors with any hex input on byte number 4 froim 81 to ff
        if key.char == 's':
            command.sendto(bytes.fromhex('668080fa80000099'), command_address)
        
        # The arrow keys will result in an attribute error, catch that properly to continue
    except AttributeError:
        # The controller expects an analog input, so you cant simply raise the motor speed from hex 80 to hex ff, 
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
    command.close()
