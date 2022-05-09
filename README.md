# E88-Pro-Python
Repository with python scripts to gather data and control an E88 pro drone. It doesn't matter wich camera version you have, since it's always the same resolution (640x480p).

# Installation
```
pip install opencv-python socket Pillow numpy
```

# Scripts
## udp_video_data.py
This script will process the mjpeg-like stream and modifys it until it can be displayed in opencv. Be aware to use the correct ip address of your pc for testing in line 10. The port you use doesn't matter.
```
video.bind(("192.168.4.100", 19797))
```

# License
Licensed under MIT License. 
