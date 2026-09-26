#!/usr/bin/env python3
from __future__ import annotations

import argparse, csv, html, json, re, tempfile, zipfile
from pathlib import Path
from urllib.parse import urlparse

ROLE_RULES = [
    (35, "founder", re.compile(r"\b(co[- ]?founder|founder|owner)\b", re.I)),
    (28, "executive", re.compile(r"\b(ceo|cto|cpo|cio|chief|vice president|\bvp\b|head of|director)\b", re.I)),
    (24, "hiring_manager", re.compile(r"\b(engineering manager|hiring manager|manager,? (engineering|product|design|research)|product manager lead)\b", re.I)),
    (20, "recruiter", re.compile(r"\b(recruiter|talent acquisition|talent partner|sourcer|recruiting)\b", re.I)),
]

FIELDS = ["contact_id","full_name","first_name","last_name","company","title","role_class","role_score","linkedin_url","x_url","x_handle","exported_email","source","connected_on","decision","notes"]

def clean(v): return re.sub(r"\s+", " ", str(v or "").strip())
def key(v): return re.sub(r"[^a-z0-9]+", "", clean(v).lower())
def classify(title):
    for score, label, rx in ROLE_RULES:
        if rx.search(title or ""): return label, score
    return ("manager_ambiguous", 12) if re.search(r"\bmanager\b", title or "", re.I) else ("other", 0)
def cid(*values):
    import hashlib
    return hashlib.sha256("|".join(clean(v).lower() for v in values if clean(v)).encode()).hexdigest()[:16]

def resolve(path, wanted):
    p=Path(path)
    if p.is_file() and p.suffix.lower()==".zip":
        td=Path(tempfile.mkdtemp(prefix="network-export-")); zipfile.ZipFile(p).extractall(td); p=td
    if p.is_dir():
        hits=[x for x in p.rglob("*") if x.is_file() and wanted(x)]
        if not hits: raise FileNotFoundError(f"No matching export file under {p}")
        return hits[0]
    return p

def linkedin_rows(path):
    p=resolve(path, lambda x: x.name.lower()=="connections.csv")
    with p.open(encoding="utf-8-sig", errors="replace", newline="") as f:
        rows=list(csv.DictReader(f))
    out=[]
    for r in rows:
        first=clean(r.get("First Name")); last=clean(r.get("Last Name")); name=clean(first+" "+last)
        url=clean(r.get("URL") or r.get("Profile URL")); company=clean(r.get("Company")); title=clean(r.get("Position") or r.get("Title"))
        role,score=classify(title)
        out.append(dict(contact_id=cid(url,name,company),full_name=name,first_name=first,last_name=last,company=company,title=title,role_class=role,role_score=score,linkedin_url=url,x_url="",x_handle="",exported_email=clean(r.get("Email Address")),source="linkedin_connections",connected_on=clean(r.get("Connected On")),decision="unreviewed",notes=""))
    return out

def x_rows(path):
    p=resolve(path, lambda x: x.name.lower()=="following.js")
    text=p.read_text(encoding="utf-8",errors="replace")
    text=re.sub(r"^\s*window\.YTD\.following\.part\d+\s*=\s*", "", text).rstrip(";\n ")
    data=json.loads(text); out=[]
    for item in data:
        r=item.get("following",item); url=clean(r.get("userLink")); handle=urlparse(url).path.strip("/").split("/")[-1] if url else ""
        out.append(dict(contact_id=cid(url,r.get("accountId")),full_name=handle,first_name="",last_name="",company="",title="",role_class="unresearched",role_score=0,linkedin_url="",x_url=url,x_handle=handle,exported_email="",source="x_following",connected_on="",decision="unreviewed",notes=""))
    return out

def dedupe(rows):
    out=[]; by={}
    for r in rows:
        keys=[key(r.get("linkedin_url")),key(r.get("x_url")),key(r.get("exported_email"))]
        existing=next((by[k] for k in keys if k and k in by),None)
        if existing:
            for f in FIELDS:
                if not existing.get(f) and r.get(f): existing[f]=r[f]
            existing["source"]="+".join(sorted(set(existing["source"].split("+"))|set(r["source"].split("+"))))
        else:
            out.append(r)
            for k in keys:
                if k: by[k]=r
    return out

def write_dashboard(rows,path):
    data=json.dumps(rows,ensure_ascii=False).replace("</","<\\/")
    doc='''<!doctype html><meta charset="utf-8"><title>Network Outreach Review</title><style>
body{font:14px system-ui;margin:0;background:#f6f5f2;color:#191817}header{position:sticky;top:0;background:#fff;padding:16px 22px;border-bottom:1px solid #ddd;z-index:2}h1{margin:0 0 8px}input,select,button{padding:8px;margin:3px;border:1px solid #bbb;border-radius:7px;background:#fff}button{cursor:pointer}.wrap{padding:16px 22px}.card{background:#fff;border:1px solid #ddd;border-radius:10px;padding:12px;margin:8px 0;display:grid;grid-template-columns:2fr 1fr auto;gap:12px}.muted{color:#6d6963}.pill{display:inline-block;padding:2px 7px;border-radius:20px;background:#eee;margin-right:4px}.actions button.active{background:#1d4ed8;color:#fff}.meta{font-size:12px}.count{font-weight:650}
</style><header><h1>Network Outreach Review</h1><span class="count" id="count"></span> <input id="q" placeholder="Search name, company, title"> <select id="source"><option value="">All sources</option><option>linkedin_connections</option><option>x_following</option></select><select id="decision"><option value="">All decisions</option><option>unreviewed</option><option>target</option><option>known_person</option><option>peer_level</option><option>do_not_contact</option><option>research_later</option></select><button onclick="download()">Export decisions CSV</button></header><div class="wrap" id="list"></div><script>
const rows=__DATA__; const decisions=JSON.parse(localStorage.getItem('network-decisions')||'{}'); rows.forEach(r=>r.decision=decisions[r.contact_id]||r.decision);
const labels={target:'Target',known_person:'Known person',peer_level:'Peer level',do_not_contact:'Do not contact',research_later:'Research later'};
function setd(id,d){decisions[id]=d;localStorage.setItem('network-decisions',JSON.stringify(decisions));rows.find(r=>r.contact_id===id).decision=d;render()}
function render(){const q=document.querySelector('#q').value.toLowerCase(),s=document.querySelector('#source').value,d=document.querySelector('#decision').value;const f=rows.filter(r=>(!q||JSON.stringify(r).toLowerCase().includes(q))&&(!s||r.source.includes(s))&&(!d||r.decision===d));count.textContent=`${f.length} shown of ${rows.length}`;list.innerHTML=f.map(r=>`<div class=card><div><b>${esc(r.full_name||r.x_handle)}</b><div>${esc(r.title)}${r.company?' at '+esc(r.company):''}</div><div class=meta>${r.linkedin_url?`<a href="${esc(r.linkedin_url)}">LinkedIn</a> `:''}${r.x_url?`<a href="${esc(r.x_url)}">X</a> `:''}${esc(r.exported_email)}</div></div><div><span class=pill>${esc(r.role_class)}</span><span class=muted>score ${r.role_score}</span><div class=meta>${esc(r.source)}</div></div><div class=actions>${Object.entries(labels).map(([k,v])=>`<button class="${r.decision===k?'active':''}" onclick="setd('${r.contact_id}','${k}')">${v}</button>`).join('')}</div></div>`).join('')}
function esc(s){return String(s||'').replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]))}
function download(){const cols=['contact_id','decision','notes'];const lines=[cols.join(','),...rows.map(r=>cols.map(c=>'"'+String(c==='decision'?(decisions[r.contact_id]||r.decision):(r[c]||'')).replaceAll('"','""')+'"').join(','))];const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([lines.join('\n')],{type:'text/csv'}));a.download='network_decisions.csv';a.click()}
q.oninput=source.onchange=decision.onchange=render;render();
</script>'''.replace("__DATA__",data)
    path.write_text(doc,encoding="utf-8")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--linkedin"); ap.add_argument("--x"); ap.add_argument("--output-dir",required=True); a=ap.parse_args()
    rows=[]
    if a.linkedin: rows+=linkedin_rows(a.linkedin)
    if a.x: rows+=x_rows(a.x)
    if not rows: ap.error("Provide --linkedin and/or --x")
    rows=dedupe(rows); out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    with (out/"normalized_contacts.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    write_dashboard(rows,out/"network_review.html")
    print(json.dumps({"contacts":len(rows),"csv":str(out/"normalized_contacts.csv"),"dashboard":str(out/"network_review.html")},indent=2))
if __name__=="__main__": main()
