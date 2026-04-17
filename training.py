import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

import numpy as np

from skl2onnx import update_registered_converter
from skl2onnx.common.data_types import FloatTensorType
from skl2onnx import convert_sklearn

from vectorise import GetVectors

def training():
    
    X=GetVectors()
    scaler=StandardScaler()
    X_scaled=scaler.fit_transform(X)
    
    clf=IsolationForest(contamination='auto', random_state=42).fit(X_scaled)
    import sys 
    np.set_printoptions(threshold=sys.maxsize)
    print(clf.predict(X_scaled))

    joblib.dump(scaler, "scaler.pkl")
    _type=[('float_input', FloatTensorType([None, X.shape[1]]))]
    
    
    
    #specified version because of runtime errors: RuntimeError: The model is using version 4 of domain 'ai.onnx.ml' not supported yet by this library. You need to specify target_opset={'ai.onnx.ml': 3}, and '':15 is general

    onx = convert_sklearn(clf, initial_types=_type, target_opset={'':15, 'ai.onnx.ml':3})
    
    
    with open("isolation_forest.onnx", "wb") as f:
        f.write(onx.SerializeToString())
        
        
