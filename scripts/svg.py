from xml.sax.saxutils import escape

FONT_SIZE = 6
LINE_HEIGHT = 7
CHAR_WIDTH = 4.2

BG = '#0d1117'
FG = '#58a6ff'

with open('assets/ascii.txt', 'r', encoding='utf-8') as f:
    lines = [line.rstrip('\n') for line in f]

max_len = max((len(l) for l in lines), default=0)

PADDING = 30
HEADER = 30

PORTRAIT_W = max_len * CHAR_WIDTH
PORTRAIT_H = len(lines) * LINE_HEIGHT

WINDOW_W = int(PORTRAIT_W + PADDING * 2)
WINDOW_H = int(PORTRAIT_H + PADDING * 2 + HEADER)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WINDOW_W}"
height="{WINDOW_H}"
viewBox="0 0 {WINDOW_W} {WINDOW_H}">
<rect width="100%" height="100%" fill="{BG}"/>
<rect x="1" y="1" width="{WINDOW_W-2}" height="{WINDOW_H-2}" rx="8" fill="{BG}" stroke="#30363d"/>
<circle cx="18" cy="17" r="5" fill="#ff5f56"/>
<circle cx="34" cy="17" r="5" fill="#ffbd2e"/>
<circle cx="50" cy="17" r="5" fill="#27c93f"/>
<text x="{WINDOW_W/2}" y="20" font-size="11" fill="#8b949e" font-family="Consolas, monospace" text-anchor="middle">arnav@github:~$</text>
<defs>
'''

delay = 0.0
last_x = PADDING
last_y = HEADER + PADDING

for i, line in enumerate(lines):
    text_width = len(line) * CHAR_WIDTH
    x = (WINDOW_W - text_width) / 2
    y = HEADER + PADDING + i * LINE_HEIGHT - 6
    last_x = x + text_width
    last_y = HEADER + PADDING + i * LINE_HEIGHT

    svg += f'''
<clipPath id="clip{i}">
<rect x="{x}" y="{y}" width="0" height="{LINE_HEIGHT+2}">
<animate attributeName="width" from="0" to="{text_width}" begin="{delay:.2f}s" dur="0.12s" fill="freeze"/>
</rect>
</clipPath>
'''
    delay += 0.018

svg += '</defs>\n'

for i, line in enumerate(lines):
    text_width = len(line) * CHAR_WIDTH
    x = (WINDOW_W - text_width) / 2
    y = HEADER + PADDING + i * LINE_HEIGHT
    svg += f'''
<text x="{x}" y="{y}" clip-path="url(#clip{i})"
font-size="{FONT_SIZE}"
font-family="Consolas, Courier New, monospace"
xml:space="preserve"
fill="{FG}">{escape(line)}</text>
'''

svg += f'''
<rect x="{last_x+2}" y="{last_y-5}" width="4" height="{FONT_SIZE}">
<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
</rect>
</svg>
'''

with open('assets/portrait.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

print('Generated assets/portrait.svg')
