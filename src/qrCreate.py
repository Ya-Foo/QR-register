import segno
import utilities as utl
import json
from os import listdir, getcwd


alreadyMembers = [f.split('.')[0] for f in listdir(fr"{getcwd()}/qrcodes") if f.split('.')[1] == "png"]

with open("src/config.json", "r") as f:
    data = json.loads(f.read())
    SPREADSHEET_ID = data["sheets_id"]
    
    SETTINGS = data["info"]
    PAGE = SETTINGS["page"]
    START_ROW = SETTINGS["start_row"]

IDENTIFIERS = f"'{PAGE}'!A{str(START_ROW)}:B1000"

creds = utl.auth()

members = utl.get_values(creds, SPREADSHEET_ID, IDENTIFIERS)

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
                fr'qrcodes/{name}.png',
                scale=10,
                border=1,
            )
        
print("\nProcess finished")