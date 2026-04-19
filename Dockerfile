FROM aflplusplus/aflplusplus:latest

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-pandas \
    python3-sklearn \
    python3-joblib

RUN pip3 install onnxruntime --break-system-packages

WORKDIR /home/setuidcheck

