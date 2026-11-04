import base64, math, random, re
NM="node_modules/"  # run: npm i @fontsource/caveat @fontsource/quicksand devicon
def b64(p): return base64.b64encode(open(p,"rb").read()).decode()
CAV=b64(NM+"@fontsource/caveat/files/caveat-latin-600-normal.woff2")
QS=b64(NM+"@fontsource/quicksand/files/quicksand-latin-500-normal.woff2")
QS6=b64(NM+"@fontsource/quicksand/files/quicksand-latin-600-normal.woff2")

# ---------- EDIT ME: your numbers ----------
CFG=dict(
 name="Akshita", college="VJTI, Mumbai",
 bullets=["I enjoy exploring technology and learning how things work",
          "Currently learning, experimenting, and improving one step at a time",
          "I like solving problems and turning ideas into practical projects",
          "Open to learning from others and collaborating on interesting things"],
 stars="0", repos="0", issues="0", forks="0",
 streak="1", streak_label="day",
)
BG="#0e0b1f"; LINE="#6d58b8"; LAV="#b79cff"; TXT="#e8e0ff"; SOFT="#9d8bd6"; CARD="#14102c"
FONTS=f"""<style>
@font-face{{font-family:'Cav';src:url(data:font/woff2;base64,{CAV}) format('woff2');font-weight:600}}
@font-face{{font-family:'Qs';src:url(data:font/woff2;base64,{QS}) format('woff2');font-weight:500}}
@font-face{{font-family:'Qs';src:url(data:font/woff2;base64,{QS6}) format('woff2');font-weight:600}}
.h{{font-family:'Cav','Segoe Script','Brush Script MT',cursive;font-weight:600;fill:{LAV}}}
.t{{font-family:'Qs','Trebuchet MS',Arial,sans-serif;font-weight:500;fill:{TXT}}}
.s{{font-family:'Qs','Trebuchet MS',Arial,sans-serif;font-weight:500;fill:{SOFT}}}
</style>"""
def svg(w,h,body,title,extra=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{title}</title><defs>{FONTS}{extra}</defs><rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>'
def spark(x,y,r,op=1,fill="none",sw=1.6,col=LAV):
    return f'<path d="M{x} {y-r} Q{x} {y} {x+r} {y} Q{x} {y} {x} {y+r} Q{x} {y} {x-r} {y} Q{x} {y} {x} {y-r}Z" fill="{fill}" stroke="{col}" stroke-width="{sw}" opacity="{op}" stroke-linejoin="round"/>'
def heart(x,y,s,col=LAV,fill="none"):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 6 C-12 -4 -6 -14 0 -7 C6 -14 12 -4 0 6Z" fill="{fill}" stroke="{col}" stroke-width="{1.6/s}" stroke-linejoin="round"/>'
def header(text,y,icon,x2=880):
    # icon drawn by caller at x=20; title at 70
    tw=len(text)*17+80
    return f'{icon}<text x="66" y="{y+10}" class="h" font-size="40">{text}</text><line x1="{max(tw,230)}" y1="{y}" x2="{x2}" y2="{y}" stroke="{LINE}" stroke-width="1.4"/>'
flower='<g transform="translate(%d %d)">%s<circle r="4" fill="#fff" opacity=".9"/></g>'
def blossom(x,y,s=1,op=1):
    pet="".join(f'<ellipse cx="0" cy="-9" rx="5.5" ry="9" fill="#b794f6" opacity="{op}" transform="rotate({a})"/>' for a in range(0,360,72))
    return f'<g transform="translate({x} {y}) scale({s})">{pet}<circle r="3" fill="#f3e6ff" opacity="{op}"/></g>'

# ---------- banner ----------
def banner():
    random.seed(7); st=""
    for _ in range(26):
        x=random.randint(30,880); y=random.randint(14,230)
        if 690<x<890 and y<225: continue
        st+=spark(x,y,random.choice([4,5,7]),op=random.choice([.4,.6,.9]),sw=1.2)
    sky="".join(f'<rect x="{x}" y="{y}" width="{w}" height="{225-y}" fill="#120e33"/>' for x,y,w in [(704,150,26),(732,120,22),(756,160,24),(782,100,30),(814,140,20),(836,128,28)])
    wins="".join(f'<rect x="{x}" y="{y}" width="4" height="5" fill="#d9c8ff" opacity=".8"/>' for x,y in [(790,112),(800,112),(790,126),(822,150),(844,140),(844,154),(740,134),(712,162)])
    cat=f'''<g>
<path d="M742 186 L748 150 L772 172Z M808 186 L802 150 L778 172Z" fill="#f6e9f7" stroke="#cdb8ff" stroke-width="1.5"/>
<path d="M750 174 L752 160 L764 172Z M800 174 L798 160 L786 172Z" fill="#f0b9d6"/>
<ellipse cx="775" cy="200" rx="40" ry="33" fill="#f6e9f7" stroke="#cdb8ff" stroke-width="1.5"/>
<ellipse cx="759" cy="198" rx="3" ry="4" fill="#3a2a66"/><ellipse cx="791" cy="198" rx="3" ry="4" fill="#3a2a66"/>
<path d="M772 207 q3 3 6 0" stroke="#3a2a66" stroke-width="1.6" fill="none" stroke-linecap="round"/>
<ellipse cx="750" cy="206" rx="6" ry="3.5" fill="#f4a6c6" opacity=".55"/><ellipse cx="800" cy="206" rx="6" ry="3.5" fill="#f4a6c6" opacity=".55"/>
<path d="M735 204 l-22 -4 M735 209 l-22 3 M815 204 l22 -4 M815 209 l22 3" stroke="#cdb8ff" stroke-width="1.3" stroke-linecap="round"/>
</g>'''
    sill='<rect x="692" y="222" width="196" height="27" fill="#2b2366"/><ellipse cx="750" cy="224" rx="11" ry="6" fill="#f6e9f7" stroke="#cdb8ff" stroke-width="1.3"/><ellipse cx="800" cy="224" rx="11" ry="6" fill="#f6e9f7" stroke="#cdb8ff" stroke-width="1.3"/>'
    win=f'''<rect x="700" y="16" width="180" height="206" rx="6" fill="#171347" stroke="#7a63c9" stroke-width="5"/>
<path d="M790 40 a24 24 0 1 0 22 33 a19 19 0 1 1 -22 -33Z" fill="#f1e8ff"/>{sky}{wins}
<circle cx="722" cy="52" r="1.6" fill="#fff"/><circle cx="760" cy="34" r="1.3" fill="#fff"/><circle cx="858" cy="92" r="1.5" fill="#fff"/>'''
    branch=f'<path d="M-5 70 Q50 50 85 18 M40 52 Q60 62 100 58 M20 62 Q22 85 48 98" stroke="#4b3580" stroke-width="3" fill="none"/>'+"".join(blossom(x,y,s,.95) for x,y,s in [(18,60,1.3),(55,40,1.2),(88,22,1.0),(34,86,1.0),(72,58,.9),(100,60,.8),(48,100,.8)])
    bow='<g transform="translate(95 205)" fill="none" stroke="#a78bfa" stroke-width="2.4" stroke-linejoin="round"><path d="M0 0 L-34 -17 Q-40 0 -34 17Z M0 0 L34 -17 Q40 0 34 17Z"/><circle r="5" fill="#a78bfa"/><path d="M-4 6 L-18 34 M4 6 L16 32"/></g>'
    body=f'''<rect x="1" y="1" width="898" height="248" rx="18" fill="url(#g)" stroke="{LINE}" stroke-width="1.5"/>{st}{branch}{bow}
<text x="345" y="128" class="h" font-size="84" text-anchor="middle" filter="url(#glow)" fill="#d7c6ff">Hi, I’m Akshita!</text>
<path d="M613 56 l14 -18 M626 70 l22 -12 M636 94 l18 -2" stroke="#cdb8ff" stroke-width="2.4" stroke-linecap="round" fill="none" opacity="0"/>
<text x="345" y="196" class="h" font-size="38" text-anchor="middle" style="fill:#c9b4ff">Welcome to my GitHub</text>{heart(552,184,1.5)}
<path d="M215 214 Q345 204 470 212" stroke="{LAV}" stroke-width="2" fill="none" stroke-linecap="round"/>
{win}{cat}{sill}'''
    ex='<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1d1245"/><stop offset=".6" stop-color="#150f33"/><stop offset="1" stop-color="#0e0b1f"/></linearGradient><filter id="glow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    return svg(900,262,body,"Hi, I’m Akshita! Welcome to my GitHub",ex)

# ---------- about ----------
def about():
    b=header("About Me",42,blossom(30,42,1.5))
    b+=f'<text x="22" y="108" class="t" font-size="21">Hey! I’m {CFG["name"]}, an Information Technology student at {CFG["college"]}.</text>'+spark(726,101,9,fill="#f5d36b",sw=0,col="#f5d36b")
    y=160
    for t in CFG["bullets"]:
        b+=spark(34,y-6,10,sw=1.6)+f'<text x="64" y="{y}" class="t" font-size="18.5">{t}</text>'; y+=40
    b+=f'<g transform="rotate(-6 760 238)"><text x="880" y="240" class="h" font-size="34" text-anchor="end">Dream · Learn · Build</text><path d="M706 258 Q800 244 884 248" stroke="{LAV}" stroke-width="1.6" fill="none"/></g>'
    b+=f'<path d="M826 292 L880 270 L852 298 L848 314 L840 302Z M880 270 L848 296" fill="none" stroke="{LAV}" stroke-width="2" stroke-linejoin="round"/><path d="M716 316 q20 -26 48 -20 t38 -8" stroke="{LAV}" stroke-width="1.6" fill="none" stroke-dasharray="6 7"/>'
    return svg(900,336,b,"About me")

# ---------- tech ----------
def tech():
    items=[("cplusplus","C++","-original"),("python","Python","-original"),("javascript","JavaScript","-original"),("react","React","-original"),("html5","HTML5","-original"),("css3","CSS3","-original"),("git","Git","-original"),("github","GitHub","-original"),("vscode","VS Code","-original")]
    laptop=f'<g transform="translate(14 22)" fill="none" stroke="{LAV}" stroke-width="2.4" stroke-linejoin="round"><rect x="4" y="2" width="30" height="22" rx="2"/><path d="M0 30 H38 L34 24 H4Z"/></g>'
    b=header("Tech Stack",42,laptop)+spark(868,34,9)+spark(884,52,5)
    n=len(items); step=94; x0=(900-step*n)/2+ (step-72)/2
    for i,(k,label,suf) in enumerate(items):
        f=f"{NM}devicon/icons/{k}/{k}{suf}.svg"
        try: d=b64(f)
        except Exception: d=b64(f"{NM}devicon/icons/{k}/{k}-plain.svg")
        x=x0+i*step
        c=x+36
        # github + vscode-friendly tile; github mark is black -> invert via light tile
        tile="#f4efff" if k=="github" else "#1b1638"
        b+=f'<rect x="{x}" y="82" width="72" height="72" rx="16" fill="{tile}" stroke="#2c2560" stroke-width="1.5"/><image x="{x+14}" y="96" width="44" height="44" href="data:image/svg+xml;base64,{d}"/><text x="{c}" y="182" class="t" font-size="15" text-anchor="middle">{label}</text>'
    return svg(900,206,b,"Tech stack: C++, Python, JavaScript, React, HTML5, CSS3, Git, GitHub, VS Code")

# ---------- stats ----------
def stats():
    def card(x,w,title,icon,inner): 
        return f'<rect x="{x}" y="8" width="{w}" height="232" rx="16" fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/><text x="{x+62}" y="62" class="h" font-size="34" style="fill:#cdb8ff">{title}</text>{icon}<path d="M{x+w-40} 44 h22 m-8 -8 l8 8 l-8 8" stroke="{LAV}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/><line x1="{x+24}" y1="82" x2="{x+w-24}" y2="82" stroke="#2c2560" stroke-width="1.5"/>{inner}'
    bars='<g fill="#8b6cf0"><rect x="0" y="14" width="7" height="12"/><rect x="11" y="6" width="7" height="20"/><rect x="22" y="-4" width="7" height="30"/></g>'
    rows=[("star","Total Stars",CFG["stars"]),("repo","Total Repos",CFG["repos"]),("iss","Total Issues",CFG["issues"]),("fork","Total Forks",CFG["forks"])]
    ic={"star":f'<path d="M0 -9 L2.6 -3 L9 -2.6 L4 1.8 L5.6 8 L0 4.6 L-5.6 8 L-4 1.8 L-9 -2.6 L-2.6 -3Z" fill="#f5d36b"/>',
        "repo":f'<rect x="-8" y="-9" width="16" height="18" rx="3" fill="none" stroke="{LAV}" stroke-width="2"/><path d="M-8 3 H8" stroke="{LAV}" stroke-width="2"/>',
        "iss":f'<circle r="9" fill="none" stroke="{LAV}" stroke-width="2"/><path d="M0 -4 V1" stroke="{LAV}" stroke-width="2.4" stroke-linecap="round"/><circle cy="5" r="1.4" fill="{LAV}"/>',
        "fork":f'<g fill="none" stroke="{LAV}" stroke-width="2"><circle cx="-6" cy="-7" r="2.5"/><circle cx="6" cy="-7" r="2.5"/><circle cy="8" r="2.5"/><path d="M-6 -4 V0 Q-6 3 0 3 Q6 3 6 0 V-4 M0 3 V5"/></g>'}
    inner=""
    for i,(k,l,v) in enumerate(rows):
        y=124+i*30
        inner+=f'<g transform="translate(50 {y-5})">{ic[k]}</g><text x="76" y="{y}" class="t" font-size="18">{l}</text><text x="240" y="{y}" class="t" font-size="18" style="font-weight:600">{v}</text>'
    cat='<g transform="translate(405 150)"><circle r="52" fill="#171236" stroke="#2c2560" stroke-width="2"/><circle r="38" fill="#a78bfa" opacity=".9"/><circle r="38" fill="#c4b0ff" opacity=".35"/></g>'
    cat+=f'<g transform="translate(405 152)" fill="#0e0b1f"><path d="M-18 -14 L-14 -28 L-4 -20 Q0 -21 4 -20 L14 -28 L18 -14 Q22 -2 12 10 Q0 18 -12 10 Q-22 -2 -18 -14Z" fill="#d9c9ff"/><circle cx="-8" cy="-4" r="2.2"/><circle cx="8" cy="-4" r="2.2"/></g>'+spark(470,98,7,sw=1.4)+spark(350,92,4,sw=1.2)+spark(455,200,5,sw=1.2)
    left=card(8,520,"GitHub Stats",f'<g transform="translate(30 30)">{bars}</g>',inner+cat)
    # streak
    random.seed(3); grid=""
    cols=15
    for c in range(cols):
        for r in range(7):
            v=random.random()
            col="#241d52" if v<.35 else "#4a3a96" if v<.65 else "#7e63e0" if v<.88 else "#b79cff"
            grid+=f'<rect x="{664+c*13.6}" y="{170+r*9.6}" width="10" height="7.5" rx="2" fill="{col}"/>'
    flame=lambda s,x,y:f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -20 C10 -8 16 0 12 12 C9 20 -9 20 -12 12 C-16 0 -6 -6 0 -20Z" fill="#ff7a3d"/><path d="M0 -4 C6 2 8 8 4 13 C1 16 -5 14 -5 9 C-5 4 -2 2 0 -4Z" fill="#ffc15a"/></g>'
    inner2=flame(1.25,700+0,0)  # placeholder not used
    sx=536
    inner2=(f'<text x="{sx+260}" y="132" class="h" font-size="56" text-anchor="middle" style="fill:#d7c6ff">{CFG["streak"]} {CFG["streak_label"]}</text>'
            f'{flame(1.1,sx+175,118)}<text x="{sx+260}" y="156" class="s" font-size="15" text-anchor="middle">Keep going!</text>'
            f'<g fill="{SOFT}" class="s" font-size="11"><text x="618" y="178">Mon</text><text x="618" y="197">Wed</text><text x="618" y="216">Fri</text></g>'+grid)
    right=card(536,356,"Contribution Streak",flame(1,576,44),inner2)
    return svg(900,248,left+right,"GitHub stats and contribution streak").replace('width="352"','')

# ---------- repos + footer ----------
def repos():
    star='<path d="M0 -14 L4 -4.5 L14 -4 L6.5 2.5 L9 12.5 L0 7 L-9 12.5 L-6.5 2.5 L-14 -4 L-4 -4.5Z" fill="#9d7bff" stroke="#b79cff" stroke-width="1.5" stroke-linejoin="round"/>'
    planet=f'<g transform="translate(822 66) rotate(-20)"><circle r="26" fill="#2a2166" stroke="{LAV}" stroke-width="2"/><ellipse rx="46" ry="11" fill="none" stroke="{LAV}" stroke-width="2"/><path d="M-26 -2 a26 26 0 0 1 52 0" fill="#2a2166" stroke="{LAV}" stroke-width="2" opacity="0"/></g>'
    b=f'<rect x="8" y="10" width="884" height="104" rx="16" fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/><g transform="translate(46 48)">{star}</g><text x="76" y="60" class="h" font-size="38" style="fill:#cdb8ff">Repositories</text><text x="46" y="96" class="t" font-size="18">Check out my repositories for more projects and experiments!</text><path d="M600 92 h50 m-10 -7 l10 7 l-10 7" stroke="{LAV}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>{planet}{spark(760,40,9)}{spark(712,86,4)}{spark(868,100,4)}'
    return svg(900,126,b,"Check out my repositories")

def footer():
    clouds="".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#2a2166"/>' for x,y,r in [(20,120,34),(60,128,30),(100,138,24),(790,128,26),(830,120,34),(872,124,36),(900,132,28)])
    b=f'<line x1="40" y1="46" x2="222" y2="46" stroke="{LINE}" stroke-width="1.4"/><line x1="678" y1="46" x2="860" y2="46" stroke="{LINE}" stroke-width="1.4"/>{spark(246,48,8)}{spark(654,48,8)}<text x="450" y="54" class="s" font-size="21" text-anchor="middle" letter-spacing="5" style="fill:#c9b4ff">Thanks for visiting!</text><rect y="96" width="900" height="44" fill="#1d1648" opacity="0"/>{clouds}'
    # heart placed after text, shift text a bit left
    return svg(900,140,b,"Thanks for visiting!")

for n,f in [("banner",banner),("about",about),("tech",tech),("stats",stats),("repos",repos),("footer",footer)]:
    open(f"./{n}.svg","w").write(f())
    print(n,len(f())//1024,"KB")
