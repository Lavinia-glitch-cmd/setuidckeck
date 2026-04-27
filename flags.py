import subprocess 
import re
from pathlib import Path
from parser import Get_SysCallTable
from strace import GetStraceDictionary
import shutil



def Get_BinaryFlags(binary):
    try :
        cmd = f"man {binary} | col -b"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        man_text = result.stdout
        if not man_text.strip():
            return []
        pattern = r'^\s+(-[a-zA-Z0-9-]+)[\s,]'
        flags = re.findall(pattern, man_text, re.MULTILINE)
        binary_flags = sorted(list(set(flags)))
        
        return binary_flags
        
    except FileNotFoundError:
        print(f"Eroare: Comanda 'man' sau binarul '{binary}' nu a fost găsit.")
        return []
    except Exception as e:
        print(f"Eroare neașteptată la extragerea flag-urilor: {e}")
        return []
        
def GenerateVectorForDetection(file_path, syscalls):
    parsed_data=GetStraceDictionary(file_path)
    for syscall_name in list(parsed_data.keys()):
        if syscall_name in syscalls.dict:
            syscall_no = syscalls.dict[syscall_name][0][0]
            parsed_data[syscall_name][0]["syscall_no"]=syscall_no
    res={file_path.name:parsed_data}
    from vectorise import GetMatrices, Vectorise
    matrices=GetMatrices(res, syscalls)
    vector=Vectorise(matrices)
    return vector

def get_vector(file, syscalls):
    parsed_data=GetStraceDictionary(file)
    if parsed_data:
        for syscall_name in list(parsed_data.keys()):
            if syscall_name in syscalls.dict:
                sys_id= syscalls.dict[syscall_name][0][0]
                parsed_data[syscall_name][0]["syscall_no"]=sys_id
    return parsed_data
        
def Generate_Binary(binary_name, binary_path, flags=None,  log=None):
    syscalls=Get_SysCallTable()
    strace_results={}

    if log:
        path=Path(log)
        return GenerateVectorForDetection(log, syscalls)
    
    base_path=Path(__file__).resolve().parent

    logs_dir=base_path / "strace_logs" / binary_name
    logs_dir.mkdir(exist_ok=True, parents=True)

    input_dir=logs_dir / "input_binaries"
    input_dir.mkdir(exist_ok=True, parents=True)

    output_dir=logs_dir / "strace_logs" / "output_dir"
    output_dir.mkdir(exist_ok=True, parents=True)
    
    for flag in flags:
        input_file=input_dir/"flag_{flag}.txt"
        with open(input_file, 'r') as f_in:
            for argument in f_in.readlines():
                output_file=output_dir/f"{binary_name}_{flag}_{argument}.txt"
                cmd=["sudo", "strace", "-c", binary_path, flag, argument]
            try:
                with open(output_file, 'w') as f_out:
                    subprocess.run(cmd, stderr=f_out, stdin.subprocess.DEVNULL, check=True)
                    strace_results[f_out] = get_vector(f_out, syscalls)
    #with open(input_file, 'r') as f:
        #for argument in f.readlines():
         #   argument=argument.strip()
          #  for flag in flags:
           #     input_file_flag=input_to_flag_file/"flag_{f}"
            #    output_file = output_dir / f"{binary_name}_{flag}_{argument}.txt"
             
             #for argument in 
              #  cmd = ["sudo", "strace", "-c", binary_path, flag, argument]
           # try:
            #    with open(output_file, "w") as out_f:
             #       subprocess.run(cmd, stderr=out_f, stdin=subprocess.DEVNULL, #check=True)
                    
                   # strace_results[out_f] = get_vector(out_f, syscalls)
                    
            except Exception as e:
                print(f"eroare: {e}")
                
    if not strace_results:
         return None       
    from vectorise import GetMatrices, Vectorise
    matrices=GetMatrices(strace_results, syscalls)
    vector=Vectorise(matrices)
    return vector
     
def Get_SUID_binaries():
    
    cmd= "find /bin /usr/bin /sbin -type f -perm /4000 2>/dev/null"
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    paths= [b for b in result.stdout.split('\n') if b]
    binaries=[]
    
    for path in paths:
        print(path)
        binary_name=Path(path).name
        flags=Get_BinaryFlags(binary_name)
        binaries.append((path, flags))
    return binaries
 
