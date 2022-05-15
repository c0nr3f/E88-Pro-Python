from sched import scheduler
import socket
import time
import threading
from pynput import keyboard

video_address = ("192.168.4.153", 8080)
video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video.bind(("192.168.4.100", 19797))

command_address = ("192.168.4.153", 8090)
command = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
command.bind(("192.168.4.100", 19097))

video_start_message = str.encode('Bv')
time.sleep(1)

commands = {
    '.......U' : bytes.fromhex('aa80800080008055'),
    'f.......' : bytes.fromhex('6680808080000099'),
    'f.....z.' : bytes.fromhex('668080ff85007a99'),
    'f.....t.' : bytes.fromhex('668080ff8b007499'),
    'f.....[.' : bytes.fromhex('668080db80005b99'),
    'f...x...' : bytes.fromhex('668080ff78008799'),
    'f...v...' : bytes.fromhex('668080ff76008999'),
    'f...t...' : bytes.fromhex('668080ff74008b99'),
    'f...r...' : bytes.fromhex('668080fe72008c99'),
    'f...s...' : bytes.fromhex('668080ff73008c99'),
    'f...u...' : bytes.fromhex('668080ff75008a99'),
    'f..(....' : bytes.fromhex('668080288000a899'),
    
    'f...v.v.' : bytes.fromhex('6680800076007699'),
    'f...w.w.' : bytes.fromhex('6680800077007799'),
    'f...x.x.' : bytes.fromhex('6680800078007899'),
    'f...y.y.' : bytes.fromhex('6680800079007999'),

    'f.....y.' : bytes.fromhex('668080ff86007999'),
    'f.....o.' : bytes.fromhex('668080fe91006f99'),
    'f.....q.' : bytes.fromhex('668080fe8f007199'),
    'f.....s.' : bytes.fromhex('668080ff8c007399'),
    'f.....u.' : bytes.fromhex('668080ff8a007599'),
    'f.....M.' : bytes.fromhex('668080cd80004d99'),
    'f.....].' : bytes.fromhex('668080dd80005d99'),
    'f.....}.' : bytes.fromhex('668080ff82007d99'),
    'f.....|.' : bytes.fromhex('668080ff83007c99'),
    'f.....{.' : bytes.fromhex('668080ff84007b99'),
    'f.....R.' : bytes.fromhex('668080d98b005299'),
    'f.....6.' : bytes.fromhex('668080be88003699'),
    'f..Sx.+.' : bytes.fromhex('6680805378002b99')
}

#     command.sendto(bytes.fromhex('6680808080000099'), command_address) # No input from user
#     command.sendto(bytes.fromhex('aa80800080008055'), command_address) # Heartbeat        

def on_press(key):
    try:
        if key.char == 's':
            command.sendto(bytes.fromhex('668080fa80000099'), command_address)
    except AttributeError:
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