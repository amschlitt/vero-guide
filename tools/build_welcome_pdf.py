import re,base64,posixpath,subprocess,os,sys
# Usage: python3 tools/build_welcome_pdf.py OUT_PDF   (run from anywhere; builds from the pages in this repo)
OUT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else 'Welcome_Book_1381_3rd_Court.pdf')
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
B="https://amschlitt.github.io/vero-guide/"
def read(p): return open(p,encoding='utf-8').read()
home=read('welcome/index.html')
css=re.search(r'<style>(.*?)</style>',home,re.S).group(1)
def main(p):
    s=read(p); m=re.search(r'<main class="wrap">(.*?)</main>',s,re.S).group(1)
    m=re.sub(r'<p><a href="[^"]*">&larr; Back to the menu</a></p>','',m)
    return re.sub(r'<footer>.*?</footer>','',m,flags=re.S)
def fixlinks(h,base):
    def r(m):
        u=m.group(1)
        if u.startswith(('http','#','mailto')): return m.group(0)
        return 'href="'+B+posixpath.normpath(posixpath.join(base,u)).lstrip('/')+('/' if u.endswith('/') else '')+'"'
    return re.sub(r'href="([^"]+)"',r,h)
intro=re.search(r'<div class="card">Welcome.*?</div>',home,re.S).group(0)
img=base64.b64encode(open('welcome/pool.jpg','rb').read()).decode()
secs=[('House information','welcome/house/index.html','welcome/house/'),('Check-in and check-out',None,None),('Food and drinks','welcome/eat/index.html','welcome/eat/'),('Things to do','welcome/explore/index.html','welcome/explore/'),('Vero Beach and Event links','welcome/vero/index.html','welcome/vero/')]
body=''
for t,p,b in secs:
    if p: c=fixlinks(main(p),b)
    else:
        g=lambda slug: main(f'how-to/{slug}/index.html')
        c='<h2>Arrival</h2><h3>Self check-in and door code</h3>'+g('check-in')+'<h3>Wi-Fi and TV</h3>'+g('wifi-tv')+'<h2>Departure</h2><h3>Checkout checklist</h3>'+g('checkout')+'<div class="card tip">Early check-in or late checkout? Message us in the Airbnb or VRBO app. A late checkout fee applies.</div>'
    body+=f'<section class="sec"><h1 class="sh">{t}</h1>{c}</section>'
guides=[('Air conditioning and thermostat','thermostat'),('Private heated pool','pool'),('Fire pit and BBQ grill','fire-pit-grill'),('Bluetooth speakers','speakers'),('Washer and dryer','laundry'),('In-home safe','safe'),('Trash and recycling','trash')]
g='<section class="sec"><h1 class="sh">How-to guides</h1><p>Each guide also has its own QR code in the house. Wi-Fi, TV, door code and checkout are in the Check-in and check-out section.</p>'
for t,s in guides: g+=f'<h2>{t}</h2>'+main(f'how-to/{s}/index.html')
body+=g+'</section>'
body=re.sub(r'<a class="back".*?</a>','',body)
toc='<h2>Inside this book</h2><div class="card"><ol style="margin:0;padding-left:1.3em;line-height:2"><li>House information</li><li>Check-in and check-out</li><li>Food and drinks</li><li>Things to do</li><li>Vero Beach and Event links</li><li>How-to guides</li></ol></div><div class="card tip">Scan the QR codes around the house for quick how-to guides, or visit the online welcome book any time.</div>'
pc='''
@page{size:Letter;margin:.6in .6in .7in}
body{background:#fff;font-size:12.5px;line-height:1.5}
.wrap{max-width:none;padding:0}
.cover{margin:0 0 14px}.cover img{width:100%;height:3.3in;object-fit:cover;border-radius:14px;display:block}
.cover h1{font-size:2.3rem;margin:.5em 0 .1em;color:#0f766e}.cover p{margin:0;color:#5b6b70;font:600 .9rem system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase}
h1.sh{font-size:1.7rem;color:#0f766e;margin:0 0 .3em;padding-bottom:.2em;border-bottom:2px solid #0f766e}
section.sec{break-before:page}
h2{break-after:avoid;font-size:1.15rem;margin:1.1em 0 .3em}h3{break-after:avoid;margin:.9em 0 0;font-family:system-ui,sans-serif;font-size:1rem}
.card{break-inside:avoid;margin:8px 0;padding:10px 14px}
ol.steps li,tr,p{break-inside:avoid}h2+p{break-after:avoid}
ol.steps li{padding:8px 0 8px 40px}
a{color:#0f766e}a.map{color:#5b6b70}
'''
html=f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Welcome Book - 1381 3rd Court</title><style>{css}{pc}</style></head><body><main class="wrap"><div class="cover"><img src="data:image/jpeg;base64,{img}" alt="Private heated pool"><h1>Welcome Book</h1><p>1381 3rd Court · Vero Beach, FL</p></div>{intro}{toc}{body}</main></body></html>'
import tempfile
TMP=os.path.join(tempfile.mkdtemp(),'wb_site.html')
open(TMP,'w',encoding='utf-8').write(html)
subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--no-pdf-header-footer','--print-to-pdf='+OUT,TMP],check=True,capture_output=True)
