import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


def training():
    from main import GetVectors
    X=GetVectors()
    scaler=StandardScaler()
    X_scaled=scaler.fit_transform(X)
    
    clf=IsolationForest(contamination=0.05).fit(X_scaled)
    
    print(list(clf.predict(X)).count(-1))
