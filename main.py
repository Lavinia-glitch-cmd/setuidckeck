import json
import numpy as np
import pandas as pd
from pathlib import Path
from strace import GetStraceDictionary
from parser import Get_SysCallTable
from vectorise import GetMatrices
    
def main():
    base_path = Path(__file__).resolve().parent
    logs_dir = base_path / "sudo_bin"
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
    np.set_printoptions(threshold=np.inf, suppress=True, linewidth=150)

    #print("\n--- MATRICEA COMPLETĂ PENTRU sudo_A ---")
    print(matrices)
  
if __name__ == "__main__":
    main()
    
