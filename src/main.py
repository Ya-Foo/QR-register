import tkinter as tk
import customtkinter as ctk
import json
import cv2
import imutils
import os
import segno

import api

from PIL import Image, ImageTk


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # System parameters
        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        
        
        # configure window
        self.title("QR registration.py")
        self.grid_columnconfigure(0, weight = 2)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        
        self.toplevel_window = None
        
        
        # Registration data
        self.scanned = []
        
        
        # Left frame (Camera and Scan results)
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, padx=(30,15), pady=30, sticky="nsew")
        
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=3)
        self.left_frame.grid_rowconfigure(1, weight=1)
        
        # Scanned individual info
        self.scanINFO_frame = ctk.CTkFrame(self.left_frame, corner_radius=20)
        self.scanINFO_frame.grid(row=1, column=0, sticky="nsew", pady=(30, 0))
        self.scanINFO_frame.grid_columnconfigure(0, weight=1)
        self.scanINFO_frame.grid_columnconfigure(1, weight=5)
        self.scanINFO_frame.grid_rowconfigure(0, weight=1)
        
        self.scanINFO_img_frame = ctk.CTkFrame(self.scanINFO_frame, fg_color="transparent")
        self.scanINFO_img_frame.grid(row=0, column=0)
        self.infoICON = ctk.CTkImage(dark_image=Image.open("src/imgs/info.png"), size=(150, 150))
        ctk.CTkLabel(self.scanINFO_img_frame, image=self.infoICON, text="").place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.scanINFO_text_frame = ctk.CTkFrame(self.scanINFO_frame, fg_color="transparent")
        self.scanINFO_text_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 30), pady=30)
        for i in range(4):
            self.scanINFO_text_frame.grid_rowconfigure(i, weight=1)
        self.scanINFO_text_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.scanINFO_text_frame, font=("Consolas", 32), text="IDENTIFIER", text_color="#1F69A3").grid(row=0, column=0, sticky="wns")
        ctk.CTkLabel(self.scanINFO_text_frame, font=("Consolas", 32), text="NAME", text_color="#1F69A3").grid(row=2, column=0, sticky="wns")
            
        self.identifier_val = ctk.CTkLabel(self.scanINFO_text_frame, font=("Consolas", 26), text="\t", padx=20)
        self.identifier_val.grid(row=1, column=0, sticky="nsw")
        self.name_val = ctk.CTkLabel(self.scanINFO_text_frame, font=("Consolas", 26), text="\t", padx=20)
        self.name_val.grid(row=3, column=0, sticky="nsw")
        
        # configure OpenCV
        with open("src/config.json", "r") as f:
            self.camera_id = json.loads(f.read())["camera_id"]
            
        self.qcd = cv2.QRCodeDetector()
        self.video_capture = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)  # Select cam
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 720p resolution width
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # 720p resolution height
        self.currentImage = None
        self.vid_frame = tk.Canvas(self.left_frame)
        self.vid_frame.grid(row=0, column=0, sticky="nsew")
        
        
        # Right frame (Status and buttons)
        self.right_frame = ctk.CTkFrame(self, corner_radius=20)
        self.right_frame.grid(row=0, column=1, padx=(15,30), pady=30, sticky="new")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        
        # Buttons
        self.register_button = ctk.CTkButton(self.right_frame, text="Save and Register", command=self.save, font=("Consolas", 18), width=250, height=50)
        self.register_button.grid(row=0, column=0, pady=(20,10))
        
        self.qr_button = ctk.CTkButton(self.right_frame, text="Create QR codes", command=self.create, font=("Consolas", 18), width=250, height=50)
        self.qr_button.grid(row=1, column=0, pady=(10,0))
        
        # Register/scan + QR create status
        self.register_frame = ctk.CTkFrame(self.right_frame)
        self.register_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        self.register_count = 0  # To run through all the names in list
        self.register_index = 1  # To count how many have been registered
        self.totalScanned = ctk.CTkLabel(self.register_frame, text="Total scanned: ", font=("Consolas", 18))
        self.totalScanned.grid(row=0, column=0, sticky="nsw", pady=(25, 15), padx=25)
        
        ctk.CTkLabel(self.register_frame, text="Register status: ", font=("Consolas", 18)).grid(row=1, column=0, sticky="nsw", pady=(15, 10), padx=25)
        self.register_status = ctk.CTkLabel(self.register_frame, text="", font=("Consolas", 18))
        self.register_status.grid(row=2, column=0, sticky="nsw", pady=(0,15), padx=55)
        
        ctk.CTkLabel(self.register_frame, text="QR create status: ", font=("Consolas", 18)).grid(row=3, column=0, sticky="nsw", pady=(15, 10), padx=25)
        self.qr_status = ctk.CTkLabel(self.register_frame, text="", font=("Consolas", 18))
        self.qr_status.grid(row=4, column=0, sticky="nsw", pady=(0,25), padx=55)
        self.qr_count = 0        # To count how many QRs have been created
        
        
        # Load camera feed
        self.update()
        
    
    def update(self):
        success, frame = self.video_capture.read()
        frame = imutils.resize(frame, width=self.w*3//2)
        
        # Flip image if using webcam
        if not CAMERA_ID:
            frame = cv2.flip(frame, 1)
            
        if success:
            successQR, decode, pts, _ = self.qcd.detectAndDecodeMulti(frame)
            
            if successQR:
                for data, p in zip(decode, pts):
                    if data:
                        # Showing scanned info
                        self.identifier_val.configure(text=f"\t{data}")
                        self.name_val.configure(text=f"\t{MEMBERS_INFO[data]}")
                        
                        # Add data to queue to be registered later
                        if data not in self.scanned:
                            self.scanned.append(data)
                            self.totalScanned.configure(text=f"Total scanned: {len(self.scanned)}")
                            
                        frame = cv2.polylines(frame, [p.astype(int)], True, (0, 255, 0), 8)  # Draw rectangle around QR
                        
            # Place image on canvas then on app
            self.currentImage = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.photo = ImageTk.PhotoImage(image=self.currentImage)
            self.vid_frame.create_image(0, 0, image=self.photo, anchor=tk.NW)
            
            self.after(15, self.update)
            

    def save(self):
        global A_START_ROW
        registered = len(self.scanned)

        if registered:
            if self.register_count < len(ROOM_MEMBERS):
        
                cell = f"'{A_PAGE}'!{A_TARGET_COL}{str(A_START_ROW)}"
                
                # If registered, then mark attendance
                if ROOM_MEMBERS[self.register_count] in self.scanned:
                    api.write_values(creds, SPREADSHEET_ID, cell, 'USER_ENTERED')
                    self.register_status.configure(text=f"[{loading[self.register_index%4]}] Registering {self.register_index}/{registered}")
                    self.register_index += 1
                    
                A_START_ROW += 1
                
            else:
                self.register_count = 0

            self.register_status.after(10, self.save)
            self.register_count += 1

    def create(self):
        new = len(NEW_MEMBERS)
        if new:
            if self.qr_count < new:
                identifier = list(NEW_MEMBERS.keys())[self.qr_count]
                name = NEW_MEMBERS[identifier].rstrip()
                
                img = segno.make_qr(identifier)

                img.save(f'qrcodes/{name}.png',scale=10,border=1)
                
                self.qr_status.after(10, self.create)
                self.qr_status.configure(text=f"[{loading[self.qr_count%4]}] Creating {self.qr_count+1}/{new}")
                
            else:
                self.qr_count = 0
            self.qr_count += 1
        else:
            self.qr_status.configure(text="No new members detected")

if __name__ == "__main__":
    # Extract config
    with open("src/config.json", "r") as f:
        data = json.loads(f.read())
        SPREADSHEET_ID = data["sheets_id"]
        CAMERA_ID = data["camera_id"]
        
        # Settings regarding registration
        A_SETTINGS = data["attendance"]
        A_PAGE = A_SETTINGS["page"]
        A_TARGET_COL = A_SETTINGS["register_column"]
        A_IDENTIFIER_COL = A_SETTINGS["identifier_column"]
        A_START_ROW = A_SETTINGS["start_row"]
        A_IDENTIFIERS = f"'{A_PAGE}'!{A_IDENTIFIER_COL}{str(A_START_ROW)}:{A_IDENTIFIER_COL}1000"
            
        # Settings regarding members' info
        I_SETTINGS = data["info"]
        I_PAGE = I_SETTINGS["page"]
        I_START_ROW = I_SETTINGS["start_row"]
        I_IDENTIFIERS = f"'{I_PAGE}'!A{str(I_START_ROW)}:B1000"
        
    # Validation and authentication
    creds = api.auth()
    
    # Constants
    loading = ["-", "\\", "|", "/"]
    MEMBERS_INFO = {}
    for identifier, name in api.get_values(creds, SPREADSHEET_ID, I_IDENTIFIERS):
        MEMBERS_INFO[identifier] = name
        
    ROOM_MEMBERS = [i[0] for i in api.get_values(creds, SPREADSHEET_ID, A_IDENTIFIERS)]
    parent_dir = os.getcwd()
    directory = "qrcodes"
    path = os.path.join(parent_dir, directory)
    if not os.path.exists(directory):
        os.mkdir(path)
        
    OG_MEMBERS = [f.split('.')[0] for f in os.listdir(path) if f.split('.')[-1] == "png"]
    NEW_MEMBERS = {}
    for identifier, name in MEMBERS_INFO.items():
        if name not in OG_MEMBERS:
            NEW_MEMBERS[identifier] = name
    
    # Main app
    app = App()
    app.after(0, lambda:app.state('zoomed'))  # Fullscreen
    app.mainloop()