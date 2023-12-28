import qrcode as qr
from os import listdir, getcwd


formLink = "https://docs.google.com/forms/d/e/1FAIpQLSfEKW8_EMYSheT-OEH1jvUnqYudxS4aQAldVk_h6kJA5Sw_3Q/formResponse?entry.592778603="

alreadyMembers = [f.split('.')[0] for f in listdir(fr"{getcwd()}/qrcodes")]

with open("delegatesInfo.csv", 'r') as f:
    for delegate in f:
        data = delegate.strip().split(',')
        name, email = data[0].rstrip(), data[-1]
        
        # not need to create QR for already-members
        if name in alreadyMembers:
            continue
        alreadyMembers.append(name)
        
        img = qr.make(formLink+email)

        img.save(fr'qrcodes/{name}.png')