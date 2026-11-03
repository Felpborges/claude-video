import numpy as np, cv2
from PIL import Image
OUT='../proj/assets/reais/'
f=cv2.imread('foto2160.png'); H,W=f.shape[:2]
a=cv2.imread('mask0.png',0).astype(np.uint8)
def poly(mask,pts,val):
    cv2.fillPoly(mask,[np.array(pts,np.int32)],val,lineType=cv2.LINE_AA)
# ── conserto do recorte
poly(a,[(1160,600),(1225,600),(1225,668),(1195,672),(1165,665)],0)          # árvore atrás do dorso
poly(a,[(925,590),(995,590),(995,618),(960,617),(925,624)],0)              # copa sobre a capota
poly(a,[(945,624),(1000,621),(1050,626),(1098,640),(1128,654),(1122,700),(1090,740),(950,740)],255)  # vidro de trás, inteiro
hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
oran=((hsv[...,0]<28)&(hsv[...,1]>110)&(hsv[...,2]>120)).astype(np.uint8)*255
zona=np.zeros_like(a); zona[1100:1160,1160:1290]=255
a[(oran>0)&(zona>0)]=0                                                     # calço da roda
a[1128:,1150:]=0
yy,xx=np.mgrid[0:H,0:W]
fora=(((xx-1217)/44.)**2+((yy-1084)/47.)**2>1)&(yy>1092)&(xx>1140)&(xx<1300)
a[fora]=0                                                                   # só a roda fica, sem o calço
# ── pás fora do corpo
blade=np.zeros_like(a)
poly(blade,[(474,610),(530,610),(528,700),(512,800),(474,800)],255)        # pá de cima
poly(blade,[(350,905),(462,880),(470,905),(400,1010),(350,1010)],255)      # pá de baixo
poly(blade,[(420,795),(478,795),(482,820),(445,826),(432,818)],255)        # toco à esquerda
poly(blade,[(325,745),(345,738),(478,806),(478,826),(445,826)],255)        # pá da esquerda
esq=np.zeros_like(a); poly(esq,[(325,745),(345,738),(478,806),(478,826),(445,826)],255)
cg=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY); a[(esq>0)&(cg<135)]=255
pas=cv2.bitwise_and(a,blade); corpo=cv2.subtract(a,pas)
# ── camada de perto: asa do lado da câmera e trem esquerdo. Na rotação, o eixo passa pelas duas rodas
# principais, então esta parte quase não sobe enquanto o nariz sobe atrás dela.
def maior(m):
    n,l,st,_=cv2.connectedComponentsWithStats((m>60).astype(np.uint8),8)
    if n<2: return m
    k=1+np.argmax(st[1:,4]); return np.where(l==k,m,0).astype(np.uint8)
# tira restos finos deixados ao separar as pás
z=corpo[600:1020,300:600]; corpo[600:1020,300:600]=cv2.morphologyEx(z,cv2.MORPH_OPEN,np.ones((7,7),np.uint8))
corpo=maior(corpo)
wz=np.zeros_like(a)
PERTO=[(70,850),(90,826),(130,818),(250,826),(430,834),(474,858),(575,866),(700,875),(880,888),(1010,905),(1062,945),(1040,994),(980,985),(762,935),(762,1148),(648,1148),(648,925),(580,912),(470,902),(380,880),(220,866),(85,856)]
poly(wz,PERTO,255)
asa=maior(cv2.bitwise_and(corpo,wz))
# ── luz: o avião está em contraluz; abre as sombras sem mudar a foto
def luz(img):
    x=(img/255.)**.74; x=np.clip(x*1.04,0,1); return (x*255).astype(np.uint8)
L=luz(f)
def rgba(alpha):
    al=cv2.GaussianBlur(alpha,(3,3),0)
    return np.dstack([L,al])
# atrás da asa de perto, o corpo precisa existir: preenche com a própria cor da barriga
Lf=L.copy()
linha=np.zeros_like(a); poly(linha,[(470,860),(1062,1012),(1062,700),(470,700)],255)
aberto=cv2.bitwise_and(wz,linha)
Lf=cv2.inpaint(Lf,cv2.dilate(aberto,np.ones((9,9),np.uint8)),7,cv2.INPAINT_TELEA)
corpo2=cv2.subtract(corpo,wz); corpo2=np.maximum(corpo2,aberto)
corpo2=maior(corpo2)                                                        # sem lascas soltas da asa
cv2.imwrite(OUT+'corpo.png',np.dstack([Lf,cv2.GaussianBlur(corpo2,(3,3),0)])); cv2.imwrite(OUT+'perto.png',rgba(asa)); cv2.imwrite(OUT+'pas.png',rgba(pas))
# ── fundo sem avião
buraco=cv2.dilate(a,np.ones((27,27),np.uint8))
buraco=np.maximum(buraco,cv2.dilate(pas,np.ones((15,15),np.uint8)))
buraco[780:880,1940:]=255
buraco[670:760,1470:1570]=255                                                 # outro avião à direita
buraco[1110:1210,240:]=np.maximum(buraco[1110:1210,240:],255)              # faixa da sombra
def reflexo(L):
    xs=np.arange(W); r=np.abs(((xs-L)%(2*L))-L); return np.clip(np.where(xs<L,xs,L-r).astype(int),0,L)
L0=330
pre=f.copy()
tip=(buraco>0)&(np.arange(W)[None,:]<L0+20)
pre=cv2.inpaint(pre,tip.astype(np.uint8)*255,9,cv2.INPAINT_TELEA)
preen=pre[:,reflexo(L0)].copy()
# chão perto da sombra: fonte só à esquerda dela
preen[1085:]=pre[1085:][:,reflexo(232)]
# pista e capim distantes: faixas retas, mediana da própria linha com textura real
validos=(buraco==0)
for y in range(796,884):
    v=f[y][validos[y]]
    if len(v)>30:
        med=np.median(v,axis=0)
        ruido=0
        preen[y]=np.clip(med+ruido,0,255)
# linha das árvores: acompanha a altura real ao longo do buraco
cinza=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32)
topo=np.zeros(W)
for x in range(W):
    col=cinza[470:800,x]; ix=np.where(col<105)[0]
    topo[x]=470+ix[0] if len(ix) else 800
cols=np.where((buraco[470:800]==0).all(axis=0))[0]
T=np.interp(np.arange(W),cols,cv2.blur(topo[cols][None,:],(25,1))[0])
ruidoT=cv2.GaussianBlur(np.random.default_rng(5).normal(0,1,(1,W)).astype(np.float32),(0,0),14)[0]*70
dentro=buraco[470:800].any(axis=0)
T=np.where(dentro,np.maximum(T,640)+ruidoT*.3,T)
base=792; rf=reflexo(L0); Tsrc=cv2.blur(topo[None,:],(9,1))[0][rf]
sm=cv2.resize(f,None,fx=.25,fy=.25,interpolation=cv2.INTER_AREA); hs=cv2.resize(buraco,(sm.shape[1],sm.shape[0]),interpolation=cv2.INTER_NEAREST)
ceu=cv2.GaussianBlur(cv2.resize(cv2.inpaint(sm,hs,10,cv2.INPAINT_TELEA),(W,H),interpolation=cv2.INTER_CUBIC),(0,0),5)
Y,X=np.mgrid[0:800,0:W].astype(np.float32)
esc=(base-Tsrc)/np.maximum(base-T,20)
mapy=base-(base-Y)*esc[None,:]
arv=cv2.remap(pre,rf.astype(np.float32)[None,:].repeat(800,0),mapy.astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
preen[:800]=ceu[:800]
ma=np.clip((Y-T[None,:])/2.5+.5,0,1)[...,None]
preen[:800]=(ceu[:800]*(1-ma)+arv*ma).astype(np.uint8)
pes=cv2.GaussianBlur((buraco>0).astype(np.float32),(25,25),0)[...,None]
pes=np.maximum(pes,(buraco>0)[...,None]*1.0)
bg=(f*(1-pes)+preen*pes).astype(np.uint8)
# suaviza o céu preenchido atrás da deriva
cv2.imwrite('bg2160.png',bg)
# ── sombra real: a razão foto/fundo na faixa do chão
fy=f[1090:1230,:].astype(np.float32).mean(2)+1; by=bg[1090:1230,:].astype(np.float32).mean(2)+1
som=np.clip(1-fy/by,0,1); som=cv2.GaussianBlur(som,(9,5),0)
som[(cv2.dilate(a,np.ones((5,5),np.uint8))[1090:1230,:]>0)]*=.92
som=np.clip((som-.08)/.6,0,1)
som*=np.clip((np.arange(som.shape[0])[:,None]+1090-1136)/6.,0,1)   # nada de roda presa na sombra
som*=np.clip((som.shape[1]-np.arange(som.shape[1])[None,:])/420.,0,1)      # a ponta da sombra se dissolve
som_rgba=np.dstack([np.zeros_like(som),np.zeros_like(som),np.zeros_like(som),som*.86*255]).astype(np.uint8)
cv2.imwrite(OUT+'sombra.png',som_rgba)
# ── placa final 0,8×, com céu e chão estendidos por reflexo
k=.8; pl=cv2.resize(bg,None,fx=k,fy=k,interpolation=cv2.INTER_AREA)
EXT_T,EXT_B=800,320
faixa=cv2.GaussianBlur(pl[:400],(0,0),2)
top=np.vstack([faixa,cv2.flip(faixa,0)])
bot=cv2.flip(pl[-EXT_B:],0)
cv2.imwrite(OUT+'fundo.jpg',np.vstack([top,pl,bot]),[cv2.IMWRITE_JPEG_QUALITY,93])
# conferência
c=(bg*1.0).copy(); ca=np.dstack([a]*3)/255.; c=c*(1-ca)+L*ca
cv2.imwrite('prova.jpg',cv2.resize(c.astype(np.uint8),None,fx=.6,fy=.6)); cv2.imwrite('bg_prova.jpg',cv2.resize(bg,None,fx=.6,fy=.6))
print('ok',pl.shape,'placa',pl.shape[0]+EXT_T+EXT_B)
