# Zaslav Display v11.001: Х gets flag terminals on the heavy stroke (top and bottom).
# Run from the repo root on the v11.000 commit: python tools/build_v11_1.py
import re, subprocess, numpy as np, cv2, potrace
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.reverseContourPen import ReverseContourPen
FN='ZaslavDisplay-Regular'
S=2; BASE=961*S; W=800*S; H=1100*S
def P(x,y): return (x*S, BASE-y*S)
def cr(p0,p1,p2,p3,t):
    return tuple(0.5*((2*p1[i])+(-p0[i]+p2[i])*t+(2*p0[i]-5*p1[i]+4*p2[i]-p3[i])*t*t+(-p0[i]+3*p1[i]-3*p2[i]+p3[i])*t**3) for i in (0,1))
def stroke(d,path,wid,n=60):
    pts=[path[0]]+path+[path[-1]]
    for i in range(1,len(pts)-2):
        for t in np.linspace(0,1,n):
            x,y=cr(pts[i-1],pts[i],pts[i+1],pts[i+2],t); w=wid[i-1]+(wid[i]-wid[i-1])*t
            cx,cy=P(x,y); r=w*S/2; d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=255)
def finish(a,seed):
    a=a.astype(np.float32); rng=np.random.default_rng(seed)
    n=cv2.GaussianBlur(rng.normal(0,1,a.shape).astype(np.float32),(0,0),2.5)
    return (cv2.GaussianBlur(a,(0,0),2.5)+n*140)>127
def kha():
    im=Image.new('L',(W,H),0); d=ImageDraw.Draw(im)
    k=375/700; L=lambda y:120+(700-y)*k; sym=lambda p:(745-p[0],700-p[1])
    pts=[(74,700),(250,700),(252,662)]+[(L(y)+132,y) for y in (600,100)]
    pts+=[sym(p) for p in [(118,672),(80,676),(74,700),(250,700),(252,662)]]
    pts+=[(L(y),y) for y in (100,600)]+[(118,672),(80,676)]
    d.polygon([P(*p) for p in pts],fill=255)
    stroke(d,[(560,660),(440,470),(300,250),(170,45)],[46,42,40,44])
    for x,y,w in [(565,684,170),(160,16,180)]: stroke(d,[(x-w/2,y+2),(x,y),(x+w/2,y+4)],[30,40,28],n=40)
    return finish(np.array(im),13)
m=kha(); pl=potrace.Bitmap(~m).trace(turdsize=20,alphamax=1.0,opttolerance=0.3)
def draw(pen):
    for c in pl:
        sp=c.start_point; pen.moveTo((sp.x,sp.y))
        for s in c.segments:
            if s.is_corner: pen.lineTo((s.c.x,s.c.y)); pen.lineTo((s.end_point.x,s.end_point.y))
            else: pen.curveTo((s.c1.x,s.c1.y),(s.c2.x,s.c2.y),(s.end_point.x,s.end_point.y))
        pen.closePath()
b=BoundsPen(None); draw(TransformPen(b,(1/S,0,0,-1/S,0,BASE/S))); T=(1/S,0,0,-1/S,45-b.bounds[0],BASE/S)
b=BoundsPen(None); draw(TransformPen(b,T)); adv=round(b.bounds[2])+45
for e in ['otf','ttf']:
    f=TTFont(f'{FN}.{e}'); gs=f.getGlyphSet(); a=AreaPen(gs); gs['uni0406'].draw(a); want=np.sign(a.value)
    a=AreaPen(None); draw(TransformPen(a,T)); wrap=ReverseContourPen if np.sign(a.value)!=want else (lambda p:p)
    if e=='otf':
        top=f['CFF '].cff.topDictIndex[0]; pen=T2CharStringPen(adv,gs); draw(TransformPen(wrap(pen),T))
        top.CharStrings['uni0425']=pen.getCharString(private=top.Private,globalSubrs=f['CFF '].cff.GlobalSubrs); top.version='11.001'
    else:
        pen=TTGlyphPen(gs); draw(TransformPen(Cu2QuPen(wrap(pen),max_err=0.5),T)); f['glyf']['uni0425']=pen.glyph()
    f['hmtx']['uni0425']=(adv,45); f['head'].fontRevision=11.001
    for r in f['name'].names:
        if r.nameID==5: r.string='Version 11.001'
        if r.nameID==3: r.string='11.001;NOWXEL;ZaslavDisplay-Regular'
    f.save(f'{FN}.{e}')
f=TTFont(f'{FN}.ttf'); f.flavor='woff2'; f.save(f'{FN}.woff2')
L='А Б В Г Ґ Д Е Є Ж З И І Ї Й К Л М Н О П Р С Т Ў Х Ч Ш Щ Ь Ю Я Ꙗ'.split()
fo=ImageFont.truetype(f'{FN}.ttf',90); im=Image.new('RGB',(950,790),'white'); d=ImageDraw.Draw(im)
for i,ch in enumerate(L): d.text((95+(i%7)*130-d.textlength(ch,font=fo)/2,40+(i//7)*150),ch,font=fo,fill='black')
im.save('preview.png')
r=open('README.md').read()
for a,b in [("**Version 11.000 —","**Version 11.001 —"),
 ("`Х` (v11) comes from the same specimen: a heavy diagonal from top left to\nbottom right, a hairline from top right to bottom left, flat serifs on all\nfour ends.",
  "`Х` (v11) comes from the same specimen: a heavy diagonal from top left to\nbottom right, a hairline from top right to bottom left. The heavy stroke is\ncut flat at both ends with a flag pointing outward (left at the top, right\nat the bottom, v11.001); the hairline keeps slab serifs."),
 ("= 11.000, name ID 5 = `Version 11.000`","= 11.001, name ID 5 = `Version 11.001`"),("`11.000;NOWXEL","`11.001;NOWXEL"),("`v11.000`","`v11.001`"),("(e.g. 11.001 for fixes","(e.g. 11.002 for fixes"),("The build script is `tools/build_v11.py`.","Build scripts: `tools/build_v11.py`, `tools/build_v11_1.py`.")]: r=r.replace(a,b)
open('README.md','w').write(r)
h=open('demo.html').read().replace("Version 11.000 —","Version 11.001 —"); open('demo.html','w').write(h)
print('OK: Х updated, version 11.001, advance',adv)
