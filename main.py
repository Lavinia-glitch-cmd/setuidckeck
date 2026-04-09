import json
from pathlib import Path
from strace import GetStraceDictionary
from parser import Get_SysCallTable

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
    print(json.dumps(strace_results, indent=4))

if __name__ == "__main__":
    main()
