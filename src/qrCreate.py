import segno
import json
import os

import api


parent_dir = os.getcwd()
directory = "qrcodes"
path = os.path.join(parent_dir, directory)

alreadyMembers = [f.split('.')[0] for f in os.listdir(path) if f.split('.')[1] == "png"]

with open("src/config.json", "r") as f:
    data = json.loads(f.read())
    SPREADSHEET_ID = data["sheets_id"]
    
    SETTINGS = data["info"]
    PAGE = SETTINGS["page"]
    START_ROW = SETTINGS["start_row"]

RANGE = f"'{PAGE}'!A{str(START_ROW)}:B1000"

creds = api.auth()

members = api.get_values(creds, SPREADSHEET_ID, RANGE)

new_members = len(members)-len(alreadyMembers)

print(f"Finding a total of {len(members)} members\n")
print(f"Detected {new_members} new members")

# If new members were found, then create code
if new_members:
    print(f"Creating QR codes for new members...")

    for name, identifier in members:
        # Just in case there are trailing whitespaces
        name, identifier = name.rstrip(), identifier.rstrip()
        
        if name not in alreadyMembers:
            alreadyMembers.append(name)
            
            img = segno.make_qr(identifier)

            img.save(
                f'qrcodes/{name}.png',
                scale=10,
                border=1,
            )
        
print("\nProcess finished")