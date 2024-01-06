import tkinter as tk
import utilities as utl
import cv2
from PIL import Image, ImageTk


class WebcamApp:
    def __init__(self, window) -> None:
        self.window = window
        self.window.title("QR Registration")
        
        # OpenCV setup
        camera_id = 1  # 0 for front cam, 1 for back cam
        self.qcd = cv2.QRCodeDetector()
        self.video_capture = cv2.VideoCapture(camera_id)
        self.currentImage = None
        
        # Display
        root.state('zoomed')
        self.canvas = tk.Canvas(window, width=screen_width//3*2, height=screen_height//3*2)
        self.canvas.pack()
        
        tk.Label(window, text="REGISTERED USER",font=("Arial bold", 25), pady=50).pack()
        self.confirm_text = ""
        self.info = tk.Label(
            master=self.window, 
            text=self.confirm_text, 
            font=("Arial", 25),
            pady=10,
            fg="green"
        )
        self.info.pack()
        
        self.update_Webcam()
        
    def update_Webcam(self):
        returnValue, frame = self.video_capture.read()
        frame = cv2.resize(frame, (screen_width//3*2, screen_height//3*2))
        
        # If using front cam, uncomment below:
        # frame = cv2.flip(frame, 1)
        if returnValue:
            returnQR, decoded_info, points, _ = self.qcd.detectAndDecodeMulti(frame)
            
            if returnQR:
                for data, p in zip(decoded_info, points):
                    if data:
                        self.info.config(text=data)
                        if data not in scanned:
                            scanned.append(data)
                        
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
SPREADSHEET_ID = "1UT_GerjzJCv7Bu_MnEMHZUr533mF3xe0W0rMiUlHnq4"
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