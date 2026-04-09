from structures import Dictionary

def GetStraceDictionary(file):
    result=Dictionary()
    coloumn_header=[]
    with open(file) as f:
        for line in f:
            line=line.strip()
            if any(x in line for x in [ "---", "usage", "[", "/usr", "total" ]):
                continue
            line=line.split()
            if line[0] == '%':
                time_percentage="".join(line[0:2])
                coloumn_header=[ time_percentage ] + line[2:]
                continue
            if ',' in line[0]:
                data={}
                line[0]=float(line[0].replace(',', '.'))
                if len(line) == 5 :
                    line.insert(4, '0')
                #print(line)
                data={ coloumn_header[i]: line[i] for i in range(len(line)) }
                result[line[-1]]=data
    return result.dict
                


    
        
