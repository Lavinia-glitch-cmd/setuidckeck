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
                
            if started_strace:
                line_parts=line.split()
                
                if "total" in line.lower():
                    seconds=float(line_parts[1].replace(',', '.'))
                    usecs_per_call=int(line_parts[2])
                    if seconds == 0.0 and usecs_per_call == 0:
                        return None
                        
                if line_parts[0][0].isdigit():
                    data={}
                    line_parts[0]=float(line_parts[0].replace(',', '.'))
                    if len(line_parts) == 5 :
                        line_parts.insert(4, '0')
                    data={ coloumn_header[i]: line_parts[i] for i in range(len(line_parts)) }
                    result[line_parts[-1]]=data
    
    return result.dict
                


    
        
