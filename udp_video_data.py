import cv2
import binascii
import socket
from io import BytesIO
from PIL import Image
from matplotlib.pyplot import gray
import numpy as np
import utils

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

# net = cv2.dnn.readNet('yolov3-wider_16000.weights', 'yolov3-face.cfg')
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
# ln = net.getLayerNames()

def camera_feed():
    face_cascade = cv2.CascadeClassifier('C:/Users/sasko/AppData/Roaming/Python/Python39/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('C:/Users/sasko/AppData/Roaming/Python/Python39/site-packages/cv2/data/haarcascade_eye.xml')
    # feature_params = dict(maxCorners = 300, qualityLevel = 0.2, minDistance = 2, blockSize = 7)
    # lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    # color = np.random.randint(0, 255, (100, 3))
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
                    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    # Haar Cascade to Detect Face and Eyes
                    # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    # for (x,y,w,h) in faces:
                    #     img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    #     roi_gray = gray[y:y+h, x:x+w]
                    #     roi_color = img[y:y+h, x:x+w]
                    #     eyes = eye_cascade.detectMultiScale(roi_gray)
                    #     for (ex,ey,ew,eh) in eyes:
                    #         cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

                    # Different blur
                    # img = cv2.GaussianBlur(img,(3,3), 10)
                    # img = cv2.medianBlur(img,5)
                    # img = cv2.bilateralFilter(img, 19, 75, 75)

                    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    # Hugh Circles
                    # circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,75,
                    #            param1=40,param2=87, minRadius=1,maxRadius=400)
    
                    # if circles is not None:
                    #     circles = np.uint16(np.around(circles))
                    #     for i in circles[0,:]:
                    #         # draw the outer circle
                    #         cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
                    #         # draw the center of the circle
                    #         cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
                    
                    # Yolov3 not working
                    # blob = cv2.dnn.blobFromImage(img, 1 / 255, (640, 480), [0, 0, 0], 1, crop=False)
                    # net.setInput(blob)
                    # outs = net.forward(ln)
                    # faces = utils.post_process(img, outs, utils.CONF_THRESHOLD, utils.NMS_THRESHOLD)
                    # info = [
                    #     ('number of faces detected', '{}'.format(len(faces)))
                    # ]

                    # for (i, (txt, val)) in enumerate(info):
                    #     text = '{}: {}'.format(txt, val)
                    #     cv2.putText(img, text, (10, (i * 20) + 20),
                    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, utils.COLOR_RED, 2)


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