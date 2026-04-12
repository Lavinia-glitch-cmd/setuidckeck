from structures import Dictionary

def GetStraceDictionary(file):
    result=Dictionary()
    coloumn_header=[]
    started_strace=False
    
    with open(file) as f:
        for line in f:
            line=line.strip()
            if not line : continue
            
            if "% time" in line and not coloumn_header:
                line=line.split()
                time_percentage="".join(line[0:2])
                coloumn_header=[ time_percentage ] + line[2:]
                continue
                
            if "------" in line:
                if not started_strace:
                    started_strace=True
                    continue
                else:
                    break
            if started_strace:
                line=line.split()
                
                if line[0][0].isdigit():
                    data={}
                    line[0]=float(line[0].replace(',', '.'))
                    if len(line) == 5 :
                        line.insert(4, '0')
                    data={ coloumn_header[i]: line[i] for i in range(len(line)) }
                    result[line[-1]]=data
    print(result.dict)
    return result.dict
                


    
        
