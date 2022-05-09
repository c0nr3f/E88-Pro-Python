import cv2
import binascii
import socket
from io import BytesIO
from PIL import Image
import numpy as np

video_address = ("192.168.4.153", 8080)
video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video.bind(("192.168.4.100", 19797))

video_start_message = str.encode('Bv')
video.sendto(video_start_message, video_address)
packet_data = bytearray()

try:
    while(True):
        data, server = video.recvfrom(2048)
        data = data.hex()[16:]
        end_of_pic = data.find("ffffffd9")
      
        if  end_of_pic > 0:   
            data = data[:end_of_pic + 8]

        data = binascii.a2b_hex(data)
        packet_data += bytearray(data)

        if end_of_pic > 0:
            if not packet_data.hex()[0:4] == "ffd8" and not packet_data.hex()[-8:] == "ffffffd9":
                packet_data = bytearray()
            else:
                buf = BytesIO(packet_data)
                
                try:
                    img = np.array(Image.open(buf))
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    cv2.imshow('Drone Camera', img)
                except:
                    pass

                buf.close()
                packet_data = bytearray()

            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                break
            else:
                continue

finally:
    video.close()