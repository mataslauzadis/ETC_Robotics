import cv2
#!/home/codetc/anaconda3/bin/python


import io
import socket
import struct
import time
import pickle
import time


fps = 20
previous = 0 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.0.0.83', 8485))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 320);
cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    elapsed_time = time.time() - previous
    ret, frame = cam.read()
    
    if elapsed_time > 1./fps:
        previous = time.time()
        result, frame = cv2.imencode('.jpg', frame, encode_param)  

        data = pickle.dumps(frame, 0)
        size = len(data)

        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1

cam.release()