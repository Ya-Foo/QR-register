import segno
from os import listdir, getcwd


alreadyMembers = [f.split('.')[0] for f in listdir(fr"{getcwd()}/qrcodes")]

with open("delegatesInfo.csv", 'r') as f:
    for delegate in f:
        data = delegate.strip().split(',')
        name, email = data[0].rstrip(), data[-1]
        
        # no need to create QR for already-members
        if name in alreadyMembers:
            continue
        alreadyMembers.append(name)
        
        img = segno.make_qr(email)

        img.save(
            fr'qrcodes/{name}.png',
            scale=10,
            border=1,
        )