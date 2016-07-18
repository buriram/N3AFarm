import microgear.client as netpie
import time
import base64
from picamera import PiCamera
from io import BytesIO
import zlib

key = '<your key>'
secret = '<your secret key>'
app = '<application name>'

netpie.create(key,secret,app,{'debugmode': True})
connected = False

def connection():
 global connected
 connected = True
 print("Connected")
 
def subscription(topic,msg):
 global this_role,ready_to_send
 if this_role == 'reciever' :
  decode_base64(msg,None) # don't need to save on disk
  running=False
 else :
  if not ready_to_send :
   if msg =='iamok':
    ready_to_send = True
    print "Reciever is ready"
  
   
 

def callback_error(msg) :
    print(msg)

def callback_reject(msg) :
    print (msg)
    print ("Script exited")
    exit(0)

def encode_base64(img_data):
 encoded = None

 try:
  #compress it first.
  compressed_data = zlib.compress(img_data.getvalue(),9)
  
  #encode it to base64 string
  encoded = base64.b64encode(compressed_data)  
 except:
  pass 
  
 return encoded
  
def decode_base64(compressed_b64str=None,save_to_file=None): 
 try :
  #firstly, decode it
  decoded = base64.decodestring(compressed_b64str)
  decompr = zlib.decompress(decoded)
  #save it if is needed.
  if save_to_file is not None:
   with open(save_to_file,"wb") as fh:
    fh.write(decompr)
  else:
   #just display on screen
   w,h = 640,480
   image = Image.fromstring('RGB',(w,h),decompr)
   image.show()
 except:
  pass   

def snap():
 global camera
 
 str_img = BytesIO()
 camera.start_preview()
 time.sleep(2)
 camera.capture(str_img,format='jpeg')
 camera.stop_preview()
 str_img.seek(0) 
 
 return str_img
 

camera = PiCamera()
camera.resolution=(640,480)


this_name = 'n3a2'     
those_name = 'n3a1'
this_role = 'sender'
running = True
ready_to_send = False

netpie.setname(this_name)
netpie.on_reject = callback_reject
netpie.on_connect = connection
netpie.on_message = subscription
netpie.on_error = callback_error
netpie.subscribe("/test")
netpie.connect(False) 



if this_role=='sender':
 while not ready_to_send :
  netpie.chat(those_name,'ruok')
  time.sleep(2)
   
 snap_shot = snap()
 b64 = encode_base64(snap_shot)
 netpie.chat(those_name,b64)
 
 time.sleep(2)
else :
 
 while running:
  pass
