FROM python:3.7

RUN pip install numpy
RUN pip3 install torch==1.9.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install transformers
RUN pip install scikit-learn

RUN pip install celery
RUN pip install redis
RUN pip install Flask

COPY LSML-FinalProject/models/bert-tokenizer.bin bert-tokenizer.bin
COPY LSML-FinalProject/models/bert-model.bin bert-model.bin
COPY LSML-FinalProject/models/LDA.bin LDA.bin
COPY LSML-FinalProject/models/LDA_vec.bin LDA_vec.bin

COPY LSML-FinalProject/server.py server.py
COPY LSML-FinalProject/models.py models.py

COPY LSML-FinalProject/start.sh start.sh

ENTRYPOINT ["/bin/bash","start.sh"]
