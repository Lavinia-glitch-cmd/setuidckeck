import subprocess 
import re

def Get_BinaryFlags(binary):
    try :
        cmd = f"man {binary} | col -b"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        man_text = result.stdout
        if not man_text.strip():
            return []
        pattern = r'^\s+(-[a-zA-Z0-9])[\s,]'
        found_flags = re.findall(pattern, man_text, re.MULTILINE)
        binary_flags = sorted(list(set(found_flags)))
        
        return binary_flags
        
    except FileNotFoundError:
        print(f"Eroare: Comanda 'man' sau binarul '{binary}' nu a fost găsit.")
        return []
    except Exception as e:
        print(f"Eroare neașteptată la extragerea flag-urilor: {e}")
        return []
