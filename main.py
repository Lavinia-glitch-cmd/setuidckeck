import json
import pandas as pd
import numpy as np


from strace import GetStraceDictionary
from parser import Get_SysCallTable
from vectorise import Vectorise, GetMatrices, GetVectors
from flags import Get_BinaryFlags
from training import training

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
    
    

def main():
   # X=GetVectors()
    training()

if __name__ == "__main__":
    main()
    
