# Zaslav Display v11.000: new Ґ, Ч, Х + kerning, version, preview, README, demo.
# Run from the repo root on a clean v10.000 checkout: python3 tools/build_v11.py
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
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
FN='ZaslavDisplay-Regular'
for e in ['otf','ttf']:
    open(f'/tmp/v10.{e}','wb').write(subprocess.check_output(['git','show',f'HEAD:{FN}.{e}']))
KERN10=subprocess.check_output(['git','show','HEAD:kern.fea']).decode()
S=2; BASE=961*S; W=800*S; H=1100*S
yy,xx=np.mgrid[0:H,0:W]; FY=(BASE-yy)/S; FX=xx/S
def P(x,y): return (x*S, BASE-y*S)
def stem_I(dx):
    im=Image.new('L',(W,H),0); ImageDraw.Draw(im).text((dx*S,0),'І',font=ImageFont.truetype('/tmp/v10.ttf',1000*S),fill=255)
    return np.array(im)
def cr(p0,p1,p2,p3,t):
    return tuple(0.5*((2*p1[i])+(-p0[i]+p2[i])*t+(2*p0[i]-5*p1[i]+4*p2[i]-p3[i])*t*t+(-p0[i]+3*p1[i]-3*p2[i]+p3[i])*t**3) for i in (0,1))
def stroke(d,path,wid,n=60):
    pts=[path[0]]+path+[path[-1]]
    for i in range(1,len(pts)-2):
        for t in np.linspace(0,1,n):
            x,y=cr(pts[i-1],pts[i],pts[i+1],pts[i+2],t); w=wid[i-1]+(wid[i]-wid[i-1])*t
            cx,cy=P(x,y); r=w*S/2; d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=255)
def ell(d,x,y,rx,ry): cx,cy=P(x,y); d.ellipse([cx-rx*S,cy-ry*S,cx+rx*S,cy+ry*S],fill=255)
def finish(a,seed):
    a=a.astype(np.float32); rng=np.random.default_rng(seed)
    n=cv2.GaussianBlur(rng.normal(0,1,a.shape).astype(np.float32),(0,0),2.5)
    return (cv2.GaussianBlur(a,(0,0),2.5)+n*140)>127
def ghe():   # Ґ: stem, loop, top bar with hanging teardrop
    J=430; st=stem_I(237); st[:int(BASE-(J+80)*S),:]=0; st[FY>J+42+(FX-332)*0.5]=0
    im=Image.fromarray(st); d=ImageDraw.Draw(im)
    stroke(d,[(440,652),(340,686),(205,680),(110,632),(66,562),(84,486),(150,436),(250,414),(300,420),(345,J+5)],[26,38,68,110,126,112,86,68,66,60])
    ell(d,448,636,28,40); return finish(np.array(im),7)
def che():   # Ч: ustav Y-form
    J=430; XC=410; st=stem_I(XC-158); st[:int(BASE-(J+10)*S),:]=0
    im=Image.fromarray(st); d=ImageDraw.Draw(im)
    stroke(d,[(XC-15,J-20),(XC-50,J+40),(XC-160,600),(XC-235,650)],[128,122,114,106])
    stroke(d,[(XC+15,J-20),(XC+50,J+40),(XC+160,600),(XC+235,650)],[112,100,92,86])
    for x,w in [(XC-245,150),(XC+245,140)]: stroke(d,[(x-w/2,684),(x,682),(x+w/2,686)],[30,40,28],n=40)
    return finish(np.array(im),11)
def kha():   # Х: heavy \ , hairline /
    im=Image.new('L',(W,H),0); d=ImageDraw.Draw(im)
    stroke(d,[(185,660),(300,470),(430,250),(560,45)],[118,116,112,110])
    stroke(d,[(560,660),(440,470),(300,250),(170,45)],[46,42,40,44])
    for x,y,w in [(175,684,210),(565,684,170),(160,16,180),(575,16,220)]: stroke(d,[(x-w/2,y+2),(x,y),(x+w/2,y+4)],[30,40,28],n=40)
    return finish(np.array(im),13)
traced={}
for name,m in {'uni0490':ghe(),'uni0427':che(),'uni0425':kha()}.items():
    pl=potrace.Bitmap(~m).trace(turdsize=20,alphamax=1.0,opttolerance=0.3)
    def draw(pen,pl=pl):
        for c in pl:
            sp=c.start_point; pen.moveTo((sp.x,sp.y))
            for s in c.segments:
                if s.is_corner: pen.lineTo((s.c.x,s.c.y)); pen.lineTo((s.end_point.x,s.end_point.y))
                else: pen.curveTo((s.c1.x,s.c1.y),(s.c2.x,s.c2.y),(s.end_point.x,s.end_point.y))
            pen.closePath()
    b=BoundsPen(None); draw(TransformPen(b,(1/S,0,0,-1/S,0,BASE/S))); T=(1/S,0,0,-1/S,45-b.bounds[0],BASE/S)
    b=BoundsPen(None); draw(TransformPen(b,T)); traced[name]=(draw,T,round(b.bounds[2])+45)
pairs={(a,b):int(v) for a,b,v in re.findall(r'pos (\S+) (\S+) (-?\d+);',KERN10)}
G,C,X='uni0490','uni0427','uni0425'; gl={a for a,b in pairs}|{b for a,b in pairs}|{X}
new={k:v for k,v in pairs.items() if G not in k and C not in k}
def copy(n,src,right):
    for g in gl:
        v=pairs.get((src,g) if right else (g,src))
        if v: new[(n,g) if right else (g,n)]=v
copy(G,'uni0406',True); copy(G,'uni0421',False); copy(C,'uni0422',True); copy(C,'uni0422',False); copy(X,'uni0416',True); copy(X,'uni0416',False)
for e in ['otf','ttf']:
    f=TTFont(f'/tmp/v10.{e}'); gs=f.getGlyphSet(); a=AreaPen(gs); gs['uni0406'].draw(a); want=np.sign(a.value)
    for name,(draw,T,adv) in traced.items():
        a=AreaPen(None); draw(TransformPen(a,T)); wrap=ReverseContourPen if np.sign(a.value)!=want else (lambda p:p)
        if name not in f.getGlyphOrder():
            order=f.getGlyphOrder()+[name]
            if e=='otf':
                top=f['CFF '].cff.topDictIndex[0]; cs=top.CharStrings
                cs.charStringsIndex.append(cs.charStringsIndex[0]); cs.charStrings[name]=len(cs.charStringsIndex)-1; top.charset.append(name)
            else: f['glyf'].glyphs[name]=f['glyf']['.notdef']; f['glyf'].glyphOrder=order
            f.setGlyphOrder(order)
            for t in f['cmap'].tables:
                if t.isUnicode(): t.cmap[0x0425]=name
            gs=f.getGlyphSet()
        if e=='otf':
            top=f['CFF '].cff.topDictIndex[0]; pen=T2CharStringPen(adv,gs); draw(TransformPen(wrap(pen),T))
            top.CharStrings[name]=pen.getCharString(private=top.Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
            top.version='11.000'
        else:
            pen=TTGlyphPen(gs); draw(TransformPen(Cu2QuPen(wrap(pen),max_err=0.5),T)); f['glyf'][name]=pen.glyph()
        f['hmtx'][name]=(adv,45)
    cm={v:k for k,v in f.getBestCmap().items()}
    lines=['languagesystem DFLT dflt;','languagesystem cyrl dflt;','','feature kern {']
    for (p,q),v in sorted(new.items(),key=lambda kv:(f.getGlyphID(kv[0][0]),f.getGlyphID(kv[0][1]))):
        lines.append(f'    pos {p} {q} {v};  # {chr(cm[p])}{chr(cm[q])}')
    fea='\n'.join(lines+['} kern;'])+'\n'
    addOpenTypeFeaturesFromString(f,fea,tables=['GPOS'])
    f['head'].fontRevision=11.0
    for r in f['name'].names:
        if r.nameID==5: r.string='Version 11.000'
        if r.nameID==3: r.string='11.000;NOWXEL;ZaslavDisplay-Regular'
    f.save(f'{FN}.{e}')
open('kern.fea','w').write(fea)
f=TTFont(f'{FN}.ttf'); f.flavor='woff2'; f.save(f'{FN}.woff2')
L='А Б В Г Ґ Д Е Є Ж З И І Ї Й К Л М Н О П Р С Т Ў Х Ч Ш Щ Ь Ю Я Ꙗ'.split()
fo=ImageFont.truetype(f'{FN}.ttf',90); im=Image.new('RGB',(950,790),'white'); d=ImageDraw.Draw(im)
for i,ch in enumerate(L): d.text((95+(i%7)*130-d.textlength(ch,font=fo)/2,40+(i//7)*150),ch,font=fo,fill='black')
im.save('preview.png')
r=open('README.md').read()
for a,b in [("Hand-drawn Belarusian Cyrillic display typeface, work in progress.","Hand-drawn Cyrillic display typeface for Belarusian and Ukrainian, work in progress.\n\nРукописний кириличний шрифт для заголовків (Заслаў, Zaslau): білоруська та українська абетки, у розробці."),
 ("**Version 10.000 (X) — 30 uppercase letters + Ꙗ:**","**Version 11.000 — 31 uppercase letters + Ꙗ:**"),
 ("С Т Ў Ч Ш","С Т Ў Х Ч Ш"),
 ("`Ш`, `Щ` and `Ч` weren't in either source image — they're constructed from\nthe same stem/serif shapes as `І`. `Щ`'s descender tail and `Ч`'s bowl were\ndrawn to match a reference the user provided, then everything is run through\nthe same trace pipeline as the rest of the glyphs for a consistent texture.",
  "`Ш` and `Щ` weren't in either source image — they're constructed from the\nsame stem/serif shapes as `І`, with `Щ`'s descender tail drawn to match a\nphoto reference, then run through the same trace pipeline as the rest of the\nglyphs for a consistent texture.\n\n`Ґ` (v11) follows a light-painting reference: the lower `І` stem, cut on a\nslant, runs into a loop that sweeps left and up into the top bar, which ends\nin a hanging teardrop on the right.\n\n`Ч` (v11) is the ustav Y-form from a small printed specimen («КАЧІЕ ІХА»):\ntwo nearly symmetric arms with flat serifs meet at about 40 % of the height\non the lower `І` stem.\n\n`Х` (v11) comes from the same specimen: a heavy diagonal from top left to\nbottom right, a hairline from top right to bottom left, flat serifs on all\nfour ends. The build script is `tools/build_v11.py`."),
 ("Kerning: 295 pairs",f"Kerning: {len(new)} pairs"),("АЧ, ДЕ","АЧ, ХА, ДЕ"),("`У Ф Х Ц`","`У Ф Ц`"),
 ("= 10.000, name ID 5 = `Version 10.000`","= 11.000, name ID 5 = `Version 11.000`"),("`10.000;NOWXEL","`11.000;NOWXEL"),("`v10.000`","`v11.000`"),
 ("(e.g. 10.001 for fixes, 11.000 for new letters)","(e.g. 11.001 for fixes, 12.000 for new letters)")]: r=r.replace(a,b)
open('README.md','w').write(r)
h=open('demo.html').read()
for a,b in [("СТЎЧ","СТЎХЧ"),("Version 10.000 (X) — 30 uppercase letters + Ꙗ. Ш/Щ/Ч/Ю/Ь/Ꙗ","Version 11.000 — 31 uppercase letters + Ꙗ. Ш/Щ/Ю/Ь/Ꙗ"),
 ("    Note: Ґ's top hook was clipped at the edge of the source scan, so its tip is flat\n    rather than pointed — worth a cleaner source or manual touch-up later.\n","    Ґ, Ч and Х (v11) are drawn from photo and specimen references.\n"),("У Ф Х Ц and","У Ф Ц and")]: h=h.replace(a,b)
open('demo.html','w').write(h)
print('OK: Ґ Ч Х built, version 11.000,',len(new),'kerning pairs')
