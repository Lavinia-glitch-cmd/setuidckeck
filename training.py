import joblib
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

import numpy as np

from skl2onnx import update_registered_converter
from skl2onnx.common.data_types import FloatTensorType
from skl2onnx import convert_sklearn

from vectorise import GetVectors

def training():
    
    all_vectors=GetVectors()
    Path("models").mkdir(parents=True, exist_ok=True)
    for binary_name, X in all_vectors.items():
        scaler=StandardScaler()
        X_scaled=scaler.fit_transform(X)
        
        clf=IsolationForest(contamination=0.01, random_state=42).fit(X_scaled)
    
        joblib.dump(scaler, f"models/scaler_{binary_name}.pkl")
        initial_type=[('float_input', FloatTensorType([None, X.shape[1]]))]
    
    
    
    #specified version because of runtime errors: RuntimeError: The model is using version 4 of domain 'ai.onnx.ml' not supported yet by this library. You need to specify target_opset={'ai.onnx.ml': 3}, and '':15 is general

        onx = convert_sklearn(clf, initial_types=initial_type, target_opset={'':15, 'ai.onnx.ml':3})
    
        onnx_path=f"models/model_{binary_name}.onnx"
        with open(onnx_path, "wb") as f:
            f.write(onx.SerializeToString())
        
        
