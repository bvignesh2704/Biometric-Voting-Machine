import cv2 as cv
import tkinter as tk
from PIL import Image
from PIL import ImageTk


class CameraCapture:
    def __init__(self, tkWindow, column=0, row=0, videosource=0):
        self.cap = cv.VideoCapture(videosource)
        self.tkWindow = tkWindow
        self.camera_ready = True
        self.width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)

        self.tkCanvas = tk.Canvas(tkWindow, width=self.width, height=self.height)
        self.tkCanvas.grid(row=row, column=column)

        if not self.cap.isOpened():
            self.camera_ready = False
            raise Exception("Camera cannot be opened")

        self.update()

    def update(self):
        ret, frame = self.cap.read()

        if ret:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.tkCanvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        if self.camera_ready:
            self.tkWindow.after(15, self.update)

    def stop(self):
        self.camera_ready = False
        self.cap.release()

    def __del__(self):
        self.stop()

    def snap(self, filename):
        ret, frame = self.cap.read()
        cv.imwrite(filename, frame)
        return ret
