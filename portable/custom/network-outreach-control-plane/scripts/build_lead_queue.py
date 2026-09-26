#!/usr/bin/env python3
import argparse,csv,json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--contacts',required=True); ap.add_argument('--decisions',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    contacts=list(csv.DictReader(open(a.contacts,encoding='utf-8-sig')))
    decisions={r['contact_id']:r for r in csv.DictReader(open(a.decisions,encoding='utf-8-sig'))}
    fields=list(contacts[0])+['decision_notes','research_status','company_domain','current_title_source_url','fit_signal','fit_signal_url','email','email_status','email_source_url','email_source_type','verification_provider','verified_at','approval_status']
    out=[]
    for r in contacts:
        d=decisions.get(r['contact_id'],{})
        if d.get('decision')!='target': continue
        r['decision']='target'; r['decision_notes']=d.get('notes',''); r.update(research_status='pending',company_domain='',current_title_source_url='',fit_signal='',fit_signal_url='',email='',email_status='not_found',email_source_url='',email_source_type='',verification_provider='',verified_at='',approval_status='research_required'); out.append(r)
    out.sort(key=lambda r:int(r.get('role_score') or 0),reverse=True)
    p=Path(a.output);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
    print(json.dumps({'targets':len(out),'output':str(p)},indent=2))
if __name__=='__main__': main()
