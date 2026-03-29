#!/usr/bin/python3
import json

import numpy as np
strace={}
try:
    with open("sudo_date.txt") as f:
        for linie in f:
            linie=linie.strip()
            if not linie or linie.startswith('%') or linie.startswith('-'):
                continue
            if not linie or not linie[0].isdigit():
                continue
            elemente = linie.split()
            x=0
            if len(elemente) == 5:
                pertime, sec, usec, calls, syscallname = elemente
                errors=0
            elif len(elemente) == 6:
                pertime, sec, usec, calls,errors, syscallname = elemente
            

            else: 
                continue
            pertime=pertime.replace(',', '.')
            sec=sec.replace(',', '.')
            strace[syscallname]={
                'pertime': float(pertime),
                'seconds': float(sec),
                'usecpertime': int(usec),
                'calls': int(calls),
                'errors': int(errors),
                'syscallname': syscallname,
                'syscallno': 0
            }

except FileNotFoundError:
    print("file not found")
except Exception as e:
    print(f"{e}")

syscalls={}
try:
    with open("syscall_no.txt") as f:
        for linie in f:
            linie=linie.strip()
            elemente=linie.split()
            if len(elemente) >= 3:
                try:
                    sysno=int(elemente[0])
                    sysname=elemente[2]
                    # print(elemente[2])

                    syscalls[sysname] ={
                        'syscallno': sysno, 
                        'syscallname':sysname
                    }      
                except ValueError:
                    continue
except FileNotFoundError:
    print("file not found")
for name in syscalls:
    number=syscalls[name]['syscallno']
    if name in strace:
        strace[name]['syscallno']=number

# print(json.dumps(syscalls, indent=4))
print(json.dumps(strace, indent=3))

for v in strace.values():
    print(v)


l=[ [v['pertime'] , v['seconds'] , v['usecpertime'],  v['calls'], v['errors'], v['syscallno']] for v in strace.values() ]
m=np.array(l).reshape(-1,6)

print(m)