import time
import numpy as np
import cv2 as cv
import threading

class Cam():
    def __init__(self):

        self.cap = cv.VideoCapture(0)
        width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.writer = cv.VideoWriter('testvid.mp4', fourcc, 30, (width, height))

        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()

    def record(self, duration_s):
        duration_ns = duration_s * 1_000_000_000
        now = time.time_ns() 
        
        while (time.time_ns() < (now + duration_ns)):

            success, frame = self.cap.read() 
            self.writer.write(frame)

            if cv.waitKey(1) == ord('q'):
                break
    
        self.cap.release()
        self.writer.release()


if __name__ == "__main__":

    cam = Cam()

    cam_thread = threading.Thread(target=cam.record, args=(20,))
    cam_thread.start()
    print("Waiting record to finish")
    cam_thread.join()
    print("Recording finished")
