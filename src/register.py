import tkinter as tk
import customtkinter as ctk
import json
import cv2
import imutils

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
        
        
        # Scanned
        self.scanned = []
        
        
        # Left frame (Camera and Scan results)
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, padx=(30,15), pady=30, sticky="nsew")
        
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=3)
        self.left_frame.grid_rowconfigure(1, weight=1)
        
        
        # Scan individual info
        self.scanINFO_frame = ctk.CTkFrame(self.left_frame, corner_radius=20)
        self.scanINFO_frame.grid(row=1, column=0, sticky="nsew", pady=(30, 0))
        
        self.scanINFO_frame.grid_columnconfigure(0, weight=1)
        self.scanINFO_frame.grid_columnconfigure(1, weight=1)
        self.scanINFO_frame.grid_columnconfigure(2, weight=4)
        self.scanINFO_frame.grid_rowconfigure(0, weight=1)
        
        self.scanINFO_img_frame = ctk.CTkFrame(self.scanINFO_frame, fg_color="transparent")
        self.scanINFO_img_frame.grid(row=0, column=0)
        self.infoICON = ctk.CTkImage(dark_image=Image.open("src/imgs/info.png"), size=(150, 150))
        ctk.CTkLabel(self.scanINFO_img_frame, image=self.infoICON, text="").place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.scanINFO_labels_frame = ctk.CTkFrame(self.scanINFO_frame, fg_color="transparent")
        self.scanINFO_labels_frame.grid(row=0, column=1, sticky="nsew")
        self.scanINFO_val_frame = ctk.CTkFrame(self.scanINFO_frame, fg_color="transparent")
        self.scanINFO_val_frame.grid(row=0, column=2, sticky="nsw")
        labels = ["IDENTIFIER", "NAME", "COUNTRY"]
        for i in range(3):
            self.scanINFO_labels_frame.grid_rowconfigure(i, weight=1)
            self.scanINFO_val_frame.grid_rowconfigure(i, weight=1)
            ctk.CTkLabel(self.scanINFO_labels_frame, font=("Consolas", 32), text=labels[i], text_color="#1E6AA4").grid(row=i, column=1, sticky="w")
            
        self.identifier_val = ctk.CTkLabel(self.scanINFO_val_frame, font=("Consolas", 26), text="")
        self.name_val = ctk.CTkLabel(self.scanINFO_val_frame, font=("Consolas", 26), text="")
        self.country_val = ctk.CTkLabel(self.scanINFO_val_frame, font=("Consolas", 26), text="")
        self.identifier_val.grid(row=0, column=0, sticky="w")
        self.name_val.grid(row=1, column=0, sticky="w")
        self.country_val.grid(row=2, column=0, sticky="w")
        
        
        # All attendees (Right frame)
        self.right_frame = ctk.CTkFrame(self, corner_radius=20)
        self.right_frame.grid(row=0, column=1, padx=(30,15), pady=30, sticky="nsew")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=5)
        self.right_frame.grid_columnconfigure(0, weight=1)
        
        self.allINFO = ctk.CTkScrollableFrame(self.right_frame, corner_radius=20)
        self.allINFO.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,20))
        self.allINFO.grid_columnconfigure(0, weight=1)
        self.allINFO.grid_rowconfigure(0, weight=1)
        self.allINFO.grid_rowconfigure(1, weight=1)
        self.totalScanned = ctk.CTkLabel(self.allINFO, text="Total scanned: ", font=("Consolas", 18))
        self.totalScanned.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        ctk.CTkLabel(self.allINFO, text="Status: ", font=("Consolas", 18)).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.allINFO.grid_rowconfigure(2, weight=5)
        self.status = ctk.CTkLabel(self.allINFO, text="", font=("Consolas", 14))
        self.status.grid(row=2, column=0, padx=10, pady=10)
        
        self.register_button = ctk.CTkButton(self.right_frame, text="Save and Register", command=self.save, font=("Consolas", 18), width=250, height=50)
        self.register_button.grid(row=0, column=0)
        
        
        # configure OpenCV
        with open("src/config.json", "r") as f:
            self.camera_id = json.loads(f.read())["camera_id"]
            
        self.qcd = cv2.QRCodeDetector()
        self.video_capture = cv2.VideoCapture(self.camera_id)
        self.currentImage = None
        self.vid_frame = tk.Canvas(self.left_frame)
        self.vid_frame.grid(row=0, column=0, sticky="nsew")
        
        
        # Load camera feed
        self.update()
        
    
    def update(self):
        ret, frame = self.video_capture.read()
        frame = imutils.resize(frame, width=self.w*3//2)
        
        # Flip image if using webcam
        if not self.camera_id:
            frame = cv2.flip(frame, 1)
            
        if ret:
            retQR, decode, pts, _ = self.qcd.detectAndDecodeMulti(frame)
            
            if retQR:
                for data, p in zip(decode, pts):
                    if data:
                        self.identifier_val.configure(text=data)
                        if data not in self.scanned:
                            self.scanned.append(data)
                            self.totalScanned.configure(text=f"Total scanned: {len(self.scanned)}")
                            
                        frame = cv2.polylines(frame, [p.astype(int)], True, (0, 255, 0), 8)
                        
            self.currentImage = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.photo = ImageTk.PhotoImage(image=self.currentImage)
            self.vid_frame.create_image(0, 0, image=self.photo, anchor=tk.NW)
            
            self.after(15, self.update)
            

    def save(self):
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
        registered = len(self.scanned)

        if registered:
            index = 1
            registerStatus = ""
            for i in members:
                cell = f"'{PAGE}'!{TARGET_COL}{str(START_ROW)}"
                
                # If registered, then mark attendance
                if i[0] in self.scanned:
                    api.write_values(creds, SPREADSHEET_ID, cell, 'USER_ENTERED')
                    registerStatus += "Registering {i[0]}......{index}/{registered}\n"
                    self.status.configure(text=registerStatus)
                    index += 1
                    
                START_ROW += 1
                
            ctk.CTkLabel(self.allINFO, text="You can close this window now.", font=("Consolas", 18)).grid(row=index+1, column=0, padx=10, pady=10)
        else:
            ctk.CTkLabel(self.allINFO, text="No one attended :(", font=("Consolas", 14)).grid(row=2, column=0, padx=10, pady=10)



if __name__ == "__main__":
    app = App()
    app.after(0, lambda:app.state('zoomed'))  # Fullscreen
    app.mainloop()