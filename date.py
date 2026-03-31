#!/usr/bin/python3
import json
import pandas as pd
import numpy as np
import os
programe=["sudo", "passwd"]
director=os.listdir(".")

def vectorise(fisier, syscalls):
    strace={}

    try:
        with open(fisier) as f:
            for linie in f:
                linie=linie.strip()
                if not linie or linie.startswith('%') or linie.startswith('-'):
                    continue
                if not linie or not linie[0].isdigit():
                    continue
                elemente = linie.split()
                
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
        for name in syscalls:
            number=syscalls[name]['syscallno']
            if name in strace:
                strace[name]['syscallno']=number
        d=[
            ('syscallname', 'U40'),
            ('pertime', 'O'),
            ('seconds', 'O'),
            ('usecpertime', 'i4'),
            ('calls', 'i4'),
            ('errors', 'i4'),
            ('syscallno', 'i4')
        ]
        l=[ (v['syscallname'], v['pertime'] , v['seconds'] , v['usecpertime'],  v['calls'], v['errors'], v['syscallno']) for k, v in strace.items() if k!='total' ]
        return np.array(l, dtype=d)

    except FileNotFoundError:
        print("file not found")
    except Exception as e:
        print(f"{e}")
    return None

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
matrices={}
for progr in programe:
    for fisier in director:
        if fisier.startswith(f"{progr}") and not fisier.endswith(('.py','.sh','.txt')):
            matrice=vectorise(fisier, syscalls)
            #print(f"pentru fisierul {fisier}:")
            #print(matrice, end="\n\n")
            if matrice is not None:
                matrices[fisier]=matrice
                
            
for nume, mat in matrices.items():
    print(f"--- Matrice pentru {nume} (forma {mat.shape}) ---")
    df=pd.DataFrame(mat)
    df=df.set_index('syscallname')
    print(df)
    x=df['calls'].sum()
    print(x)
    
    
