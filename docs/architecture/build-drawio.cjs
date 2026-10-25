// Regenerate how-it-fits.drawio from the NODES and WIRES data in how-it-fits.html,
// so the editable diagram and the interactive page cannot drift apart.
// Usage (from this folder): node build-drawio.cjs
'use strict';
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, 'how-it-fits.html'), 'utf8');
const start = html.indexOf('const ICONS');
const end = html.indexOf('// ---- Rendering.');
if (start < 0 || end < 0) throw new Error('Data block not found in how-it-fits.html');
const { ICONS, NODES, WIRES } = new Function(html.slice(start, end) + '\nreturn {ICONS, NODES, WIRES};')();

const DY = 90; // Room for the title above the canvas.
const COLORS = { ok: '#3f8a66', part: '#5b7fb8', todo: '#aa7d48' };
const STATE = { ok: 'Running', part: 'Built, not in the live flow', todo: 'Not built yet' };
const attr = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/\n/g, '&#10;');
const size = n => n.type.includes('agent') ? { w: 270, h: 92 } : n.type.includes('circle') ? { w: 66, h: 66 } : { w: 92, h: 92 };
const icon = name => 'data:image/svg+xml,' + Buffer.from(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#224f43" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${ICONS[name]}</svg>`).toString('base64');

const BASE = 'whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#b9c7bc;strokeWidth=1.5;shadow=0;fontFamily=Segoe UI;fontColor=#203c35;';
const BELOW = 'verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;align=center;spacingTop=4;';
function shapeStyle(n) {
  if (n.type.includes('agent')) return 'rounded=1;arcSize=18;' + BASE + 'align=left;verticalAlign=middle;spacingLeft=66;';
  if (n.type.includes('trigger')) return 'shape=delay;flipH=1;' + BASE + BELOW + 'labelWidth=150;';
  if (n.type.includes('circle')) return 'ellipse;' + BASE + BELOW + 'labelWidth=120;';
  return 'rounded=1;arcSize=18;' + BASE + BELOW + 'labelWidth=150;';
}
function tooltip(n) {
  return [n.tech, '', n.what, '', ...n.job.map(j => '• ' + j), '', 'Today: ' + (n.status || STATE[n.state]),
    ...(n.proof ? ['Proof: ' + n.proof] : []), ...(n.note ? ['', 'Note: ' + n.note] : []), '', 'Read: ' + n.refs].join('\n');
}

const cells = [];
cells.push(`<mxCell id="title" value="${attr('<b style="font-size:28px">purrpose<font color="#aa7d48">.</font></b> <span style="font-size:18px">How the parts fit</span><br><span style="font-size:13px;color:#62736d">Solid wires carry the request. Dashed wires are calls and sources. Three agents group the six roles in FULL_GUIDANCE §16. Hover a node for its notes.</span>')}" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;fontFamily=Segoe UI;fontColor=#203c35;" vertex="1" parent="1"><mxGeometry x="40" y="16" width="900" height="64" as="geometry"/></mxCell>`);
[['ok', 'running'], ['part', 'built, not in the live flow'], ['todo', 'not built yet']].forEach(([state, text], i) => {
  const x = 960 + i * 150;
  cells.push(`<mxCell id="lg${i}" value="" style="ellipse;fillColor=${COLORS[state]};strokeColor=#ffffff;strokeWidth=2;" vertex="1" parent="1"><mxGeometry x="${x}" y="40" width="12" height="12" as="geometry"/></mxCell>`);
  cells.push(`<mxCell id="lgt${i}" value="${attr(text)}" style="text;html=1;align=left;verticalAlign=middle;fontFamily=Segoe UI;fontSize=13;fontColor=#62736d;" vertex="1" parent="1"><mxGeometry x="${x + 18}" y="34" width="130" height="24" as="geometry"/></mxCell>`);
});

NODES.forEach(n => {
  const s = size(n);
  const big = n.type.includes('agent') ? 16 : 14;
  const label = `<b style="font-size:${big}px">${n.name}</b><br><span style="font-size:12px;color:#62736d">${n.sub}</span>`;
  cells.push(`<UserObject id="${n.id}" label="${attr(label)}" tooltip="${attr(tooltip(n))}"><mxCell style="${shapeStyle(n)}" vertex="1" parent="1"><mxGeometry x="${n.x}" y="${n.y + DY}" width="${s.w}" height="${s.h}" as="geometry"/></mxCell></UserObject>`);
  const ic = n.type.includes('circle') ? 28 : 34;
  const ix = n.type.includes('agent') ? 18 : (s.w - ic) / 2;
  cells.push(`<mxCell id="ic-${n.id}" value="" style="shape=image;image=${icon(n.icon)};imageAspect=1;movable=0;resizable=0;editable=0;" vertex="1" parent="${n.id}"><mxGeometry x="${ix}" y="${(s.h - ic) / 2}" width="${ic}" height="${ic}" as="geometry"/></mxCell>`);
  const dot = n.type.includes('circle') ? [50.1, 3.9] : [s.w - 7, -5];
  cells.push(`<mxCell id="st-${n.id}" value="" style="ellipse;fillColor=${COLORS[n.state]};strokeColor=#ffffff;strokeWidth=2;movable=0;resizable=0;" vertex="1" parent="${n.id}"><mxGeometry x="${dot[0]}" y="${dot[1]}" width="12" height="12" as="geometry"/></mxCell>`);
});

const EDGE = 'html=1;fontFamily=Segoe UI;fontSize=11;fontColor=#62736d;labelBackgroundColor=#fbfbf7;strokeColor=#9fb0a6;edgeStyle=orthogonalEdgeStyle;curved=1;';
const SOLID = EDGE + 'strokeWidth=2;endArrow=block;endFill=1;endSize=6;';
const DASHED = EDGE + 'strokeWidth=1.5;dashed=1;dashPattern=5 4;endArrow=oval;endFill=1;endSize=5;';
const SUB_EXIT = { provider: 0.15, hmem: 0.85 };
WIRES.forEach(([f, t, kind, label], i) => {
  let style;
  if (kind === 'main') {
    const exitY = f === 'gate' ? (t === 'qual' ? 0.35 : 0.65) : 0.5;
    style = SOLID + `exitX=1;exitY=${exitY};exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;`;
  } else if (kind === 'loopR') {
    style = SOLID + 'exitX=1;exitY=0.35;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;';
  } else if (kind === 'loopL') {
    style = SOLID + 'exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.65;entryDx=0;entryDy=0;';
  } else {
    const exitX = f === 'agent' ? SUB_EXIT[t] : 0.5;
    style = DASHED + `exitX=${exitX};exitY=1;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;`;
  }
  cells.push(`<mxCell id="w${i}" value="${attr(label || '')}" style="${style}" edge="1" parent="1" source="${f}" target="${t}"><mxGeometry relative="1" as="geometry"/></mxCell>`);
});

const xml = `<mxfile host="app.diagrams.net" type="device">
  <diagram id="how-it-fits" name="How it fits">
    <mxGraphModel dx="1400" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1420" pageHeight="1040" background="#fbfbf7" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        ${cells.join('\n        ')}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
`;
fs.writeFileSync(path.join(__dirname, 'how-it-fits.drawio'), xml);
console.log(`Wrote how-it-fits.drawio: ${NODES.length} nodes, ${WIRES.length} wires`);
