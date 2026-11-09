# Usage: python3 tools/build_qr_sheet.py OUT_PDF   (pip install segno reportlab)
# The items list below must match the menu pages on the site. Add/remove entries when sections or how-to guides change.
import segno
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import black, HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
B="https://amschlitt.github.io/vero-guide/"
items=[("Welcome Book","Start here: everything about the house and area","welcome/"),
("House information","What is in the house, rules and pool safety","welcome/house/"),
("Check-in and check-out","Times, door code and departure checklist","welcome/stay/"),
("Food and drinks","Restaurants, bars, coffee and groceries","welcome/eat/"),
("Things to do","Beaches and attractions nearby","welcome/explore/"),
("Vero Beach and Event links","About our town, local events and community groups","welcome/vero/"),
("All how-to guides","Quick steps for everything in the house","how-to/"),
("How do I set the air conditioning?","Air conditioning and thermostat","how-to/thermostat/"),
("How do I connect to Wi-Fi and the TV?","Wi-Fi and TV","how-to/wifi-tv/"),
("How do I get in with my door code?","Self check-in and door code","how-to/check-in/"),
("What do I do before checkout?","Checkout checklist","how-to/checkout/"),
("How do I use the washer and dryer?","Washer and dryer","how-to/laundry/"),
("How does the pool work?","Private heated pool","how-to/pool/"),
("How do I use the fire pit and BBQ grill?","Fire pit and BBQ grill","how-to/fire-pit-grill/"),
("How do I use the Bluetooth speakers?","Bluetooth speakers","how-to/speakers/"),
("How do I use the safe?","In-home safe","how-to/safe/"),
("Where do the trash and recycling go?","Trash and recycling","how-to/trash/")]
W,H=letter;mx,my=0.5*inch,0.5*inch;cw=(W-2*mx)/2;ch=(H-2*my)/6
def wrap(t,f,s,w):
    out=[];cur=""
    for wd in t.split():
        n=(cur+" "+wd).strip()
        if stringWidth(n,f,s)<=w: cur=n
        else: out.append(cur);cur=wd
    return out+[cur]
import sys
c=canvas.Canvas(sys.argv[1] if len(sys.argv)>1 else "QR_Codes_1381_3rd_Court.pdf",pagesize=letter)
c.setTitle("QR codes - 1381 3rd Court")
for i,(title,sub,path) in enumerate(items):
    k=i%12
    if k==0 and i: c.showPage()
    col=k%2;row=k//2
    x=mx+col*cw;y=H-my-(row+1)*ch
    q=segno.make(B+path,error='m',micro=False);m=q.matrix;n=len(m)+8
    size=1.2*inch;u=size/n;qx=x+0.15*inch;qy=y+(ch-size)/2
    c.setFillColor(black)
    for r,rowd in enumerate(m):
        for cc,v in enumerate(rowd):
            if v: c.rect(qx+(cc+4)*u,qy+size-(r+5)*u,u+0.2,u+0.2,stroke=0,fill=1)
    tx=qx+size+0.1*inch;tw=cw-(tx-x)-0.15*inch
    lines=wrap(title,"Helvetica-Bold",12.5,tw);sl=wrap(sub,"Helvetica",8.5,tw)
    th=len(lines)*15+len(sl)*10.5+4;ty=y+ch/2+th/2-11
    c.setFont("Helvetica-Bold",12.5);c.setFillColor(black)
    for l in lines: c.drawString(tx,ty,l);ty-=15
    c.setFont("Helvetica",8.5);c.setFillColor(HexColor("#555555"));ty-=2
    for l in sl: c.drawString(tx,ty,l);ty-=10.5
c.save()
