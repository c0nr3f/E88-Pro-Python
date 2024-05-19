import socket
from pynput import keyboard

command_address = ("192.168.4.153", 8090)
command = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
command.bind(("192.168.4.100", 19097))

#     command.sendto(bytes.fromhex('6680808080000099'), command_address) # No input from user
#     command.sendto(bytes.fromhex('aa80800080008055'), command_address) # Heartbeat        

def on_press(key):
    try:
        if key.char == 's':
            command.sendto(bytes.fromhex('668080fa80000099'), command_address)

        elif key.char == '+':
            command.sendto(bytes.fromhex('6680808080000099'), command_address)
            command.sendto(bytes.fromhex('668080c580008099'), command_address)
            command.sendto(bytes.fromhex('668080ff80008099'), command_address)
            command.sendto(bytes.fromhex('668080ff80008099'), command_address)

        elif key.char == '-':
            command.sendto(bytes.fromhex('6680808080000099'), command_address)
            command.sendto(bytes.fromhex('6680804880008099'), command_address)
            command.sendto(bytes.fromhex('6680800180008099'), command_address)
        
    except AttributeError:
        if key == keyboard.Key.up:
            command.sendto(bytes.fromhex('6680808080000099'), command_address)
            command.sendto(bytes.fromhex('668080c580000099'), command_address)
            command.sendto(bytes.fromhex('668080ff87007f99'), command_address)

        elif key == keyboard.Key.down:
            command.sendto(bytes.fromhex('6680808080000099'), command_address)
            command.sendto(bytes.fromhex('6680804885008599'), command_address)
            command.sendto(bytes.fromhex('6680800185008599'), command_address)

        elif key == keyboard.Key.esc:
            return False


def on_release(key):
    try:
        if key.char == 's':
            command.sendto(bytes.fromhex('6680808080000099'), command_address)

        elif key.char == '+':
            command.sendto(bytes.fromhex('668080ff80008099'), command_address)
            command.sendto(bytes.fromhex('668080c580008099'), command_address)
            command.sendto(bytes.fromhex('6680808080000099'), command_address)
        
        elif key.char == '-':
            command.sendto(bytes.fromhex('6680800180008099'), command_address)
            command.sendto(bytes.fromhex('6680804880008099'), command_address)
            command.sendto(bytes.fromhex('6680808080000099'), command_address)

    except AttributeError:
        if key == keyboard.Key.up:
            command.sendto(bytes.fromhex('668080ff87007899'), command_address)
            command.sendto(bytes.fromhex('668080c587007899'), command_address)
            command.sendto(bytes.fromhex('6680808080000099'), command_address)

        elif key == keyboard.Key.down:
            command.sendto(bytes.fromhex('6680800185008599'), command_address)
            command.sendto(bytes.fromhex('6680804885008599'), command_address)
            command.sendto(bytes.fromhex('6680808080000099'), command_address)


try:        
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
            
finally:
    print('closing socket')
    command.close()