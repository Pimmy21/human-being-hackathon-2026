"""Original repo-native pixel kitten; SVG source and derived animated GIF.
No external image, model call or asset download is used.
"""
from pathlib import Path
from math import sin,pi
from PIL import Image,ImageDraw
import html
ROOT=Path(__file__).resolve().parents[2]/'design/mascot'
ROOT.mkdir(parents=True,exist_ok=True)
COLORS=['#ffffff','#613c32','#f5a34a','#e78335','#ffd18b','#fff2d7','#ef9a91','#3f8a79','#bfe0ce']
W,H,S=64,56,4

def frame(i):
 im=Image.new('P',(W,H),0)
 palette=[]
 for color in COLORS:palette.extend(bytes.fromhex(color[1:]))
 im.putpalette(palette+[0]*(768-len(palette)))
 d=ImageDraw.Draw(im);svg=[]
 def rect(box,c):
  d.rectangle(box,fill=c);x,y,r,b=box
  svg.append(f'<rect x="{x}" y="{y}" width="{r-x+1}" height="{b-y+1}" fill="{COLORS[c]}"/>')
 def poly(points,c):
  d.polygon(points,fill=c)
  svg.append(f'<polygon points="'+ ' '.join(f'{x},{y}' for x,y in points)+f'" fill="{COLORS[c]}"/>')
 # Three small stationary ground pixels keep the bouncing body visually anchored.
 rect((21,48,44,49),8)
 sway=round(3*sin(2*pi*i/16));bob=1 if i in range(4,10) else 0
 # Tail sits behind the body and sways slowly.
 tail=[(40,43),(49,43),(53+sway,39),(54+sway,31),(52+sway,28),(49+sway,29),(49+sway,36),(46,38),(40,38)]
 poly(tail,1)
 poly([(42,40),(48,40),(51+sway,36),(51+sway,31),(52+sway,31),(52+sway,38),(48,42),(42,42)],2)
 rect((50+sway,30,52+sway,32),4)
 # Seated body, chest, paws.
 poly([(22,28+bob),(40,28+bob),(44,36),(44,46),(40,48),(21,48),(18,45),(19,36)],1)
 poly([(23,29+bob),(39,29+bob),(42,37),(42,45),(38,46),(22,46),(20,44),(21,36)],2)
 poly([(28,31+bob),(35,31+bob),(37,39),(35,44),(28,44),(26,39)],5)
 rect((20,43,27,46),4);rect((35,43,42,46),4)
 rect((24,44,24,46),3);rect((38,44,38,46),3)
 rect((21,34,24,35),3);rect((39,34,41,35),3)
 # Ear tips and a broad, gently smiling face.
 poly([(17,12+bob),(17,4+bob),(20,4+bob),(26,11+bob),(37,11+bob),(43,4+bob),(46,4+bob),(46,18+bob),(48,21+bob),(48,28+bob),(44,33+bob),(20,33+bob),(15,28+bob),(15,20+bob)],1)
 poly([(19,13+bob),(19,7+bob),(25,13+bob),(38,13+bob),(44,7+bob),(44,18+bob),(46,22+bob),(46,27+bob),(42,31+bob),(21,31+bob),(17,27+bob),(17,21+bob)],2)
 poly([(20,9+bob),(24,13+bob),(20,15+bob)],6)
 poly([(43,9+bob),(39,13+bob),(43,15+bob)],6)
 rect((29,13+bob,31,17+bob),3);rect((33,13+bob,35,16+bob),3)
 rect((18,21+bob,22,22+bob),3);rect((41,21+bob,45,22+bob),3)
 poly([(26,25+bob),(37,25+bob),(39,28+bob),(36,31+bob),(27,31+bob),(24,28+bob)],5)
 blink=i in (12,13)
 if blink:
  rect((24,22+bob,27,22+bob),1);rect((37,22+bob,40,22+bob),1)
 else:
  rect((25,20+bob,27,23+bob),1);rect((37,20+bob,39,23+bob),1)
  rect((25,20+bob,25,20+bob),5);rect((37,20+bob,37,20+bob),5)
 rect((30,25+bob,33,26+bob),6);rect((31,27+bob,32,28+bob),1)
 rect((28,29+bob,30,29+bob),1);rect((33,29+bob,35,29+bob),1)
 rect((20,26+bob,23,26+bob),1);rect((40,26+bob,43,26+bob),1)
 # Tiny teal collar adds a recognizable Purrpose accent.
 rect((25,32+bob,38,33+bob),7);rect((31,34+bob,33,35+bob),4)
 svgtext=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" shape-rendering="crispEdges" role="img" aria-label="Orange kitten">'+''.join(svg)+'</svg>'
 return im.resize((W*S,H*S),Image.Resampling.NEAREST),svgtext
frames=[frame(i)[0] for i in range(16)]
frames[0].save(ROOT/'purrpose-ginger.gif',save_all=True,append_images=frames[1:],duration=150,loop=0,transparency=0,disposal=2,optimize=False)
frames[0].save(ROOT/'purrpose-ginger.png',transparency=0)
(ROOT/'purrpose-ginger.svg').write_text(frame(0)[1],encoding='utf-8')
print('Original kitten: 16 frames, 2.4 second loop, GIF bytes', (ROOT/'purrpose-ginger.gif').stat().st_size)
