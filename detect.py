import onnxruntime as rt
import joblib
import numpy as np
from flags import GenerateVectorForDetection
from parser import Get_SysCallTable

syscalls=Get_SysCallTable()
inference=rt.InferenceSession("isolation_forest_onnx")
_scaler=joblib.load("scaler.pkl")

def detect(file):
    
    vector=GenerateVectorForDetection(file, syscalls)
    vector_scaled = _scaler.transform([vector]).astype(np.float32)
