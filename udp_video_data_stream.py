import cv2
import binascii
import socket
from io import BytesIO
from PIL import Image
import numpy as np

# IP and port of the drone, possible to sniff via wireshark of packet sniffer for the phone app
video_address = ("192.168.4.153", 8080)
video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Use your IP here
video.bind(("192.168.4.100", 19797))

# The message 'Bv' will start the video stream from the drone
video_start_message = str.encode('Bv')
video.sendto(video_start_message, video_address)

# The message 'By' will change the video input source
# switch_camera_message = str.encode('By')
# video.sendto(switch_camera_message, video_address)

def camera_feed():
    face_cascade = cv2.CascadeClassifier('C:/Users/sasko/AppData/Roaming/Python/Python39/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('C:/Users/sasko/AppData/Roaming/Python/Python39/site-packages/cv2/data/haarcascade_eye.xml')
    packet_data = bytearray()

    while(True):
        data, server = video.recvfrom(2048)
        
        # The first 8 bytes will crash the video output, since they are not part of the jpeg image. No use for them in this code yet. 
        data = data.hex()[16:]
        end_of_pic = data.find("ffffffd9")
      
        # Same for the last 5 bytes after the end of the jpeg
        if  end_of_pic > 0:   
            data = data[:end_of_pic + 8]

        data = binascii.a2b_hex(data)
        packet_data += bytearray(data)

        if end_of_pic > 0:
            
            # If the package is not complete, drop it
            if not packet_data.hex()[0:4] == "ffd8" and not packet_data.hex()[-8:] == "ffffffd9":
                packet_data = bytearray()
            else:
                # Initialize ByteIO buffer class
                buf = BytesIO(packet_data)
                
                # Try/catch is important here, since the image could still be defective. This leads to a crash in the program.
                try:
                    img = np.array(Image.open(buf))
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    # Haar Cascade to Detect Face and Eyes
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    for (x,y,w,h) in faces:
                        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                        roi_gray = gray[y:y+h, x:x+w]
                        roi_color = img[y:y+h, x:x+w]
                        eyes = eye_cascade.detectMultiScale(roi_gray)
                        for (ex,ey,ew,eh) in eyes:
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

                    cv2.imshow('Drone Camera', img)
                    
                except:
                    pass
                
                # Close the buffer and empty the package variable
                buf.close()
                packet_data = bytearray()

            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                break
            else:
                continue


try:
    camera_feed()

finally:
    video.close()
