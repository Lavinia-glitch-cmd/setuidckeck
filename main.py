import json
import pandas as pd
import numpy as np
from pathlib import Path
import subprocess

from strace import GetStraceDictionary
from parser import Get_SysCallTable
from vectorise import Vectorise, GetMatrices
from flags import Get_BinaryFlags
from training import training

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
   
def GetVectors():
    SUID_binaries=Get_SUID_binaries()
    all_vectors=[]
    for binary_path, flags in SUID_binaries:
        bin_path = Path(binary_path)
        binary_name = bin_path.name
        try:
            vector=Generate_Binary(binary_name, flags)
            if vector is not None:
                all_vectors.append(vector)
            
        except Exception as e:
            print(f"Error found for {binary_name}: {e}")
    
    X=np.vstack(all_vectors)
    return X
  
 
def Generate_Binary(binary_name, flags):
    base_path = Path(__file__).resolve().parent
    main_logs_dir=base_path/"strace_logs"
    logs_dir = main_logs_dir / f"{binary_name}_flags"
    logs_dir.mkdir(parents=True, exist_ok=True)
    for flag in flags:
        output_path=logs_dir / f"{binary_name}_{flag.strip('-')}.txt"
        if not output_path.exists():
            cmd=f"sudo timeout 2s strace -c {binary_name} {flag} </dev/null > /dev/null 2> {output_path}"
            subprocess.run(cmd, shell=True)
            
            
    syscalls = Get_SysCallTable()
    strace_results={}
    if logs_dir.exists() and logs_dir.is_dir():
        for file in logs_dir.iterdir():
            if file.is_file():
                parsed_data=GetStraceDictionary(file)
                    
                if parsed_data:
                    strace_results[file.name] = GetStraceDictionary(file)
    else:
        return
    for file_name, strace_dict in strace_results.items():
        for strace_syscall_name in list(strace_dict.keys() ):
            if strace_syscall_name in syscalls.dict:
                syscall_no=syscalls.dict[strace_syscall_name][0][0]
                strace_dict[strace_syscall_name][0]["syscall_no"] = syscall_no 
    
    matrices=GetMatrices(strace_results, syscalls)
    vector=Vectorise(matrices)
    return vector
    
    

def Get_SUID_binaries():
    cmd= "find /bin /usr/bin /sbin -type f -perm /4000 2>/dev/null"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    paths= [b for b in result.stdout.split('\n') if b]
    binaries=[]
    
    
    for path in paths:
        binary_name=Path(path).name
        flags=Get_BinaryFlags(binary_name)
        valid_flags=[]
        if flags :
            for flag in flags:
                test_cmd = f"sudo timeout 1s strace -c {path} {flag} </dev/null"
                test_run = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
                
                output=test_run.stderr
                invalid_patterns=["requires an argument", "option", "Try"]
                if any(p in output for p in invalid_patterns):
                    continue
                else:
                    valid_flags.append(flag)
            if valid_flags:
                binaries.append((path, valid_flags))
        else:
            pass
    return binaries
        
  
    

def main():
    X=GetVectors()
    print(X.shape)
    training()
    
    
    
    
if __name__ == "__main__":
    main()
    
