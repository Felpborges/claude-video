# Versão "desenho" das camadas reais, pixel a pixel no mesmo lugar: cores chapadas na paleta do
# avião 3D do começo do filme e traço de tinta. Assim desenho e foto são o mesmo avião.
import numpy as np, cv2
R='../proj/assets/reais/'; OUT=R
INK=np.array([24,30,22],np.float32)[::-1]                      # BGR
def rgb(h): h=h.lstrip('#'); return np.array([int(h[4:6],16),int(h[2:4],16),int(h[0:2],16)],np.float32)

def chapado(bgr, alpha, verde, cinza, vidro=None):
    m=alpha>40
    # alisa forte para as cores seguirem a forma do avião, não o ruído da foto
    pq=cv2.resize(bgr,None,fx=.5,fy=.5,interpolation=cv2.INTER_AREA)
    pq=cv2.pyrMeanShiftFiltering(pq,10,26)
    lisa=cv2.resize(pq,(bgr.shape[1],bgr.shape[0]),interpolation=cv2.INTER_CUBIC)
    f=lisa.astype(np.float32)
    lum=cv2.GaussianBlur(cv2.cvtColor(lisa,cv2.COLOR_BGR2LAB)[...,0].astype(np.float32)/255.,(0,0),5)
    # tons do próprio avião: o desenho segue a luz da foto, em três faixas de verde como o avião 3D
    dentro=lum[m]; c1,c2=np.percentile(dentro,38),np.percentile(dentro,80)
    bandas=np.array([0,c1,c2,1.01])
    idx=np.clip(np.digitize(lum,bandas)-1,0,2)
    idx=cv2.medianBlur(idx.astype(np.uint8),9)
    def mapa(pal): return np.stack(pal)[idx]
    out=mapa(verde)
    q=(idx*90).astype(np.uint8)
    e=cv2.Canny(q,10,30).astype(np.float32)/255.
    e2=cv2.Canny(cv2.GaussianBlur(cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY),(0,0),1.6),70,150).astype(np.float32)/255.
    linha=cv2.GaussianBlur(np.maximum(e*.7,e2*.8),(3,3),0)
    sil=cv2.morphologyEx((alpha>110).astype(np.uint8)*255,cv2.MORPH_GRADIENT,np.ones((5,5),np.uint8)).astype(np.float32)/255.
    sil=cv2.GaussianBlur(sil,(3,3),0)
    tinta=np.clip(np.maximum(linha,sil),0,1)*m
    out=out*(1-tinta[...,None])+INK*tinta[...,None]
    return np.clip(out,0,255).astype(np.uint8), (tinta*255).astype(np.uint8)

VERDE=[rgb('#2d4a2e'),rgb('#4c7848'),rgb('#a9b9a0')]
CINZA=[rgb('#4d5753'),rgb('#7d8781'),rgb('#b2bab1')]
for n in ['corpo','perto','pas']:
    a=cv2.imread(R+n+'.png',cv2.IMREAD_UNCHANGED); bgr=a[...,:3]; al=a[...,3]
    hsv=cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV)
    vid=np.zeros(al.shape,np.float32)
    if n=='corpo':
        z=np.zeros(al.shape,np.uint8)
        cv2.fillPoly(z,[np.array([(820,780),(900,640),(1000,618),(1100,640),(1130,660),(1110,740),(990,760),(850,800)],np.int32)],255)
        vid=cv2.GaussianBlur(((z>0)&((hsv[...,2]>95)|(hsv[...,0]>85))).astype(np.float32),(0,0),2.5)
    des,tinta=chapado(bgr,al,VERDE,CINZA)
    cv2.imwrite(OUT+'des-'+n+'.png',np.dstack([des,al]))
    tinta=np.minimum(tinta,(al>0).astype(np.uint8)*255)
    cv2.imwrite(OUT+'des-linha-'+n+'.png',np.dstack([np.full(al.shape,22,np.uint8),np.full(al.shape,30,np.uint8),np.full(al.shape,24,np.uint8),tinta]))

# ── cenário desenhado, no mesmo desenho do fundo real
fb=cv2.imread(R+'fundo.jpg'); H,W=fb.shape[:2]
f=fb.astype(np.float32); hsv=cv2.cvtColor(fb,cv2.COLOR_BGR2HSV).astype(np.float32)
lum=cv2.cvtColor(fb,cv2.COLOR_BGR2GRAY).astype(np.float32)
foto=cv2.imread('foto2160.png'); cz=cv2.cvtColor(foto,cv2.COLOR_BGR2GRAY).astype(np.float32)
mask0=cv2.dilate(cv2.imread('mask0.png',0),np.ones((31,31),np.uint8))
topo2=np.zeros(2160,np.float32); ok=np.zeros(2160,bool)
for x in range(2160):
    col=cz[440:800,x]; ix=np.where(col<105)[0]
    if len(ix) and not mask0[440:800,x].any(): topo2[x]=440+ix[0]; ok[x]=True
xs=np.arange(2160); topo2=np.interp(xs,xs[ok],cv2.blur(topo2[ok][None,:],(9,1))[0])
topo=800+np.interp(np.arange(W)/.8,xs,topo2)*.8
fim=int(800+800*.8); faixa=int(800+880*.8)
Y=np.arange(H)[:,None]
SKY=rgb('#c4cbbf'); NUV=rgb('#d9ddd2'); ARV1=rgb('#9ca89a'); ARV2=rgb('#7f8e7d')
AREIA=[rgb('#a99a7a'),rgb('#bcae8f'),rgb('#c9bb9c'),rgb('#d6caad')]
out=np.zeros_like(f)
ceu=(Y<topo[None,:])
nuvem=cv2.GaussianBlur(((lum>200)&ceu).astype(np.float32),(0,0),7)
nuvem=(nuvem>.5).astype(np.float32); nuvem=cv2.GaussianBlur(nuvem,(0,0),1.5)
# céu liso como o do avião 3D, só um degradê leve; as nuvens da foto não entram no desenho
gy=np.clip(Y/float(fim),0,1)[...,None]
out[:]=SKY*(.95+.05*gy)
nuvem[:]=0
mata=(Y>=topo[None,:])&(Y<=fim)
tom=cv2.GaussianBlur(lum,(0,0),6)
out[mata]=np.where((tom[mata]<70)[:,None],ARV2,ARV1)
chao=Y>faixa
pista=(Y>fim)&(Y<=faixa)
l2=cv2.GaussianBlur(lum,(0,0),2)/255.
bandas=np.array([0,.45,.58,.7,1.01]); idx=np.clip(np.digitize(l2,bandas)-1,0,3)
ar=np.stack(AREIA)[idx]
out[chao[:,0]]=ar[chao[:,0]]
PI=[rgb('#a39a82'),rgb('#b3a985'),rgb('#9da07a')]
lp=cv2.GaussianBlur(lum,(0,0),3)
for y in range(fim+1,faixa+1): out[y]=PI[0] if lp[y].mean()<120 else (PI[2] if f[y,:,1].mean()>f[y,:,2].mean()+4 else PI[1])
# pontilhado do chão do começo do filme
yy,xx=np.mgrid[0:H,0:W]
pts=(((xx+(yy//26)%2*13)%26-13)**2+((yy%26)-13)**2)<9
out[chao[:,0]&False]=out[chao[:,0]&False]
out=np.where((pts&chao)[...,None],out*.78,out)
# traço fino na linha das árvores e no horizonte
borda=cv2.Canny((mata*255).astype(np.uint8),50,150).astype(np.float32)/255.
borda=np.maximum(borda,cv2.Canny((nuvem*255).astype(np.uint8),50,150).astype(np.float32)/255.*.5)
borda=cv2.GaussianBlur(borda,(3,3),0)*.55
out=out*(1-borda[...,None])+INK*borda[...,None]
cv2.imwrite(OUT+'des-fundo.jpg',np.clip(out,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,93])
print('horizonte',fim,'de',H)
# prova: lado a lado
a=cv2.imread(R+'corpo.png',cv2.IMREAD_UNCHANGED); d=cv2.imread(OUT+'des-corpo.png',cv2.IMREAD_UNCHANGED)
def sobre(x,bgc):
    al=x[...,3:]/255.; return (x[...,:3]*al+bgc*(1-al)).astype(np.uint8)
crop=lambda im: im[560:1180,60:2000]
pf=crop(cv2.resize(fb[800:800+1296],(2160,1620)))
cv2.imwrite('prova-des.jpg',cv2.resize(np.vstack([sobre(crop(a),pf),sobre(crop(d),crop(cv2.resize(out[800:800+1296],(2160,1620)).astype(np.uint8)))]),None,fx=.5,fy=.5))
