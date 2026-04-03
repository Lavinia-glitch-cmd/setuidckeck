from collections.abc import MutableMapping

class Dictionary(MutableMapping):
    def __init__(self):
        self.dict={}
    def __getitem__(self, key):
        return self.dict[key]
    def __setitem__(self, key, value):
        self.dict[key]=value     
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
            #print(line)
            sys_call_number=int(line[0])
            entry_name=line[2]
            if len(line) > 3:
                kernel_symbol=line[3]
            print('%s %s %s' % (sys_call_number, entry_name, kernel_symbol) )
            temporary_list=[sys_call_number, entry_name]
            for key, value in SysCallTable.items():
                __setitem__(SysCallTable, key, value)
            print(SysCallTable.dict)
            
            
            
        
            
            
            
except FileNotFoundError:
    print("file not found")
