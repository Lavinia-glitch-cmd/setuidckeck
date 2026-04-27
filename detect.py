import onnxruntime as rt
import joblib
import numpy as np
from flags import GenerateVectorForDetection
from parser import Get_SysCallTable


def detect(file):
    syscalls=Get_SysCallTable()
    sess=rt.InferenceSession("isolation_forest_onnx", providers=rt.get_available_providers())
    _scaler=joblib.load("scaler.pkl")
    
    
   
    
    vector=GenerateVectorForDetection(file, syscalls)
    vector_scaled = _scaler.transform([vector]).astype(np.float32)
    
    ###https://onnxruntime.ai/docs/api/python/tutorial.html
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    
    pred_onx = sess.run([label_name], {input_name: vector_scaled})[0]
