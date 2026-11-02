#!/usr/bin/env python3
"""Validate the retained Abstract Pipeline Representation from a JSON (YAML-subset) file.

This checks design consistency, not native platform syntax or actual runner success.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def cyclic(graph):
    visiting=set();done=set()
    def visit(n):
        if n in visiting:return True
        if n in done:return False
        visiting.add(n)
        if any(visit(x) for x in graph.get(n,[]) if x in graph):return True
        visiting.remove(n);done.add(n);return False
    return any(visit(n) for n in graph)


def validate(doc):
    errors=[]
    a=doc.get('apr') if isinstance(doc,dict) else None
    if not isinstance(a,dict):return {'valid':False,'errors':['Expected apr object']}
    if a.get('version')!='1.0':errors.append('Unsupported APR version; expected 1.0')
    stages=a.get('stages')
    if not isinstance(stages,list) or not stages:return {'valid':False,'errors':errors+['At least one stage is required']}
    stage_names={};jobs={};jobstage={};sg={};jg={}
    for s in stages:
        if not isinstance(s,dict) or not isinstance(s.get('name'),str) or not s['name']:
            errors.append('Every stage needs a nonempty name');continue
        n=s['name']
        if n in stage_names:errors.append('Duplicate stage: '+n)
        stage_names[n]=s
        dep=s.get('depends_on')
        if dep is None:dep=[]  # Omitted/null is allowed by the retained schema.
        if not isinstance(dep,list) or any(not isinstance(x,str) for x in dep):errors.append('Stage dependencies must be names: '+n);dep=[]
        sg[n]=dep
        if not isinstance(s.get('jobs'),list) or not s['jobs']:errors.append('Stage has no jobs: '+n);continue
        for j in s['jobs']:
            if not isinstance(j,dict) or not isinstance(j.get('name'),str) or not j['name']:
                errors.append('Every job needs a nonempty name');continue
            name=j['name']
            if name in jobs:errors.append('Duplicate global job name: '+name)
            jobs[name]=j;jobstage[name]=n
            deps=j.get('depends_on')
            if deps is None:deps=[]
            if not isinstance(deps,list) or any(not isinstance(x,str) for x in deps):errors.append('Job dependencies must be names: '+name);deps=[]
            jg[name]=deps
            if not isinstance(j.get('timeout_minutes'),int) or isinstance(j.get('timeout_minutes'),bool) or not 1<=j['timeout_minutes']<=360:
                errors.append('Job timeout must be 1..360 minutes: '+name)
            if not isinstance(j.get('runner'),str) or not j['runner']:errors.append('Job runner missing: '+name)
            steps=j.get('steps')
            if not isinstance(steps,list) or not steps:errors.append('Job steps missing: '+name);continue
            for step in steps:
                if not isinstance(step,dict) or step.get('type') not in ('checkout','setup','cache','run','upload','download'):
                    errors.append('Unknown step type in '+name);continue
                if step['type']=='run' and (not isinstance(step.get('command'),str) or not step['command'].strip()):errors.append('Run step needs a command: '+name)
    for n,deps in sg.items():
        for d in deps:
            if d not in stage_names:errors.append(f'Unknown stage dependency {n} -> {d}')
    # Stage prerequisites also create edges between their jobs. This exposes
    # cross-stage job cycles hidden by separately acyclic stage/job graphs.
    combined={n:list(ds) for n,ds in jg.items()}
    for n,deps in jg.items():
        for d in deps:
            if d not in jobs:errors.append(f'Unknown job dependency {n} -> {d}')
        for sn in sg.get(jobstage[n],[]):combined[n].extend(x for x in jobs if jobstage[x]==sn)
    if cyclic(sg):errors.append('Stage dependency cycle')
    if cyclic(combined):errors.append('Job/stage dependency cycle')
    secrets=a.get('secrets') or []
    if not isinstance(secrets,list):errors.append('Secrets must be an array');secrets=[]
    secret_names={x.get('name') for x in secrets if isinstance(x,dict) and isinstance(x.get('name'),str)}
    for s in secrets:
        if not isinstance(s,dict):errors.append('Invalid secret declaration');continue
        for j in s.get('required_for') or []:
            if j not in jobs:errors.append('Secret references unknown job: '+str(j))
    for n,j in jobs.items():
        for step in j.get('steps') or []:
            if isinstance(step,dict):
                for name in step.get('secrets') or []:
                    if name not in secret_names:errors.append(f'Undeclared secret {name} in {n}')
    for item in a.get('artifacts') or []:
        if not isinstance(item,dict):errors.append('Invalid artifact declaration');continue
        if item.get('produced_by') not in jobs:errors.append('Artifact producer missing: '+str(item.get('name')))
        for n in item.get('consumed_by') or []:
            if n not in jobs:errors.append('Artifact consumer missing: '+str(n))
    envs={e.get('name'):e for e in (a.get('environments') or []) if isinstance(e,dict)}
    for n,s in stage_names.items():
        if s.get('environment') and s['environment'] not in envs:errors.append('Undeclared stage environment: '+n)
    return {'format':'apr-validation/1','valid':not errors,'errors':errors,'stages':len(stage_names),'jobs':len(jobs),
            'limits':'Structural APR checks only; native config, action pinning, credentials and real runner/deployment acceptance require separate verification.'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('apr_json',type=Path);a=p.parse_args(argv)
    try:r=validate(json.loads(a.apr_json.read_text()));print(json.dumps(r,indent=2));return 0 if r['valid'] else 1
    except (ValueError,OSError,TypeError) as e:p.exit(2,f'{type(e).__name__}: {e}\n')

if __name__=='__main__':raise SystemExit(main())
