"""Original side-view pixel kitten, with SVG source and a derived walk-cycle GIF.
Requires Pillow only when rebuilding design assets. No third-party artwork.
"""
from pathlib import Path
from math import sin,cos,pi
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]/'design/mascot'
COLORS=['#ffffff','#624133','#f5a34a','#dc7d35','#ffd18b','#fff1d6','#ed9d94','#3f8a79','#dce7db','#bd672e','#91b65b','#648e44','#b5cf7b','#f5d780']
W,H,S=88,58,4

def frame(i):
 im=Image.new('P',(W,H),0);palette=[]
 for c in COLORS:palette.extend(bytes.fromhex(c[1:]))
 im.putpalette(palette+[0]*(768-len(palette)))
 d=ImageDraw.Draw(im);svg=[]
 def rect(box,c):
  d.rectangle(box,fill=c);x,y,r,b=box
  svg.append(f'<rect x="{x}" y="{y}" width="{r-x+1}" height="{b-y+1}" fill="{COLORS[c]}"/>')
 def poly(points,c):
  d.polygon(points,fill=c)
  svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="{COLORS[c]}"/>')
 phase=2*pi*i/16;bob=round(.6*cos(phase*2));sway=round(sin(phase))
 # A small grassy patch with quiet blades and two tiny flowers.
 poly([(10,50),(13,47),(75,47),(79,50),(76,54),(14,54)],10)
 rect((15,52,74,54),11)
 for x,y in [(14,48),(20,49),(27,47),(36,50),(44,48),(52,50),(62,47),(70,49),(75,48)]:
  poly([(x-2,y+2),(x-2,y-1),(x,y+1),(x+1,y-3),(x+2,y+2)],11)
 for x in (18,31,48,66,72):rect((x,51,x+3,51),12)
 rect((16,47,16,49),11);rect((15,46,17,47),13)
 rect((73,46,73,48),11);rect((72,45,74,46),5)
 # Upturned tail, a relaxed tabby silhouette.
 poly([(27,30+bob),(21,28),(17+sway,21),(15+sway,11),(13+sway,7),(10+sway,7),(9+sway,11),(11+sway,22),(16,31),(24,36+bob)],1)
 poly([(25,31+bob),(20,28),(15+sway,20),(13+sway,10),(11+sway,9),(11+sway,14),(13+sway,23),(18,31),(24,34+bob)],2)
 rect((10+sway,9,12+sway,12),5)
 rect((12+sway,18,15+sway,20),3)
 def leg(anchor,offset,far=False):
  t=phase+offset;foot=anchor+round(5*sin(t));bottom=47-round(max(0,cos(t))*3)
  poly([(anchor-3,33+bob),(anchor+3,33+bob),(anchor+2,39),(foot+2,bottom-3),(foot+5,bottom-2),(foot+5,bottom),(foot-2,bottom),(foot-3,bottom-4),(anchor-2,39)],1)
  poly([(anchor-1,34+bob),(anchor+1,34+bob),(anchor,39),(foot+1,bottom-2),(foot+3,bottom-1),(foot-1,bottom-1),(foot-1,bottom-4),(anchor-1,39)],9 if far else 2)
  rect((foot-1,bottom-2,foot+3,bottom-1),4 if far else 5)
 # Far legs are drawn first and alternate with the near pair.
 leg(30,pi,True);leg(54,0,True)
 poly([(24,23+bob),(44,21+bob),(56,23+bob),(61,28+bob),(60,35+bob),(54,39+bob),(30,40+bob),(23,36+bob),(21,29+bob)],1)
 poly([(25,25+bob),(43,23+bob),(55,25+bob),(58,29+bob),(57,34+bob),(52,37+bob),(30,38+bob),(25,35+bob),(23,29+bob)],2)
 poly([(29,34+bob),(44,35+bob),(54,33+bob),(53,37+bob),(31,38+bob)],4)
 poly([(30,25+bob),(33,24+bob),(32,30+bob),(29,31+bob)],3)
 poly([(39,24+bob),(42,24+bob),(41,30+bob),(38,31+bob)],3)
 poly([(48,25+bob),(51,25+bob),(50,29+bob),(47,30+bob)],3)
 leg(28,0);leg(55,pi)
 # Small side-facing head and two upright ears.
 poly([(52,23+bob),(51,13+bob),(54,11+bob),(60,16+bob),(64,10+bob),(67,11+bob),(68,19+bob),(71,22+bob),(72,25+bob),(77,26+bob),(77,29+bob),(72,31+bob),(66,35+bob),(57,34+bob),(52,30+bob)],1)
 poly([(54,23+bob),(53,15+bob),(55,14+bob),(60,19+bob),(65,13+bob),(66,20+bob),(69,23+bob),(70,27+bob),(75,27+bob),(74,29+bob),(70,30+bob),(65,33+bob),(58,32+bob),(54,29+bob)],2)
 poly([(55,16+bob),(58,19+bob),(55,21+bob)],6)
 poly([(64,16+bob),(65,14+bob),(65,20+bob),(62,21+bob)],6)
 poly([(66,28+bob),(73,27+bob),(75,28+bob),(71,31+bob),(66,32+bob),(63,30+bob)],5)
 rect((65,23+bob,67,25+bob),1);rect((65,23+bob,65,23+bob),5)
 rect((75,26+bob,77,27+bob),6)
 rect((71,30+bob,73,30+bob),1)
 rect((57,25+bob,60,26+bob),3);rect((59,29+bob,62,29+bob),3)
 rect((72,24+bob,78,24+bob),1)
 # Subtle collar accent matches the earlier mascot.
 poly([(54,30+bob),(57,32+bob),(64,33+bob),(63,35+bob),(57,34+bob),(53,32+bob)],7)
 rect((62,35+bob,64,37+bob),4)
 svgtext=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" shape-rendering="crispEdges" role="img" aria-label="Orange kitten walking to the right">'+''.join(svg)+'</svg>'
 return im.resize((W*S,H*S),Image.Resampling.NEAREST),svgtext
frames=[frame(i)[0] for i in range(16)]
frames[0].save(ROOT/'purrpose-ginger.gif',save_all=True,append_images=frames[1:],duration=90,loop=0,transparency=0,disposal=2,optimize=False)
frames[0].save(ROOT/'purrpose-ginger.png',transparency=0)
(ROOT/'purrpose-ginger.svg').write_text(frame(0)[1],encoding='utf-8')
print('Side-view walking kitten generated:',(ROOT/'purrpose-ginger.gif').stat().st_size,'bytes')
