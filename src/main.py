import tkinter as tk
import utilities as utl
import cv2
from PIL import Image, ImageTk


class WebcamApp:
    def __init__(self, window) -> None:
        self.window = window
        self.window.title("QR Registration")
        
        # OpenCV setup
        camera_id = 1
        self.qcd = cv2.QRCodeDetector()
        self.video_capture = cv2.VideoCapture(camera_id)
        self.currentImage = None
        
        # Display
        root.state('zoomed')
        self.canvas = tk.Canvas(window, width=screen_width, height=screen_height)
        self.canvas.pack()
        
        self.update_Webcam()
        
    def update_Webcam(self):
        returnValue, frame = self.video_capture.read()
        frame = cv2.resize(frame, (screen_width//2, screen_height//2))
        
        # If using front came, uncomment
        # frame = cv2.flip(frame, 1)
        if returnValue:
            returnQR, decoded_info, points, _ = self.qcd.detectAndDecodeMulti(frame)
            
            if returnQR:
                for s, p in zip(decoded_info, points):
                    if s:
                        if s not in scanned:
                            scanned.append(s)
                        
                        frame = cv2.polylines(frame, [p.astype(int)], True, (0, 255, 0), 8)
                    
            self.currentImage = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.photo = ImageTk.PhotoImage(image=self.currentImage)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.window.after(15, self.update_Webcam)
        

# ============================================================= #
# ========================== QR Scan ========================== #
# ============================================================= #
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

scanned = []

app = WebcamApp(root)

root.mainloop()


# ============================================================= #
# ======================== Update data ======================== #
# ============================================================= #
SPREADSHEET_ID = "1PnVaAUNO2wG6fS9klsNLNhpuWz4pZ2MYPxKfCx0x2Zk"
TARGET_COLUMN = "G"
START_ROW = 3
MEMBER_EMAILS_COLUMN = "C"

MEMBER_EMAILS = f"{MEMBER_EMAILS_COLUMN}{str(START_ROW)}:{MEMBER_EMAILS_COLUMN}1000"

creds = utl.auth()

members = utl.get_values(creds, SPREADSHEET_ID, MEMBER_EMAILS)

for i in members["values"]:
    cell = TARGET_COLUMN + str(START_ROW)
    if i[0] in scanned:
        utl.write_values(creds, SPREADSHEET_ID, cell, 'USER_ENTERED')
    START_ROW += 1
