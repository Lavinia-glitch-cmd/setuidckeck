import json
import numpy as np
import pandas as pd
from pathlib import Path
from strace import GetStraceDictionary
from parser import Get_SysCallTable

def vectorise(dictionary):
    vectorised_data={}
    columns = ["syscall_no", "%time", "seconds", "usecs/call", "calls", "errors"]
    for file_name, syscall_dict in dictionary.items():
        rows_file=[]
        for syscall_name, data_list in syscall_dict.items():
            rows_data=data_list[0]
            print(data_list[0])
            row=[]

            for col in columns:
                val=rows_data.get(col, 0)
                try:
                    row.append(float(val))
                except (ValueError, TypeError):
                    row.append(0.0)
            rows_file.append(row)
        if rows_file:
            vectorised_data[file_name] = np.array(rows_file)
        else:
            vectorised_data[file_name] = np.zeros((0, len(columns)))
            
    return vectorised_data
    
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
    matrices=vectorise(strace_results)
    print(matrices)
  
if __name__ == "__main__":
    main()
    
