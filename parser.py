from pathlib import Path
from structures import Dictionary

def Get_SysCallTable():
    base_path=Path(__file__).resolve().parent
    file_path=base_path/"syscall_no.txt"
    
    SysCallTable=Dictionary()
    try:
        with open(file_path) as f:
            for line in f:
                line=line.strip().split()
                try:
                    syscall_number=int(line[0])
                    syscall_name=line[2]
                    entry_point=line[3] if len(line) > 3 else "N/A"
                    SysCallTable[syscall_name]=[syscall_number, entry_point]
                except ValueError: 
                    continue
    except FileNotFoundError:
        return None
    print(SysCallTable.dict)
    return SysCallTable

    
        
