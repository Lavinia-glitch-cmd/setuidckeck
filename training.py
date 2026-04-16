import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

import numpy as np

from skl2onnx import update_registered_converter
from skl2onnx.common.data_types import FloatTensorType
from skl2onnx import convert_sklearn

def training():
    from main import GetVectors
    X=GetVectors()
    scaler=StandardScaler()
    X_scaled=scaler.fit_transform(X)
    
    clf=IsolationForest(contamination='auto').fit(X_scaled)
    np.set_printoptions(threshold=np.inf)
    print(clf.predict(X_scaled))
    
