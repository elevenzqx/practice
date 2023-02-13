FROM tensorflow/tensorflow:2.0.0rc0-gpu-py3

RUN apt update && \ 
    apt install -y gcc python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev g++ git fish cmake build-essential vim htop openssh-server tree tmux bedtools 
RUN pip install pip -U && \ 
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install numpy pandas scikit-learn scikit-image matplotlib tqdm
