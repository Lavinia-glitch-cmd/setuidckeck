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

   
        
# def Generate_Binary(binary_name,binary_path=None, flags=None, log=None):
#     strace_results={}
#     syscalls = Get_SysCallTable()
#     if log:
#         _path=Path(log)
#         return GenerateVectorForDetection(_path, syscalls)
        
        
#     base_path=Path(__file__).resolve().parent
#     logs_dir=base_path /"strace_logs" / f"{binary_name}_flags_fuzzer"
#     input_dir=base_path / "strace_logs" / "inputs" / f"in_{binary_name}_flags"
#     output_dir=base_path/ "strace_logs" / "outputs" / f"out_{binary_name}_flags"

#     input_dir.mkdir(parents=True, exist_ok=True)
#     logs_dir.mkdir(parents=True, exist_ok=True)
    
#     output_dir.parent.mkdir(parents=True, exist_ok=True)
    
#     for d in [input_dir, output_dir, logs_dir]:
#         if d.exists():
#             shutil.rmtree(d)
#         d.mkdir(parents=True, exist_ok=True)
    
#     if not any(input_dir.iterdir()):
#         if flags and len(flags)>0:
#             for index, flag in enumerate(flags):
#                 seed_file=input_dir / f"seed_{index}.txt"
#                 with open(seed_file, "w") as f:
                   
#                     f.write(flag)
#         else:
#             with open(input_dir / "seed.txt", "w") as f:
#                 f.write("-h")
        
#     dict_file = base_path / "dicts" / f"{binary_name}.dict"
#     dict_cmd = f"-x {dict_file}" if dict_file.exists() else ""    
#     fuzzer_cmd= f"timeout 60s afl-fuzz -Q {dict_cmd} -i {input_dir} -o {output_dir} -- {binary_path} @@"
#     subprocess.run(fuzzer_cmd, shell=True)
    
#     queue_dir=output_dir / "default" / "queue"
#     if queue_dir.exists():
#         seeds=sorted([ s for s in queue_dir.iterdir() if s.is_file() ])
#         for i, seed in enumerate(seeds):
#             output_path=logs_dir/f"{binary_name}_fuzz_{i}.txt"
#             if not output_path.exists():
#                 with open(seed, errors='ignore') as f:
#                     content= f.read(100).strip()
                    
#                 binary_name=binary_path.name
#                 cmd=f"timeout 2s strace -c {binary_name} {content} </dev/null 2> {output_path}"
#                 subprocess.run(cmd, shell=True)
                
#                 parsed_data=GetStraceDictionary(output_path)
                    
#                 if parsed_data:
#                     for syscall_name in list(parsed_data.keys()):
#                         if syscall_name in syscalls.dict:
#                             s_id = syscalls.dict[syscall_name][0][0]
#                             parsed_data[syscall_name][0]["syscall_no"] = s_id
                
                
#                     strace_results[output_path.name] = parsed_data
                
#     if not strace_results:
#         print(f"[!] Atenție: Nu s-au generat date strace pentru {binary_name}")
#         return None       
#     from vectorise import GetMatrices, Vectorise
#     matrices=GetMatrices(strace_results, syscalls)
#     vector=Vectorise(matrices)
#     return vector


            




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
        
