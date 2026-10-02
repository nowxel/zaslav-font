# Zaslav Display v12.000: Ш redrawn from a clean specimen, Ц (new) and Щ built from it.
# Ц = Ш without the middle stem, counter widened ~45 %, flag-cut descender; Щ = full Ш + same descender.
# Outlines were traced from the specimen and are stored here as plain coordinates (font units).
# Run from the repo root on the v11.002 commit: python3 tools/build_v12_000.py
import re, hashlib
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
FN='ZaslavDisplay-Regular'; VER='12.000'
G={
    'uni0428': (891, 'M 83 0 C 99 -1 130 0 153 1 C 200 5 286 5 322 2 C 343 0 401 0 428 2 C 438 2 490 3 557 3 C 668 4 694 5 735 7 C 746 8 771 9 791 10 C 821 10 827 11 830 12 C 840 16 841 18 843 57 C 843 70 844 90 845 100 C 846 120 846 124 842 128 C 839 132 835 133 826 133 C 815 133 811 135 808 143 C 807 146 807 153 806 219 C 806 274 805 295 804 301 C 803 312 803 380 804 401 C 806 424 807 469 808 539 L 809 605 L 811 617 C 812 623 815 635 817 643 C 823 667 821 678 811 683 L 808 685 L 780 685 C 737 684 695 685 681 685 C 665 686 661 686 657 682 C 650 676 651 668 660 658 C 668 650 671 646 673 637 C 679 623 679 615 676 586 C 674 575 673 558 672 548 C 671 537 670 522 669 514 C 668 506 667 491 666 480 C 666 469 665 456 665 450 C 662 413 661 355 664 324 C 665 315 666 293 666 275 C 667 256 668 235 668 228 C 672 173 674 111 673 96 C 673 83 667 74 658 71 C 651 69 627 70 591 74 C 581 75 568 76 561 76 C 549 77 534 81 530 83 C 525 87 525 89 527 112 C 529 144 530 199 528 241 C 525 311 525 339 526 394 C 526 423 527 473 527 503 C 528 560 530 593 532 606 C 533 610 536 621 540 631 C 545 649 545 650 545 659 C 545 672 544 686 542 691 C 541 693 538 696 537 697 C 533 699 533 700 525 699 C 514 699 468 699 429 699 C 389 699 392 700 376 688 C 363 679 360 676 360 666 C 360 663 361 659 361 658 C 362 657 364 650 366 643 C 370 627 373 621 379 612 C 385 604 386 601 389 576 C 391 557 391 553 391 525 C 391 508 391 485 390 473 C 390 461 389 432 389 407 C 389 383 389 353 388 341 C 386 273 386 227 390 176 C 392 148 393 94 392 87 C 391 81 386 73 382 70 C 376 66 370 65 336 64 C 292 62 282 63 276 65 C 262 71 253 83 246 107 L 243 119 L 243 196 C 243 247 243 280 244 297 C 245 316 245 326 244 339 C 244 349 243 366 242 377 C 242 389 241 408 240 421 C 238 445 238 464 240 493 C 240 501 241 529 242 555 C 243 611 242 603 258 631 C 272 655 273 656 273 670 C 273 679 273 682 272 686 C 270 691 265 696 260 697 C 255 699 227 699 204 697 C 195 697 163 696 126 696 C 65 696 63 696 61 694 C 52 689 52 683 59 662 C 67 636 71 629 86 620 C 103 609 103 607 99 556 C 98 545 97 528 97 518 C 96 500 96 499 93 475 C 93 467 92 452 91 443 C 91 433 89 415 88 402 C 86 380 86 374 85 312 C 85 260 84 242 83 226 C 80 198 80 115 83 100 C 86 80 85 78 68 77 C 58 77 57 77 53 74 C 46 69 44 63 45 44 C 47 20 49 15 55 8 C 60 3 67 1 83 0 Z'),
    'uni0426': (697, 'M 567 -170 C 569 -170 580 -170 590 -170 C 610 -170 613 -169 618 -164 C 622 -159 622 -157 633 -120 C 649 -64 651 -56 652 -48 C 652 -41 649 21 648 31 C 647 38 645 42 641 48 C 634 57 634 57 635 88 C 636 109 636 116 635 119 C 633 128 628 132 617 134 C 609 136 607 137 604 140 C 598 146 598 143 597 217 C 597 269 597 288 595 303 C 594 323 594 382 596 408 C 597 433 598 473 599 536 C 600 605 600 606 606 635 C 611 658 612 667 608 675 C 605 681 600 684 593 686 C 590 687 573 687 538 686 C 483 686 474 686 460 690 C 449 693 444 692 436 684 C 426 676 425 666 430 646 C 437 621 445 609 456 611 C 459 611 459 611 461 609 C 464 604 463 566 458 521 C 455 492 454 478 454 416 C 454 384 454 345 453 332 C 451 274 452 242 457 205 C 459 185 462 129 461 106 C 461 89 459 84 452 77 C 447 72 442 69 435 68 C 427 66 387 65 333 65 C 285 65 284 65 279 67 C 265 72 257 82 251 100 C 245 119 245 118 245 209 C 246 254 246 299 246 310 C 247 331 245 379 242 416 C 240 441 240 465 241 483 C 242 489 243 508 243 525 C 246 604 245 599 248 606 C 249 610 254 619 258 627 C 272 652 275 659 275 671 C 275 688 269 696 254 699 C 249 700 229 700 190 698 C 179 698 148 697 121 697 C 93 697 70 697 69 697 C 61 694 57 690 55 684 C 54 679 55 671 59 658 C 66 638 70 632 84 620 C 102 605 102 602 99 558 C 98 550 97 533 96 521 C 95 508 94 488 93 477 C 92 465 91 448 90 439 C 90 430 88 414 87 403 C 85 370 84 356 84 306 C 84 265 84 252 82 229 C 80 193 79 132 81 108 C 83 86 81 83 70 80 C 58 76 56 75 53 73 C 46 67 45 62 45 47 C 45 22 50 10 62 3 C 74 -3 105 -4 163 1 C 199 3 368 2 417 -1 C 435 -2 444 -2 459 1 C 477 5 486 4 503 -3 C 528 -13 540 -23 548 -44 L 551 -50 L 551 -157 L 554 -161 C 556 -167 560 -169 567 -170 Z'),
    'uni0429': (908, 'M 778 -170 C 780 -170 791 -170 801 -170 C 821 -170 824 -169 829 -164 C 833 -159 833 -157 844 -120 C 860 -64 862 -56 863 -48 C 863 -41 860 21 859 31 C 858 38 856 42 852 48 C 845 57 845 57 846 88 C 847 109 847 116 846 119 C 844 128 839 132 828 134 C 820 136 818 137 815 140 C 809 146 809 143 809 217 C 808 269 808 288 806 303 C 805 323 805 382 807 408 C 808 433 809 473 810 536 C 811 605 811 606 817 635 C 822 658 823 667 819 675 C 816 681 811 684 804 686 C 800 687 669 686 665 686 C 662 685 658 681 656 678 C 653 672 655 664 662 654 C 668 647 672 639 674 631 C 677 623 677 602 674 579 C 673 570 672 557 671 550 C 671 542 670 529 669 521 C 668 512 667 498 666 490 C 666 481 665 465 664 453 C 661 398 660 366 663 328 C 664 318 665 297 665 281 C 666 251 667 238 669 197 C 671 164 673 115 672 103 C 671 86 668 79 658 75 C 654 73 653 73 635 73 C 625 73 611 73 603 74 C 595 75 581 76 573 77 C 544 79 535 82 531 91 C 528 95 528 100 530 119 C 532 148 532 196 530 233 C 527 304 527 337 528 400 C 529 433 529 483 530 511 C 530 539 531 569 532 577 C 533 602 534 607 544 638 C 547 648 547 649 547 661 C 547 682 544 691 536 697 L 532 700 L 469 700 C 421 701 403 701 399 700 C 384 697 365 683 362 673 C 358 661 365 634 377 614 C 384 602 385 597 387 582 C 391 555 391 543 390 502 C 389 480 389 434 388 399 C 388 363 387 316 386 294 C 385 250 386 225 389 181 C 391 151 392 97 391 90 C 388 74 380 68 359 67 C 336 65 294 64 289 65 C 270 67 258 78 251 100 C 245 119 245 118 245 209 C 246 254 246 299 246 310 C 247 331 245 379 242 416 C 240 441 240 465 241 483 C 242 489 243 508 243 525 C 246 604 245 599 248 606 C 249 610 254 619 258 627 C 272 652 275 659 275 671 C 275 688 269 696 254 699 C 249 700 229 700 190 698 C 179 698 148 697 121 697 C 93 697 70 697 69 697 C 61 694 57 690 55 684 C 54 679 55 671 59 658 C 66 638 70 632 84 620 C 102 605 102 602 99 558 C 98 550 97 533 96 521 C 95 508 94 488 93 477 C 92 465 91 448 90 439 C 90 430 88 414 87 403 C 85 370 84 356 84 306 C 84 265 84 252 82 229 C 80 193 79 132 81 108 C 83 86 81 83 70 80 C 58 76 56 75 53 73 C 46 67 45 62 45 47 C 45 22 50 10 62 3 C 74 -3 106 -4 163 1 C 195 3 297 3 326 1 C 352 -2 389 -2 433 0 C 457 1 484 2 537 2 C 577 2 628 2 651 3 C 698 4 698 4 715 -3 C 739 -13 751 -23 759 -44 L 762 -50 L 762 -157 L 765 -161 C 767 -167 771 -169 778 -170 Z'),
}
assert hashlib.sha256(''.join(s for _,s in G.values()).encode()).hexdigest()[:12]=='929c2c7eda04', 'outline data damaged in copy-paste'
U={'uni0428':0x0428,'uni0426':0x0426,'uni0429':0x0429}
def draw(s,pen):
    t=s.split(); i=0
    while i<len(t):
        op=t[i]; i+=1; n={'M':2,'L':2,'C':6,'Z':0}[op]; v=[int(x) for x in t[i:i+n]]; i+=n
        if op=='M': pen.moveTo(tuple(v))
        elif op=='L': pen.lineTo(tuple(v))
        elif op=='C': pen.curveTo(tuple(v[:2]),tuple(v[2:4]),tuple(v[4:]))
        else: pen.closePath()
fea=open('kern.fea').read()
pairs={(a,b):int(v) for a,b,v in re.findall(r'pos (\S+) (\S+) (-?\d+);',fea)}
for (a,b),v in list(pairs.items()):
    if a=='uni0428': pairs.setdefault(('uni0426',b),v)
    if b=='uni0428': pairs.setdefault((a,'uni0426'),v)
for e in ['otf','ttf']:
    f=TTFont(f'{FN}.{e}')
    for name,(adv,s) in G.items():
        if name not in f.getGlyphOrder():
            order=f.getGlyphOrder()+[name]
            if e=='otf':
                top=f['CFF '].cff.topDictIndex[0]; cs=top.CharStrings
                cs.charStringsIndex.append(cs.charStringsIndex[0]); cs.charStrings[name]=len(cs.charStringsIndex)-1; top.charset.append(name)
            else: f['glyf'].glyphs[name]=f['glyf']['.notdef']; f['glyf'].glyphOrder=order
            f.setGlyphOrder(order)
            for t in f['cmap'].tables:
                if t.isUnicode(): t.cmap[U[name]]=name
        gs=f.getGlyphSet()
        if e=='otf':
            top=f['CFF '].cff.topDictIndex[0]; pen=T2CharStringPen(adv,gs); draw(s,pen)
            top.CharStrings[name]=pen.getCharString(private=top.Private,globalSubrs=f['CFF '].cff.GlobalSubrs); top.version=VER
        else:
            pen=TTGlyphPen(gs); draw(s,Cu2QuPen(pen,max_err=0.5)); f['glyf'][name]=pen.glyph()
        f['hmtx'][name]=(adv,45)
    cm={v:k for k,v in f.getBestCmap().items()}
    lines=['languagesystem DFLT dflt;','languagesystem cyrl dflt;','','feature kern {']
    for (p,q),v in sorted(pairs.items(),key=lambda kv:(f.getGlyphID(kv[0][0]),f.getGlyphID(kv[0][1]))):
        lines.append(f'    pos {p} {q} {v};  # {chr(cm[p])}{chr(cm[q])}')
    fea='\n'.join(lines+['} kern;'])+'\n'
    addOpenTypeFeaturesFromString(f,fea,tables=['GPOS'])
    f['head'].fontRevision=float(VER)
    for r in f['name'].names:
        if r.nameID==5: r.string=f'Version {VER}'
        if r.nameID==3: r.string=f'{VER};NOWXEL;ZaslavDisplay-Regular'
    f.save(f'{FN}.{e}')
open('kern.fea','w').write(fea)
f=TTFont(f'{FN}.ttf'); f.flavor='woff2'; f.save(f'{FN}.woff2')
r=open('README.md').read()
for a,b in [("**Version 11.001 — 31 uppercase letters + Ꙗ:**","**Version 12.000 — 32 uppercase letters + Ꙗ:**"),("Т Ў Х Ч Ш Щ","Т Ў Х Ц Ч Ш Щ"),
 ("`Ш` and `Щ` weren't in either source image — they're constructed from the\nsame stem/serif shapes as `І`, with `Щ`'s descender tail drawn to match a\nphoto reference, then run through the same trace pipeline as the rest of the\nglyphs for a consistent texture.",
  "`Ш` (v12) is traced from a clean specimen. `Ц` and `Щ` (v12) are built from\nit: `Ц` is `Ш` without the middle stem, with the counter widened by about\n45 %; `Щ` is the full `Ш`. Both get the same descender, about a quarter of the\ncap height deep, cut on a slant like a flag to echo the top of the left stem.\nThe outlines live in `tools/build_v12_000.py`. `Ц` borrows `Ш`'s kerning pairs."),
 ("Still missing: `У Ф Ц` and all lowercase letters.","Still missing: `У Ф` and all lowercase letters."),
 ("= 11.001, name ID 5 = `Version 11.001`","= 12.000, name ID 5 = `Version 12.000`"),("`11.001;NOWXEL","`12.000;NOWXEL"),("Git tag: `v11.001`","Git tag: `v12.000`"),
 ("(e.g. 11.002 for fixes, 12.000 for new letters)","(e.g. 12.001 for fixes, 13.000 for new letters)")]: r=r.replace(a,b)
r=re.sub(r'Kerning: \d+ pairs',f'Kerning: {len(pairs)} pairs',r); open('README.md','w').write(r)
h=open('demo.html').read()
for a,b in [("ТЎХЧШЩЬЮЯꙖ","ТЎХЦЧШЩЬЮЯꙖ"),("Version 11.001 — 31 uppercase letters + Ꙗ. Ш/Щ/Ю/Ь/Ꙗ are constructed","Version 12.000 — 32 uppercase letters + Ꙗ. Ш is traced from a clean specimen, Ц/Щ are built from it; Ю/Ь/Ꙗ are constructed"),("Still missing: У Ф Ц and lowercase.","Still missing: У Ф and lowercase.")]: h=h.replace(a,b)
open('demo.html','w').write(h)
try:
    from PIL import Image, ImageDraw, ImageFont
    L='А Б В Г Ґ Д Е Є Ж З И І Ї Й К Л М Н О П Р С Т Ў Х Ц Ч Ш Щ Ь Ю Я Ꙗ'.split()
    fo=ImageFont.truetype(f'{FN}.ttf',90); im=Image.new('RGB',(950,790),'white'); d=ImageDraw.Draw(im)
    for i,ch in enumerate(L): d.text((95+(i%7)*130-d.textlength(ch,font=fo)/2,40+(i//7)*150),ch,font=fo,fill='black')
    im.save('preview.png')
except ImportError: print('(Pillow not installed: preview.png not updated)')
print('OK: Ш Ц Щ built, version',VER,'-',len(pairs),'kerning pairs')
