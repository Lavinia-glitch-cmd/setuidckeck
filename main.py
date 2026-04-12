import json
import pandas as pd
import numpy as np
import pandas as pd
from pathlib import Path
import subprocess

from strace import GetStraceDictionary
from parser import Get_SysCallTable
from vectorise import GetMatrices, Vectorise
from flags import Get_BinaryFlags

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
    
def main():
    binary_name="sudo"
    base_path = Path(__file__).resolve().parent
    
    logs_dir = base_path / f"{binary_name}_flags"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    flags=Get_BinaryFlags(binary_name)
    
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
    scaler = StandardScaler()
    vector_scaled=scaler.fit_transform(vector)
    
    np.set_printoptions(threshold=np.inf, suppress=True, linewidth=300)
    #print(vector)
    
    
    #print(matrices)
  
if __name__ == "__main__":
    main()
    
