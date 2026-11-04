#!/usr/bin/env python3
"""Fetch real GitHub stats and regenerate assets/stats.svg (stdlib only).
Env: GH_TOKEN (required unless --demo), USERNAME (required unless --demo)."""
import base64, json, os, sys, urllib.request, datetime
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
def b64(n): return base64.b64encode(open(os.path.join(HERE,"fonts",n),"rb").read()).decode()
CAV=b64("caveat-latin-600-normal.woff2"); QS=b64("quicksand-latin-500-normal.woff2"); QS6=b64("quicksand-latin-600-normal.woff2")
BG="#0e0b1f"; LINE="#6d58b8"; LAV="#b79cff"; TXT="#e8e0ff"; SOFT="#9d8bd6"; CARD="#14102c"
WEEKS=15

def gql(token,query,variables):
    req=urllib.request.Request("https://api.github.com/graphql",json.dumps({"query":query,"variables":variables}).encode(),
        {"Authorization":f"bearer {token}","Content-Type":"application/json","User-Agent":"readme-stats"})
    d=json.load(urllib.request.urlopen(req,timeout=30))
    if "errors" in d: raise SystemExit(f"GraphQL error: {d['errors']}")
    return d["data"]["user"]

Q="""query($login:String!,$after:String){user(login:$login){
 issues{totalCount}
 contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount contributionLevel}}}}
 repositories(ownerAffiliations:OWNER,privacy:PUBLIC,first:100,after:$after){totalCount pageInfo{hasNextPage endCursor} nodes{stargazerCount forkCount}}}}"""

def fetch(token,login):
    stars=forks=0; after=None
    while True:
        u=gql(token,Q,{"login":login,"after":after}); r=u["repositories"]
        for n in r["nodes"]: stars+=n["stargazerCount"]; forks+=n["forkCount"]
        if not r["pageInfo"]["hasNextPage"]: break
        after=r["pageInfo"]["endCursor"]
    weeks=u["contributionsCollection"]["contributionCalendar"]["weeks"]
    days=[d for w in weeks for d in w["contributionDays"]]
    return dict(stars=stars,forks=forks,repos=r["totalCount"],issues=u["issues"]["totalCount"],days=days,weeks=weeks[-WEEKS:])

def streak(days):
    s=0; today=datetime.date.today().isoformat()
    for i,d in enumerate(reversed(days)):
        if d["contributionCount"]>0: s+=1
        elif i==0 and d["date"]>=today: continue   # today not over yet
        else: break
    return s

def demo():
    import random; random.seed(1); lv=["NONE","FIRST_QUARTILE","SECOND_QUARTILE","THIRD_QUARTILE","FOURTH_QUARTILE"]
    w=[{"contributionDays":[{"date":"2026-01-01","contributionCount":1,"contributionLevel":random.choice(lv)} for _ in range(7)]} for _ in range(WEEKS)]
    return dict(stars=12,forks=3,repos=9,issues=2,days=[{"date":"2026-01-01","contributionCount":1}]*5,weeks=w)

def spark(x,y,r,sw=1.4):
    return f'<path d="M{x} {y-r} Q{x} {y} {x+r} {y} Q{x} {y} {x} {y+r} Q{x} {y} {x-r} {y} Q{x} {y} {x} {y-r}Z" fill="none" stroke="{LAV}" stroke-width="{sw}" stroke-linejoin="round"/>'
def flame(s,x,y): return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -20 C10 -8 16 0 12 12 C9 20 -9 20 -12 12 C-16 0 -6 -6 0 -20Z" fill="#ff7a3d"/><path d="M0 -4 C6 2 8 8 4 13 C1 16 -5 14 -5 9 C-5 4 -2 2 0 -4Z" fill="#ffc15a"/></g>'
COL={"NONE":"#241d52","FIRST_QUARTILE":"#4a3a96","SECOND_QUARTILE":"#6a52c8","THIRD_QUARTILE":"#7e63e0","FOURTH_QUARTILE":"#b79cff"}

def build(st):
    def card(x,w,title,icon,inner):
        return f'<rect x="{x}" y="8" width="{w}" height="232" rx="16" fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/><text x="{x+62}" y="62" class="h" font-size="34" style="fill:#cdb8ff">{title}</text>{icon}<path d="M{x+w-40} 44 h22 m-8 -8 l8 8 l-8 8" stroke="{LAV}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/><line x1="{x+24}" y1="82" x2="{x+w-24}" y2="82" stroke="#2c2560" stroke-width="1.5"/>{inner}'
    bars='<g fill="#8b6cf0"><rect x="0" y="14" width="7" height="12"/><rect x="11" y="6" width="7" height="20"/><rect x="22" y="-4" width="7" height="30"/></g>'
    ic={"star":'<path d="M0 -9 L2.6 -3 L9 -2.6 L4 1.8 L5.6 8 L0 4.6 L-5.6 8 L-4 1.8 L-9 -2.6 L-2.6 -3Z" fill="#f5d36b"/>',
        "repo":f'<rect x="-8" y="-9" width="16" height="18" rx="3" fill="none" stroke="{LAV}" stroke-width="2"/><path d="M-8 3 H8" stroke="{LAV}" stroke-width="2"/>',
        "iss":f'<circle r="9" fill="none" stroke="{LAV}" stroke-width="2"/><path d="M0 -4 V1" stroke="{LAV}" stroke-width="2.4" stroke-linecap="round"/><circle cy="5" r="1.4" fill="{LAV}"/>',
        "fork":f'<g fill="none" stroke="{LAV}" stroke-width="2"><circle cx="-6" cy="-7" r="2.5"/><circle cx="6" cy="-7" r="2.5"/><circle cy="8" r="2.5"/><path d="M-6 -4 V0 Q-6 3 0 3 Q6 3 6 0 V-4 M0 3 V5"/></g>'}
    rows=[("star","Total Stars",st["stars"]),("repo","Total Repos",st["repos"]),("iss","Total Issues",st["issues"]),("fork","Total Forks",st["forks"])]
    inner=""
    for i,(k,l,v) in enumerate(rows):
        y=124+i*30; inner+=f'<g transform="translate(50 {y-5})">{ic[k]}</g><text x="76" y="{y}" class="t" font-size="18">{l}</text><text x="240" y="{y}" class="t" font-size="18" style="font-weight:600">{v}</text>'
    cat=f'<g transform="translate(405 150)"><circle r="52" fill="#171236" stroke="#2c2560" stroke-width="2"/><circle r="38" fill="#a78bfa" opacity=".9"/><circle r="38" fill="#c4b0ff" opacity=".35"/></g><g transform="translate(405 152)"><path d="M-18 -14 L-14 -28 L-4 -20 Q0 -21 4 -20 L14 -28 L18 -14 Q22 -2 12 10 Q0 18 -12 10 Q-22 -2 -18 -14Z" fill="#d9c9ff"/><circle cx="-8" cy="-4" r="2.2" fill="{BG}"/><circle cx="8" cy="-4" r="2.2" fill="{BG}"/></g>'+spark(470,98,7)+spark(350,92,4)+spark(455,200,5)
    left=card(8,520,"GitHub Stats",f'<g transform="translate(30 30)">{bars}</g>',inner+cat)
    grid=""
    for c,w in enumerate(st["weeks"]):
        for r,d in enumerate(w["contributionDays"]):
            grid+=f'<rect x="{664+c*13.6:.1f}" y="{170+r*9.6:.1f}" width="10" height="7.5" rx="2" fill="{COL.get(d["contributionLevel"],COL["NONE"])}"/>'
    n=streak(st["days"]); label="day" if n==1 else "days"
    msg="Keep going!" if n else "Start a new streak today!"
    inner2=(f'<text x="796" y="132" class="h" font-size="56" text-anchor="middle" style="fill:#d7c6ff">{n} {label}</text>{flame(1.1,711-(10 if n>9 else 0),118)}'
            f'<text x="796" y="156" class="s" font-size="15" text-anchor="middle">{msg}</text>'
            f'<g class="s" font-size="11"><text x="618" y="187">Mon</text><text x="618" y="206">Wed</text><text x="618" y="226">Fri</text></g>'+grid)
    right=card(536,356,"Contribution Streak",flame(1,576,44),inner2)
    css=f"""<style>@font-face{{font-family:'Cav';src:url(data:font/woff2;base64,{CAV}) format('woff2');font-weight:600}}@font-face{{font-family:'Qs';src:url(data:font/woff2;base64,{QS}) format('woff2');font-weight:500}}@font-face{{font-family:'Qs';src:url(data:font/woff2;base64,{QS6}) format('woff2');font-weight:600}}
.h{{font-family:'Cav','Segoe Script',cursive;font-weight:600;fill:{LAV}}}.t{{font-family:'Qs','Trebuchet MS',Arial,sans-serif;font-weight:500;fill:{TXT}}}.s{{font-family:'Qs','Trebuchet MS',Arial,sans-serif;font-weight:500;fill:{SOFT}}}</style>"""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="248" viewBox="0 0 900 248" role="img"><title>GitHub stats and contribution streak</title><defs>{css}</defs><rect width="900" height="248" fill="{BG}"/>{left}{right}</svg>'

if __name__=="__main__":
    if "--demo" in sys.argv: st=demo()
    else: st=fetch(os.environ["GH_TOKEN"],os.environ["USERNAME"])
    out=os.path.join(ROOT,"assets","stats.svg") if "--demo" not in sys.argv else "/tmp/stats-demo.svg"
    os.makedirs(os.path.dirname(out),exist_ok=True); open(out,"w").write(build(st)); print("wrote",out)
