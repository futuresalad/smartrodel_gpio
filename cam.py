import time
import numpy as np
import cv2 as cv
import threading

class Cam():
    def __init__(self):

        self.cap = cv.VideoCapture(0)
        self.width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.fourcc = cv.VideoWriter_fourcc('m','p','4','v')
        
        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()

    def record(self, duration_s):
        
        # waiting for all threads to be set up
        writer = cv.VideoWriter('messdaten/video/success.mp4', self.fourcc, 20, (self.width, self.height))
        print("Camera started")
        now = time.time() 
        #successful_frame = np.zeros(self.height, self.width) 
        while (time.time() <= (now + duration_s)):
            
            success, frame = self.cap.read() 

            if success:
                successful_frame = frame
                writer.write(successful_frame)

            if not success:
                writer.write(successful_frame)

            if cv.waitKey(1) == ord('q'):
                break
    
        self.cap.release()
        writer.release()


if __name__ == "__main__":
    duration = 20
    cam = Cam()

    cam_thread = threading.Thread(target=cam.record, args=(duration,))
    cam_thread.start()

    print("Waiting record to finish")
    cam_thread.join()

    print("Recording finished")
