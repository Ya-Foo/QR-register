import tkinter as tk
import cv2
import json
from PIL import Image, ImageTk

import api


class WebcamApp:
    def __init__(self, window) -> None:
        self.window = window
        self.window.title("QR Registration")
        
        # OpenCV setup
        with open("src/config.json", "r") as f:
            self.camera_id = json.loads(f.read())["camera_id"]
            
        self.qcd = cv2.QRCodeDetector()
        self.video_capture = cv2.VideoCapture(self.camera_id)
        self.currentImage = None
        
        # Display
        root.state('zoomed')
        self.canvas = tk.Canvas(
            window, 
            width=screen_width//3*2, 
            height=screen_height//3*2
        )
        self.canvas.pack()
        
        tk.Label(
            window, 
            text="REGISTERED USER",
            font=("Arial bold", 25), 
            pady=50
        ).pack()
        
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
        
        # Flip image if using webcam
        if not self.camera_id:
            frame = cv2.flip(frame, 1)
            
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
with open("src/config.json", "r") as f:
    data = json.loads(f.read())
    SPREADSHEET_ID = data["sheets_id"]
    
    SETTINGS = data["attendance"]
    PAGE = SETTINGS["page"]
    TARGET_COL = SETTINGS["register_column"]
    IDENTIFIER_COL = SETTINGS["identifier_column"]
    START_ROW = SETTINGS["start_row"]

IDENTIFIERS = f"'{PAGE}'!{IDENTIFIER_COL}{str(START_ROW)}:{IDENTIFIER_COL}1000"

creds = api.auth()

members = api.get_values(creds, SPREADSHEET_ID, IDENTIFIERS)
registered = len(scanned)

if registered:
    print(f"Registering {registered} members...")

    index = 1
    for i in members:
        cell = f"'{PAGE}'!{TARGET_COL}{str(START_ROW)}"
        
        # If registered, then mark attendance
        if i[0] in scanned:
            api.write_values(creds, SPREADSHEET_ID, cell, 'USER_ENTERED')
            
            print(f"\t{index}/{registered} cells updated")
            index += 1
            
        START_ROW += 1
else:
    print("No one attended :(")

print("\nProcess finished")