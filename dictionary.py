from collections.abc import MutableMapping

class Dictionary(MutableMapping):
    def __init__(self):
        self.dict={}
        
    def __getitem__(self, key):
        return self.dict[key]
        
    def __setitem__(self, key, value):
        if key not in self.dict: 
            self.dict[key]=[]
        
        self.dict[key].append(value) 
        
    def __delitem__(self, key):
        del self.dict[key]
        
    def __iter__(self):
        keys=list(self.dict.keys())
        keys.sort()
        for key in keys:
            yield key
            
    def __len__(self):
        return len(self.dict)



try:
    with open("syscall_no.txt") as f:
        SysCallTable=Dictionary()
        
        for line in f:
            line=line.strip().split()
           
            number=int(line[0])
            name=line[2]
            entry_point=line[3] if len(line) > 3 else "N/A"
            
            SysCallTable[name]=[number, entry_point]
            
             
    import json
    #print(json.dumps(SysCallTable.dict, indent=4))
            
except FileNotFoundError:
    print("file not found")
