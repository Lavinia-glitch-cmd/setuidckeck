import numpy as np
import pandas as pd
from pathlib import Path
import subprocess
from flags import Get_SUID_binaries, Generate_Binary 

def Vectorise(matrices):
    vector=[]
    for name, mat in matrices.items():
        line=mat[:, 1:]
        vector.append(line.flatten())
    return np.array(vector)

def GetVectors(file=None):
    
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

def GetMatrices(strace_results, syscalls_dict):
    matrices={}
    columns = ["%time", "seconds", "usecs/call", "calls", "errors"]
    syscalls=[]
    for syscall_name, entry  in syscalls_dict.items():
        syscall_no=entry[0][0]
        syscalls.append((syscall_no, syscall_name))
    syscalls.sort()
    
    for file_name, file_data in strace_results.items():
        
        file_matrix = np.zeros((len(syscalls), 6))
        
        for i, (sys_no, sys_name) in enumerate(syscalls):
            file_matrix[i, 0] = sys_no
            if sys_name in file_data:
                stats = file_data[sys_name][0]
                for col_idx, col_name in enumerate(columns, start=1):
                    val = stats.get(col_name, 0)
                    try:
                        file_matrix[i, col_idx] = float(val)
                    except:
                        file_matrix[i, col_idx] = 0.0
        matrices[file_name] = file_matrix
      
        
    return matrices
