import numpy as np, cv2
from PIL import Image
from rembg import remove, new_session
F="../fontes/originais/tucano-patio.jpg"
im=Image.open(F).convert('RGB'); W=2160; im=im.resize((W,int(im.height*W/im.width)),Image.LANCZOS); im.save('foto2160.png')
s=new_session('isnet-general-use')
m=remove(im,session=s,only_mask=True,post_process_mask=True)
m.save('mask0.png')
a=np.array(m); print(a.shape,(a>128).mean())
ys,xs=np.where(a>128); print('bbox',xs.min(),xs.max(),ys.min(),ys.max())
rgb=np.array(im); vis=(rgb*0.25+np.dstack([a*0.75,a*0.2,a*0.2])).astype(np.uint8)
g=(rgb*(a[...,None]/255.)+np.array([255,0,255])*(1-a[...,None]/255.)).astype(np.uint8)
Image.fromarray(g).crop((0,380,2160,1250)).save('corte0.png')
